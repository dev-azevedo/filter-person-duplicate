import pandas as pd
import sqlite3
import os
import requests
from requests.auth import HTTPBasicAuth

def conectar_db():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco_dados = os.path.join(caminho_atual, 'DB', 'comprasoft.db')
    os.makedirs(os.path.dirname(caminho_banco_dados), exist_ok=True)
    
    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()
    
    return conn, cursor

# def criar_tabelas():
#     conn, cursor = conectar_db()

#     # Criar tabela empresas se não existir
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS clientes (
#             Id INTEGER PRIMARY KEY,
#             cnpj TEXT UNIQUE NOT NULL,
#             nome_razao_social TEXT NOT NULL,
#             nome_fantasia TEXT,
#             logradouro TEXT,
#             numero TEXT,
#             complemento TEXT,
#             cep TEXT,
#             bairro TEXT,
#             municipio TEXT,
#             uf TEXT,
#             email TEXT,
#             telefone TEXT
#         )
#     ''')

#     # Criar tabela empresas_divergentes se não existir
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS clientes_divergentes (
#             Id INTEGER PRIMARY KEY,
#             cnpj TEXT NOT NULL,
#             nome_razao_social TEXT NOT NULL,
#             nome_fantasia TEXT,
#             logradouro TEXT,
#             numero TEXT,
#             complemento TEXT,
#             cep TEXT,
#             bairro TEXT,
#             municipio TEXT,
#             uf TEXT,
#             email TEXT,
#             telefone TEXT
#         )
#     ''')
    
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS parceiros (
#             Id INTEGER PRIMARY KEY,
#             cnpj TEXT UNIQUE NOT NULL,
#             nome_razao_social TEXT NOT NULL,
#             nome_fantasia TEXT,
#             logradouro TEXT,
#             numero TEXT,
#             complemento TEXT,
#             cep TEXT,
#             bairro TEXT,
#             municipio TEXT,
#             uf TEXT,
#             email TEXT,
#             telefone TEXT
#         )
#     ''')

#     conn.commit()
#     conn.close()

# def remover_mascara(item):
#     # Remover caracteres que não são dígitos
#     item = ''.join(filter(str.isdigit, item))
    
#     return item

# def buscar_dados_por_cnpj(cnpj):
#     response = requests.get(f"https://consulta-cnpj.tributojusto.com.br/consulta/{cnpj}", auth=HTTPBasicAuth("salesforce", "S@lesForce_2023"))

#     if response.status_code == 200:
#         data = response.json()
#         return data['result']
    
#     return None
           
# def adicionar_na_tabela(cnpj, nome, table):
#     cnpj = remover_mascara(cnpj)
#     conn, cursor = conectar_db()

#     cursor.execute(f'SELECT * FROM {table} WHERE cnpj = ?', (cnpj,))
#     resultado = cursor.fetchone()
    
#     if resultado is None and cnpj and cnpj != '0' and cnpj != '':
#         if len(cnpj) == 14:
#             dados_empresa = buscar_dados_por_cnpj(cnpj)
#             if dados_empresa:
#                 telefone = dados_empresa.get('telefone')
#                 fantasia = None if "*****" in dados_empresa.get('fantasia') else dados_empresa.get('fantasia')
#                 cep = remover_mascara(dados_empresa.get('cep')) if dados_empresa.get('cep') else None
                
#                 cursor.execute(f"""
#                             INSERT INTO {table} 
#                             (cnpj, nome_razao_social, nome_fantasia, logradouro, numero, complemento, cep, bairro, municipio, UF, email, telefone) 
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
#                             (cnpj, dados_empresa['nome'], fantasia, dados_empresa['logradouro'], dados_empresa['numero'], dados_empresa['complemento'], cep, dados_empresa['bairro'], dados_empresa['municipio'], dados_empresa['uf'], dados_empresa['email'], telefone))
#                 print(f'Adicionado na tabela: {table} - CNPJ: {cnpj}, Nome: {nome}')
#             else: 
#                 cursor.execute(f'INSERT INTO {table} (cnpj, nome_razao_social) VALUES (?, ?)', (cnpj, nome))
#                 print(f'Adicionado na tabela: {table} - CNPJ: {cnpj}, Nome: {nome}')
#         else: 
#             cursor.execute(f'INSERT INTO {table} (cnpj, nome_razao_social) VALUES (?, ?)', (cnpj, nome))
#             print(f'Adicionado na tabela: {table} - CNPJ: {cnpj}, Nome: {nome}')
#     else:
#         print(f'Duplicado ou inválido: CNPJ: {cnpj}, Nome: {nome}')
#         if table == 'clientes': 
#             cursor.execute(f'SELECT * FROM clientes_divergentes WHERE cnpj = ? AND nome_razao_social = ?', (cnpj, nome))
#             resultado = cursor.fetchone()
            
#             if resultado is None:
#                 cursor.execute('INSERT INTO clientes_divergentes (cnpj, nome_razao_social) VALUES (?, ?)', (cnpj, nome))
#                 print(f'Adicionado a clientes_divergentes: CNPJ: {cnpj}, Nome: {nome}')

#     conn.commit()
#     conn.close()

# def exportar_para_txt(table, nome_txt):
#     conn, cursor = conectar_db()

#     cursor.execute(f'SELECT * FROM {table}')
#     resultados = cursor.fetchall()
    
#     caminho_completo = os.path.join("txt_exportados", f'{nome_txt}.txt')

#     with open(caminho_completo, 'w', encoding='utf-8') as file:
#         for resultado in resultados:
#             id, cnpj, nome_razao_social = resultado
#             file.write(f'{cnpj} | {nome_razao_social}\n')

#     conn.close()

# def cadastrar_entidades(df, table):
#     for index, row in df.iterrows():
#         cnpj = str(row['CNPJ'])
#         nome_empresa = str(row['NOME'])
#         adicionar_na_tabela(cnpj, nome_empresa, table)
#     print("\n")

# df_clientes = pd.read_excel('Planilhas/Clientes.xlsx')
# df_parceiros = pd.read_excel('Planilhas/Parceiros.xlsx')

# criar_tabelas()

# cadastrar_entidades(df_clientes, 'clientes')
# cadastrar_entidades(df_parceiros, 'parceiros')
#     # exportar_para_txt('clientes', 'dados_clientes')
#     # exportar_para_txt('clientes_divergentes', 'dados_clientes_divergentes')
#     # exportar_para_txt('parceiros', 'dados_parceiros')

# print('Concluído! As empresas foram adicionadas ao banco de dados, as divergentes foram salvas em Clientes_divergentes.txt. Os dados completos foram exportados para dados_empresas.txt.')
