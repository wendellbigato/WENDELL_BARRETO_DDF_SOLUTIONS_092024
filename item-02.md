## Item 02 | Implementação do Carregamento e Análise Descritiva de Dados

Este notebook foi desenvolvido para realizar o carregamento, a limpeza e a análise descritiva de um dataset de produtos, disponível no site informado. Seguindo as boas práticas de Data Engineering, ele faz o seguinte:

### Passos Realizados

### 1. Carregamento do Dataset
O dataset foi carregado diretamente da Hugging Face usando a biblioteca `datasets`. O nome do dataset utilizado foi `spacemanidol/product-search-corpus` na divisão `train`. 

Aqui está o código utilizado para carregar o dataset:

```python
from datasets import load_dataset

# Nome do dataset no Hugging Face
dataset_name = "spacemanidol/product-search-corpus"
split = "train"  # Divisão do dataset

# Carregar o dataset
dataset = load_dataset(dataset_name, split=split)
```

### 2. Análise Preliminar
Em seguida, foi realizada uma análise inicial para verificar a integridade dos dados, como campos vazios ou ausentes, dentro de um número limitado de linhas (100):

```python
# Visualizar as primeiras linhas do dataset
num_linhas = 100  # Número de linhas a serem lidas para análise inicial
df_inicial = dataset.to_pandas().head(num_linhas)

# Exibir uma amostra
df_inicial.head()
```

Esta etapa garantiu que o dataset carregado estava correto e que todos os campos essenciais estavam presentes.

### 3. Filtragem de Linhas Válidas
Foi aplicada uma filtragem para garantir que os campos críticos, como `text` e `title`, não estivessem vazios. O código abaixo identifica as linhas válidas e as salva em um arquivo CSV. 

Linhas válidas são aquelas em que tanto o título quanto o texto não estão vazios:

```python
# Filtrar linhas onde 'text' e 'title' não estão vazios
linhas_validas = (df_inicial['text'] != '') & (df_inicial['title'] != '')

# Separar as linhas válidas
df_validas = df_inicial[linhas_validas]

# Salvar o DataFrame de linhas válidas em um arquivo CSV
output_csv_validas = "dataset/linhas_validas.csv"
df_validas.to_csv(output_csv_validas, index=False)

print(f"Arquivo {output_csv_validas} criado com {len(df_validas)} linhas válidas.")
```

### 4. Salvando as Linhas Inválidas
Além disso, as linhas inválidas (aquelas que tinham campos vazios) também foram identificadas e seus IDs foram salvos separadamente para análise posterior:

```python
# Identificar as linhas excluídas (linhas inválidas)
df_excluidas = df_inicial[~linhas_validas]

# Salvar os IDs das linhas excluídas
output_csv_excluidas = "dataset/linhas_excluidas.csv"
df_excluidas[['docid']].to_csv(output_csv_excluidas, index=False)

print(f"Arquivo {output_csv_excluidas} criado com {len(df_excluidas)} IDs de linhas excluídas.")
```

### Conclusão

Esse processo de limpeza e validação garante que os dados estejam prontos para análises mais avançadas e, eventualmente, para modelagem de machine learning. 

