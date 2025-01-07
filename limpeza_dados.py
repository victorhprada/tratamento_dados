import pandas as pd

df = pd.read_csv('clientes.csv')

pd.set_option('display.width', None)
print(f"Primeiro DataFrame: \n {df.head()}")

# Remover dados que não serão utilizados
df.drop(labels='pais', axis=1, inplace=True) # Coluna
df.drop(labels=2, axis=0, inplace=True) # Linha

# Normalizar campos de texto
df['nome'] = df['nome'].str.title()
df['endereco'] = df['endereco'].str.lower()
df['estado'] = df['estado'].str.strip().str.upper()

# Converter tipos de dados
df['idade'] = df['idade'].astype(int)

print(f"\nSegundo DataFrame: \n {df.head()}")

# Tratar valores nulos (ausentes)
df_fillna = df.fillna(0) # Substituir valores nulos por 0
df_dropna = df.dropna() # Remover registros com valores nulos
df_dropna4 = df.dropna(thresh=4) # Manter registros com no mínimo 4 valores não nulos
df = df.dropna(subset=['cpf']) # Remover registro com cpf nulo

print(f"\nValores nulos: \n {df.isnull().sum()}")
print(f"\nQuantidade de registros nulos com fillna: \n {df_fillna.isnull().sum().sum()}")
print(f"\nQuantidade de registros nulos com dropna: \n {df_dropna.isnull().sum().sum()}")
print(f"\nQuantidade de registros nulos com dropna4: \n {df_dropna4.isnull().sum().sum()}")
print(f"\nQuantidade de registros nulos com CPF: \n {df.isnull().sum().sum()}")

df.fillna(value={'estado': 'Desconhecido'}, inplace=True) # Se o estado for nulo sera adicionado o texto desconhecido
df['endereco'] = df['endereco'].fillna('Endereço não informado') # Outro jeito de fazer a mesma coisa da linha de cima
df['idade_corrigida'] = df['idade'].fillna(df['idade'].mean()) # Adciona a média quando o campo possuir um valor nulo

# Tratar formato de dados
df['data_corrigida'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
print(f"\nTerceiro DataFrame com Alteração de Data: \n {df.head()}")

# Tratar valores duplicados
print(f"\nQuantidade de registros atual: {df.shape[0]}") # Shape mostra linhas e colunas
df.drop_duplicates()
df.drop_duplicates(subset='cpf', inplace=True) # Remove os cpf's duplicados
print(f"\nQuantidade de registros removendo as duplicadas: {len(df)}")
print(f"\nQuarto DataFrame com Dados Limpos: \n {df}")

# Salvar o DataFrame
df['data'] = df['data_corrigida']
df['idade'] = df['idade_corrigida']

df_salvar = df[['nome', 'cpf', 'idade', 'data','endereco', 'estado']]
df_salvar.to_csv('clientes_limpeza.csv', index=False)

print(f"\nNovo DataFram Tratado: \n{pd.read_csv('clientes_limpeza.csv')}")