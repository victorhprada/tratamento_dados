import pandas as pd
from scipy import stats

pd.set_option('display.width', None)

df = pd.read_csv('clientes_limpeza.csv')

df_filtro_basico = df[df['idade'] > 100]
print(f"Filtro Básico: \n {df_filtro_basico[['nome', 'idade']]}")
print(f"\nQuantidade de Cadastros com Mais de 100 anos:  {df_filtro_basico.shape[0]}")

# Identificar outliers com Z-score > 3
z_scor = stats.zscore(df['idade'].dropna()) #.dropna() -> Trata valores nulos
outliers_z = df[z_scor >= 3]
print(f"\nZ-score: \n {z_scor}")
print(f"\nOutliers pelo Z-score: \n {outliers_z}")

# Filtrar outliers com Z-score < 3
ds_zscore = df[(stats.zscore(df['idade']) < 3)]
print(f"\n Filtrando outliers: \n {ds_zscore}")

# Identificar outliers com IQR
Q1 = df['idade'].quantile(0.25) # 1 Quadrante = 25%
Q3 = df['idade'].quantile(0.75) # 3 Quadrante = 75%
IQR = Q3 - Q1

limite_baixo = Q1 - 1.5 * IQR
limite_alto = Q3 + 1.5 * IQR

print(f"\nLimites IQR: \n Limite baixo: {limite_baixo} \n Limite auto: {limite_alto}")

# Buscar os outliers que estão a baixo do limite baixo e a cima do limite alto
outliers_iqr = df[(df['idade'] < limite_baixo) | (df['idade'] > limite_alto)]
print(f"\nOutiliers fora dos limites IQR: \n {outliers_iqr}")
print(f"\nQuantidade de outliers fora dos limites IQR: {outliers_iqr.shape[0]}")

# Buscar outiers que estão entre o limite baixo e o limite alto
df_iqr = df[((df['idade'] >= limite_baixo) & (df['idade'] <= limite_alto))]
print(f"\nOutiliers dentro dos limites IQR: \n {df_iqr}")
print(f"\n Quantidade de outiliers dentro dos limites IQR: \n {df_iqr.shape[0]}")

# Criar um limite de idade
limite_baixo = 1
limite_alto = 100

new_df = df[((df['idade'] >= limite_baixo) & (df['idade'] <= limite_alto))]
print(f"\n DataFrame com idades entre 1 e 100 anos: \n {new_df}")
print(f"\n Quantidade de dados entre 1 e 100 anos: \n {new_df.shape[0]}")

# Filtrar endereços inválidos
df['endereco'] = df['endereco'].apply(lambda x: 'Endereço inválido' if len(x.split('\n')) < 3 else x) # Endereços com menos do que 3 linhas são alterados para endereço inválido
enderecos_invalidos = df[df['endereco'] == 'Endereço inválido']
print(f"\n DataFrame com endereços inválidos: \n {enderecos_invalidos}")
print(f"\n Quantidade de endereços inválidos: {enderecos_invalidos.shape[0]}")

# Filtrar campos de texto
df['nome'] = df['nome'].apply(lambda x: 'Nome inválido' if isinstance(x, str) and len(x) > 50 else x) # Nomes que não são string e que tem mais do que 50 caracteres para nome inválido
nomes_invalidos = df[df['nome'] == 'Nome inválido']
print(f"\nDataFrame com nomes inválidos: \n {nomes_invalidos}")
print(f"\nQuantidade de nomes inválidos: {nomes_invalidos.shape[0]}")

# DataFrame com outliers tratados
print(f"\nDados com outliers tratados: \n {df}")

# Salvar DataFrame
df.to_csv('clientes_remove_outliers.csv', index=False)