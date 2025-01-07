import pandas as pd

# Função para calcular o cubo de um número

def cubo(x):
    return x ** 3

# Expressão de lambda para calcular o cubo de um número
cubo_lambda = lambda x: x ** 3 # Cria uma função em uma linha

print(f"Função cubo: {cubo(2)}")
print(f"\nFunção cubo lambda: {cubo_lambda(2)}")

df = pd.DataFrame({'numeros': [1, 2, 3, 4, 5, 20]})

df['cubo_funcao'] = df['numeros'].apply(cubo) # Precisa criar a função antes
df['cubo_lambda'] = df['numeros'].apply(lambda x: x ** 3) # Função criada no momento do apply, bom para operações simples
print(df)