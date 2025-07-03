# Projeto Power BI: Construção de Star Schema para Análise Financeira

## Visão Geral do Projeto

Este projeto demonstra a construção de um modelo de dados otimizado no Power BI, utilizando o padrão Star Schema, a partir de uma tabela de dados financeiros brutos (`financials_Table`). O objetivo é transformar dados transacionais complexos em um modelo mais intuitivo e performático para análises de negócios, relatórios e dashboards.

## Fonte de Dados

A base deste projeto é a `financials_Table`, uma tabela plana contendo diversas informações sobre vendas, lucros, produtos, segmentos, países e datas.

## Estrutura do Modelo de Dados (Star Schema)

O modelo final é um Star Schema composto por uma tabela de fatos central e várias tabelas de dimensão que fornecem contexto à esses fatos.

### 1. Tabela de Fatos: `F_Vendas`

A tabela `F_Vendas` (Fato de Vendas) contém as métricas numéricas principais (medidas) e as chaves estrangeiras que se conectam às tabelas de dimensão.

**Colunas:**
* `ID_Produto` (Chave Estrangeira para `D_Produtos` e `D_Produtos_Detalhes`)
* `ID_Desconto` (Chave Estrangeira para `D_Descontos`)
* `Date` (Chave Estrangeira para `D_Calendario`)
* `Segment` (Chave Estrangeira para `D_Detalhes`)
* `Country` (Chave Estrangeira para `D_Detalhes`)
* `Units Sold`
* `Sale Price`
* `Sales`
* `Profit`
* `COGS` (Custo dos Produtos Vendidos)

### 2. Tabelas de Dimensão

As tabelas de dimensão fornecem contexto descritivo aos dados da tabela de fatos.

* **`D_Produtos` (Dimensão Produto):** Descreve os produtos e suas características agregadas.
    * **Colunas:** `Produto`, `Média de Unidades Vendidas`, `Médias do valor de vendas`, `Valor máximo de Venda`, `Valor mínimo de Venda`.
    * **Chave Primária:** `Produto` (assumindo unicidade do nome do produto).

* **`D_Produtos_Detalhes` (Dimensão Detalhes do Produto):** Fornece detalhes mais granulares de produtos.
    * **Colunas:** `ID_produtos` (originalmente `Product`), `Discount Band`, `Sale Price`, `Units Sold`, `Manufacturing Price`.
    * **Chave Primária:** `ID_produtos`.

* **`D_Descontos` (Dimensão Descontos):** Contém informações sobre as faixas de desconto.
    * **Colunas:** `ID_Desconto` (chave substituta gerada), `Discount Band`.
    * **Chave Primária:** `ID_Desconto`.

* **`D_Detalhes` (Dimensão Detalhes Gerais):** Agrupa atributos contextuais como segmento e país.
    * **Colunas:** `Segment`, `Country`.
    * **Chaves:** `Segment` e `Country` (para relacionamentos múltiplos).

* **`D_Calendario` (Dimensão Calendário):** Fornece uma hierarquia de tempo robusta para análises temporais.
    * **Colunas:** `Date` (chave primária), `Ano`, `MesNumero`, `NomeMes`, `Trimestre`.

## Processo de Construção do Modelo

A construção do Star Schema foi realizada em duas fases principais: transformação de dados no Power Query (linguagem M) e modelagem/cálculos no Power BI Desktop (DAX).

### 1. Transformação de Dados no Power Query (Linguagem M)

1.  **Backup da Tabela Original:** A tabela `financials_Table` foi duplicada e renomeada para `Financials_origem`, sendo oculta no relatório para servir apenas como fonte de dados de backup.
2.  **Criação das Dimensões:**
    * Cada tabela de dimensão (`D_Produtos`, `D_Produtos_Detalhes`, `D_Descontos`, `D_Detalhes`) foi criada a partir de uma duplicação da `financials_Table` original.
    * **`D_Produtos`**: Colunas específicas foram selecionadas (`Product`, `Units Sold`, `Sales`, `Sale Price`), e a tabela foi agrupada por `Produto` para calcular médias e valores mínimos/máximos de vendas e unidades.
    * **`D_Produtos_Detalhes`**: Colunas relevantes (`Product`, `Discount Band`, `Sale Price`, `Units Sold`, `Manufacturing Price`) foram selecionadas, e duplicatas foram removidas para garantir unicidade da combinação de detalhes. `Product` foi renomeado para `ID_produtos`.
    * **`D_Descontos`**: Esta dimensão foi crucial. Inicialmente, a coluna `Discount Band` continha duplicatas, impedindo um relacionamento eficaz. A solução foi **remover todas as colunas exceto `Discount Band`**, **remover duplicatas** da `Discount Band` restante e, em seguida, **adicionar uma "Coluna de Índice" (`Table.AddIndexColumn`)** para criar uma Chave Substituta (`ID_Desconto`).
    * **`D_Detalhes`**: `Segment` e `Country` foram selecionadas, e duplicatas foram removidas para criar uma lista única de combinações de segmento/país.
3.  **Criação da Tabela de Fatos (`F_Vendas`):**
    * A `F_Vendas` foi criada duplicando a `financials_Table` e selecionando apenas as colunas de medidas e as chaves naturais/estrangeiras necessárias para os relacionamentos com as dimensões (`Product`, `Units Sold`, `Sale Price`, `Discount Band`, `Segment`, `Country`, `Sales`, `Profit`, `Date`). `Product` foi renomeado para `ID_Produto`.
    * **Integração da Chave Substituta (`ID_Desconto`):** Para conectar `F_Vendas` à `D_Descontos` usando a chave substituta, foi realizada uma operação de **"Mesclar Consultas" (`Table.NestedJoin`)** na `F_Vendas`. A `F_Vendas` foi mesclada com a `D_Descontos` usando `Discount Band` como chave de junção, e apenas a coluna `ID_Desconto` foi expandida para a `F_Vendas`. A coluna `Discount Band` original na `F_Vendas` foi então removida.

### 2. Modelagem e Cálculos no Power BI Desktop (DAX)

1.  **Criação da Dimensão Calendário (`D_Calendario`):**
    * A `D_Calendario` foi criada usando a função DAX `CALENDAR(MIN(F_Vendas[Date]), MAX(F_Vendas[Date]))` para garantir que ela abrangesse todo o período de dados transacionais.
    * Colunas de tempo adicionais (`Ano`, `MesNumero`, `NomeMes`, `Trimestre`) foram criadas usando funções DAX como `YEAR()`, `MONTH()`, `FORMAT()`.
    * A tabela `D_Calendario` foi marcada como "Tabela de Data" para otimização de tempo.
2.  **Criação de Medidas DAX:**
    * Medidas explícitas foram criadas na tabela `F_Vendas` para facilitar a análise e garantir cálculos corretos.
    * `Mediana Valor Vendas = MEDIAN(F_Vendas[Sales])` (resolvendo o desafio de calcular a mediana que não era possível no Power Query).
    * `Total de Vendas = SUM(F_Vendas[Sales])`
    * `Lucro Total = SUM(F_Vendas[Profit])`
    * `Unidades Vendidas Total = SUM(F_Vendas[Units Sold])`
3.  **Estabelecimento de Relacionamentos (Star Schema):**
    * Todos os relacionamentos entre a `F_Vendas` e as dimensões foram configurados na visão de Modelo do Power BI.
    * **Cardinalidade:** Todos os relacionamentos são do tipo "Muitos para Um" (`*` para `1`).
    * **Direção do Filtro Cruzado:** "Única" (das dimensões para a tabela de fatos).
    * Os relacionamentos estabelecidos foram:
        * `F_Vendas[ID_Produto]` <-> `D_Produtos[Produto]`
        * `F_Vendas[ID_Produto]` <-> `D_Produtos_Detalhes[ID_produtos]`
        * `F_Vendas[ID_Desconto]` <-> `D_Descontos[ID_Desconto]`
        * `F_Vendas[Segment]` <-> `D_Detalhes[Segment]`
        * `F_Vendas[Country]` <-> `D_Detalhes[Country]`
        * `F_Vendas[Date]` <-> `D_Calendario[Date]`

## Diagrama do Star Schema

Abaixo está o diagrama do modelo de dados Star Schema construído:

![Diagrama Star Schema](Star_Schema_Diagram.png)

## Desafios Enfrentados e Soluções

* **Unicidade da Chave da Dimensão (`D_Descontos`):** Inicialmente, a coluna `Discount Band` na `D_Descontos` continha valores duplicados ("None"), impedindo um relacionamento Many-to-One. A solução foi refatorar a `D_Descontos` para conter apenas valores únicos de `Discount Band` e, crucialmente, gerar uma **Chave Substituta numérica (`ID_Desconto`)**. Esta chave foi então mesclada na `F_Vendas` para estabelecer um relacionamento robusto e performático. Este ponto reforça a importância das Surrogate Keys em modelos de dados relacionais.
* **Erro na Medida DAX (`MEDIAN`):** Um erro de "coluna não encontrada" ao criar a medida `Mediana Valor Vendas` foi depurado. A verificação do nome exato da coluna e do tipo de dado no Power Query foi fundamental para a resolução, garantindo que a referência DAX estivesse correta.

## Conclusão e Aprendizados

Este projeto solidificou o entendimento sobre os princípios do Star Schema, a importância da modelagem dimensional e as capacidades de transformação e cálculo do Power BI. A experiência prática com o Power Query M para a preparação de dados, a criação de chaves substitutas e o uso do DAX para medidas e dimensões de tempo foram aprendizados valiosos, preparando o terreno para projetos de BI mais complexos e eficientes.

## Como Usar o Projeto

1.  Faça o download do arquivo `Desafio_Star_Schema.pbix`.
2.  Abra-o no Power BI Desktop.
3.  Explore o modelo de dados na "Visão de Modelo" e os dados nas "Visão de Dados".
4.  As medidas criadas podem ser utilizadas em relatórios para analisar as vendas por diferentes dimensões (Produto, Tempo, Desconto, Detalhes Geográficos/Segmento).

---

**Autor:** RANNYER GABRIEL DE OLIVEIRA
