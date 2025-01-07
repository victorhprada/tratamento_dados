import pandas as pd

df = pd.read_csv('/Users/victorhugopradateixeira/Documents/Python(Dados)/Tratamento de Dados/tratamento_dados/clientes.csv')

# Verificar os primeiros registros
print(df.head().to_string())

# Verifica os últimos registros
print(df.tail().to_string())

# Verifica a quantidade de linhas e colunas
print(f"\nQuantidade: {df.shape}")

# Verifica tipos de dados
print(f"\nTipagem: \n{df.dtypes}")

# Checagem de valores nulos
print(f"\nValores nulos: \n{df.isnull().sum()}")