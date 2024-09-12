## Item 03 | Implementação de Features com LLM e Langchain

Neste item, utilizamos um **Large Language Model (LLM)**, configurado com a biblioteca **Langchain**, para criar features a partir das colunas de texto do dataset de produtos. A Langchain foi aplicada para estruturar o processo de extração e validação das features de maneira robusta, garantindo que os dados seguissem um formato JSON padronizado e consistente.

### Passos Realizados

### 1. Configuração do Cliente OpenAI

O primeiro passo foi configurar o cliente da OpenAI usando o modelo **GPT-3.5-turbo** com uma temperatura de **0.7** para controlar o grau de criatividade nas respostas geradas pelo LLM. A temperatura define o nível de variação e criatividade das respostas, com **0.7** sendo um valor moderado para balancear consistência e variedade nas extrações.

```python
# Configurar o cliente OpenAI corretamente
client = ChatOpenAI(
    api_key=api_key,
    model="gpt-3.5-turbo",
    temperature=0.7
)
```

### 2. Definição do Esquema JSON para Saída

Para garantir a consistência dos dados extraídos, definimos um **esquema JSON** que especifica como as features do produto devem ser organizadas. Esse esquema é estruturado em torno de sete componentes principais:

- **product_summary**: Um nome simplificado e resumido do produto.
- **category**: A categoria do produto, descrita em uma única palavra.
- **material**: O material predominante do produto.
- **functions**: As principais funcionalidades do produto, representadas por até três palavras.
- **compatibility**: A compatibilidade do produto com outros itens.
- **price**: Um valor estimado do preço do produto em dólares americanos.
- **other_details**: Outros detalhes relevantes que não se enquadram nas categorias anteriores.

O esquema JSON foi configurado utilizando o **Langchain** para garantir que as respostas do LLM sigam o formato correto:

```python
# Definir o esquema do JSON esperado como saída
response_schemas = [
    ResponseSchema(name="product_summary", description="Um nome simplificado e resumido do produto."),
    ResponseSchema(name="category", description="A categoria do produto em uma palavra."),
    ResponseSchema(name="material", description="O material predominante do produto em uma palavra."),
    ResponseSchema(name="functions", description="As funções principais do produto, escritas de forma consistente para produtos similares."),
    ResponseSchema(name="compatibility", description="A compatibilidade do produto com outros itens, se aplicável."),
    ResponseSchema(name="price", description="Um valor estimado numérico no formato inteiro."),
    ResponseSchema(name="other_details", description="Outros detalhes relevantes do produto.")
]
```

### 3. Validação da Saída com Langchain

Usamos o **Langchain** para criar um **parser estruturado** que valida as respostas geradas pelo LLM. Esse parser garante que o JSON retornado siga o formato definido no esquema acima. Ele também facilita o tratamento de erros no caso de respostas malformadas, garantindo a consistência do output.

```python
# Criar um parser com LangChain para validar o formato de saída
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
```

### 4. Função para Extrair Features com LLM e Validar com Langchain

A função `extrair_features_com_parser` utiliza o modelo da OpenAI para processar o título e a descrição de cada produto e retornar as features no formato JSON. Aqui, um **template de prompt** é utilizado para estruturar as perguntas feitas ao LLM, garantindo que as respostas sejam coerentes e sigam as regras estabelecidas (como restringir cada valor a uma única palavra).

Além disso, o **output_parser** garante que o formato JSON gerado esteja de acordo com o esquema definido.

```python
def extrair_features_com_parser(titulo, descricao):
    prompt_template = """
    Titulo: {titulo}
    Descrição do Produto: {descricao}
    
    Quais são as principais features do produto? Resuma as informações abaixo em um formato JSON com as seguintes diretrizes:
    - Simplifique o nome do produto.
    - Cada feature deve ser descrita com uma única palavra.
    - Descreva cada categoria com uma única palavra. Exemplo "category" : "mobile"
    - Produtos similares devem ter descrições consistentes de funções (exemplo: use termos similares para slots, suportes, etc.).
    - Para o material, se houver mais de um, selecione o material que mais representa o produto.
    - Estime um valor para o preço do produto em dólares americanos.
    - As funções principais do produto devem ser brevemente descritas com uma palavra apenas.
    - Inclua outros detalhes relevantes sobre o produto com uma palavra.
    - Cada valor no esquema abaixo deve ter apenas uma palavra.

    O formato do JSON deve ser o seguinte:
    {{
        "product_summary": "...",
        "category": "...",
        "material": "...",
        "functions": {{
            "main_function": "...",
            "additional_function_1": "...",
            "additional_function_2": "..."
        }},
        "compatibility": "...",
        "price": int,
        "other_details": "..."
    }}
    """

    # Substituir as variáveis no prompt
    prompt = prompt_template.format(titulo=titulo, descricao=descricao)

    # Chamar o LLM usando a função invoke corretamente
    response = client.invoke(
        input=[
            {"role": "system", "content": "Você é um assistente que extrai características de descrições de produtos."},
            {"role": "user", "content": prompt}
        ]
    )

    # Validar o formato da resposta usando o output_parser
    try:
        parsed_response = output_parser.parse(response.content.strip())
        return parsed_response
    except Exception as e:
        print(f"Erro ao validar o formato JSON: {e}")
        return None
```

### 5. Aplicação do Processo de Extração e Salvamento dos Dados

A função de extração de features é aplicada a todas as linhas do dataset, processando as colunas de `title` e `description` para gerar as features. Os resultados são armazenados em uma nova coluna do DataFrame (`features`) e, posteriormente, salvos em um arquivo JSON.

```python
# Carregar o CSV "linhas_validas.csv"
df = pd.read_csv("dataset/linhas_validas.csv")

# Aplicar a extração de características com o parser
df['features'] = df.apply(lambda row: extrair_features_com_parser(row['title'], row['text']), axis=1)

# Manter todas as features como um dicionário em uma única coluna
df['features'] = df['features'].apply(lambda x: json.dumps(x) if x is not None else '{}')

# Salvar o DataFrame atualizado em um novo arquivo JSON
output_json = "dataset/linhas_validas_com_features.json"
df.to_json(output_json, orient='records', lines=True)

print(f"Arquivo JSON '{output_json}' salvo com sucesso com as features em uma única coluna no formato dicionário.")
```

### 6. Exemplo de JSON Gerado

Aqui está um exemplo de como as features são armazenadas no arquivo JSON final:

```json
"features":{
  \"product_summary\": \"Leather Case\",
  \"category\": \"mobile\",
  \"material\": \"Leather\",
  \"functions\": {
    \"main_function\": \"Protection\",
    \"additional_function_1\": \"Mirror\",
    \"additional_function_2\": \"CardSlots\"
  },
  \"compatibility\": \"Samsung Galaxy S8 Plus\",
  \"price\": 25,
  \"other_details\": \"RFID Blocking\"
}
```

### 7. Integração e Orquestração da Pipeline

Essa função faz parte de uma **pipeline** integrada que envolve as seguintes etapas:

1. **Carregamento dos Dados**: O CSV contendo os produtos é carregado no início da pipeline.
2. **Extração das Features**: Utilizamos o LLM com o suporte da **Langchain** para garantir a consistência do JSON gerado.
3. **Salvamento dos Dados**: As features extraídas são salvas em um arquivo JSON, pronto para importação.

Essa pipeline garante que o processo seja escalável e automatizado, facilitando a geração e validação de dados em larga escala.

### Observação

A importação do dataset foi ilustrativa e baseada na documentação [Dadosfera Import API](https://docs.dadosfera.ai/docs/import-data-api-enterprise-only). O script de importação no notebook `03-import` não foi testado diretamente, mas os notebooks anteriores funcionaram corretamente e geraram os dados manualmente importados para a continuação do teste.
