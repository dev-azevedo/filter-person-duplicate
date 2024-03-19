import sqlite3
import os
from pprint import pprint
import requests
import logging


def conectar_db():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco_dados = os.path.join(caminho_atual, 'DB', 'comprasoft.db')
    os.makedirs(os.path.dirname(caminho_banco_dados), exist_ok=True)
    
    conn = sqlite3.connect(caminho_banco_dados)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    return conn, cursor

def configurar_logger(name_file):
    logging.basicConfig(filename=f'{name_file}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def remover_mascara(item):
    # Remover caracteres que não são dígitos
    item = ''.join(filter(str.isdigit, item))
    
    return item

def consulta_cnpj(cnpj):
    cnpj_sem_mascara = remover_mascara(cnpj)
    conn, cursor = conectar_db()
    print(cnpj_sem_mascara)
    cursor.execute(f'SELECT * FROM parceiros WHERE cnpj = ?', (cnpj_sem_mascara,))
    cliente = cursor.fetchone()
    
    if cliente:
        cliente_dict = dict(zip([col[0] for col in cursor.description], cliente))
        pprint(cliente_dict)
    
    conn.close()
    
def buscar_todos_clientes(table, typeEntity):
    conn, cursor = conectar_db()
    
    entities = cursor.execute(f'SELECT * FROM {table}').fetchall()
    conn.row_factory = sqlite3.Row 
    
    for entity in entities:
        telefone_celular = entity['telefone'] if entity['telefone'] and len(entity['telefone']) == 11 else None
        telefone = entity['telefone'] if entity['telefone'] and len(entity['telefone']) == 10 else None
        nome_fantasia = entity['nome_fantasia'].strip() if entity['nome_fantasia']  and entity['nome_fantasia'] != "" else None
       
        entity_db = {
            "name": entity['nome_razao_social'].strip(),
            "fantasyName": nome_fantasia,
            "cpfCnpj": entity['cnpj'].strip(),
            "registration": None,
            "isSeller": False,
            "isEmployee": False,
            "isSupplier": False,
            "isCompany": False,
        }
        
        if typeEntity == "cliente":
            entity_db['isClient'] = True
            entity_db['isPartner'] = False
        else:
            entity_db['isClient'] = False
            entity_db['isPartner'] = True
        
        if telefone is not None or telefone_celular is not None or entity['email'] is not None:
            entity_db['contact'] = {
                "email": entity['email'],
                "phoneNumber": telefone,
                "cellPhoneNumber": telefone_celular,
                "isWhatsApp": False,
                "typeContactId": 4,
            }
            
        if entity['logradouro'] is not None or entity['cep'] is not None:
            complemento = entity['complemento'].strip() if entity['complemento'] and not "*" in entity['complemento'] else None
            entity_db['address'] = {
                "streetAddress": entity['logradouro'].strip(),
                "number": entity['numero'].strip(),
                "cep": entity['cep'].strip(),
                "district": entity['bairro'].strip(),
                "city": entity['municipio'].strip(),
                "uf": entity['uf'].strip(),
                "complement": complemento
            }

        url_api = f'http://localhost:5046/api/Person'
        
        response = requests.post(url_api, json=entity_db)

        if response.status_code == 200:
            dados_api = response.json()
            print(f"Dados do {typeEntity} {entity['Id']}")
            pprint(dados_api)
        else:
            print(f"Falha ao obter dados do {typeEntity} {entity['Id']}. Código de resposta: {response.status_code}")
            logging.error(f"""
                          Falha ao cadastrar {typeEntity.upper()}. 
                            ID sqlite: {entity['Id']};  
                            entity: {entity_db};
                            Error: {response.text}
                        """)
        print("\n")

    conn.close()
  
configurar_logger("log_error")  
buscar_todos_clientes('clientes', 'cliente')
buscar_todos_clientes('parceiros', 'parceiro')

# consulta_cnpj("12.932.245/0001-36")