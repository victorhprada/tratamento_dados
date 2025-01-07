import pandas as pd
import numpy as np

pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('clientes_remove_outliers.csv')

print(df.head())
#Mascarar dados pessoas
df['cpf_mascara'] = df['cpf'].apply(lambda cpf: f'{cpf[:3]}.***.***-{cpf[-2:]}')
print(f"\n DataFrame com CPF mascarádos: \n {df.head()}")

# Corrigir datas
df['data'] = pd.to_datetime(df['data'], errors='coerce')
print(f"\n DataFrame com datas corrigidas: \n {df.head()}")

date_today = pd.to_datetime('today')
df['data_atualizada'] = df['data'].where(df['data'] <= date_today, pd.to_datetime('1900-01-01')) # Alterar as datas inválidas para uma data padrão
df['idade_ajustada'] = date_today.year - df['data_atualizada'].dt.year # Calcula a idade ajustada com base no ano atual
df['idade_ajustada'] -= ((date_today.month <= df['data_atualizada'].dt.month) & (date_today.day < df['data_atualizada'].dt.day)).astype(int) # Se a opção for verdadeira será retornado 1, se não 0
df.loc[df['idade_ajustada'] > 100, 'idade_ajustada'] = np.nan # Vai substituir os valor que são maiores do que 100 por NaN
print(f"\n DataFrame com data atualizada e idade ajustada conforme ano: \n {df[['data_atualizada', 'idade_ajustada']]}")

# Corrigir campo com múltiplas informações
df['endereco_curto'] = df['endereco'].apply(lambda x: x.split('\n')[0].strip()) # Extrai a primeira linha do endereço e cria uma coluna chamada endereco_curto
df['bairro'] = df['endereco'].apply(lambda x: x.split('\n')[1].strip() if len(x.split('\n')) > 1 else 'Bairro Desconhecido') # Extrai a segunda linha e se não existir, troca o nome para bairro desconhecido
df['estado_sigla'] = df['endereco'].apply(lambda x: x.split(' / ')[-1].strip().upper() if len(x.split('\n')) > 1 else 'Estado Desconhecido') # Divide a string e seleciona o último elemento da lista
df['cep'] = df['endereco'].apply(lambda x: x.split('\n')[2].split()[0] if isinstance(x, str) and len(x.split('\n')) > 2 else 'CEP Desconhecido') # Após acessar a terceira linha, divide a linha em palavras e seleciona a primeira palavra onde se encontra o cep
df['nome_endereco'] = df['endereco'].apply(lambda x: x.split('\n')[2].split(maxsplit=2)[1]
                                           if isinstance(x, str) and len(x.split('\n')) > 2 and len(x.split('\n')[2].split()) > 1 
                                           else 'Nome do Endereço Desconhecido') # Divide a string e seleciona a posição em que se encontra o nome do endereço
print(f"\n DataFrame com endereços: \n {df[['endereco_curto', 'bairro', 'estado_sigla', 'cep', 'nome_endereco']]}")

# Verificar formatação do endereço
df['endereco_curto'] = df['endereco_curto'].apply(lambda x: 'Endereço inválido' if len(x) > 50 or len(x) < 5 else x) # Endereços maiores que 50 caracteres ou menores do que 5 caracteres seram subsitituidos por endereço inválido

# Corrigir dados erroneos
df['cpf'] = df['cpf'].apply(lambda x: x if len(x) == 14 or len(x) == 11 else 'CPF inváido')

print(f"\nDados tratados: \n {df.head()}")

df['cpf'] = df['cpf_mascara']
df['idade'] = df['idade_ajustada']
df['endereco'] = df['endereco_curto']
df['estado'] = df['estado_sigla']
df_salvar = df[['nome', 'cpf', 'idade', 'data', 'endereco', 'bairro', 'estado', 'cep']]

print(f"\nDados tratados: \n {df_salvar.head()}")

df_salvar.to_csv('clientes_tratados.csv', index=False)
print(f"Novo DataFrame: \n {pd.read_csv('clientes_tratados.csv')}")