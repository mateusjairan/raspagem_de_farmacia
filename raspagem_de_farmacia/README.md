# Raspador de Dados da Pague Menos por EAN

Este projeto utiliza Python e Selenium para automatizar a coleta de dados de produtos no site da farmácia Pague Menos. O script lê uma lista de códigos de barras (EANs) de um arquivo de texto, busca cada produto no site, extrai as informações relevantes e salva os dados em um arquivo CSV.

## Funcionalidades

- **Leitura de EANs em Lote**: Lê uma lista de códigos de barras a partir de um arquivo `eans.txt`.
- **Automação Web**: Utiliza Selenium para abrir o navegador, navegar até a página de busca de cada produto e carregar o conteúdo dinâmico.
- **Extração de Dados Inteligente**: Em vez de depender de seletores CSS frágeis, o script analisa o JSON embutido na página (tag `__STATE__`), garantindo uma coleta de dados mais robusta e precisa.
- **Dados Coletados**: Extrai o EAN, o nome (`name`) e o preço (`price`) de cada produto.
- **Tratamento de Erros**: Lida com casos em que um produto não é encontrado, registrando-o no CSV para posterior verificação.
- **Modo Headless**: Pode ser configurado para rodar em segundo plano, sem abrir uma janela visível do navegador.
- **Exportação para CSV**: Salva todos os dados coletados em um arquivo `produtos_paguemenos.csv`, pronto para ser utilizado em planilhas ou outras análises.

## Pré-requisitos

- Python 3.x
- Google Chrome instalado

## Instalação e Configuração

1.  **Clone o repositório ou baixe os arquivos do projeto.**

2.  **Crie e ative um ambiente virtual (Recomendado):**

    ```bash
    # No Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # No macOS/Linux
    # python3 -m venv .venv
    # source .venv/bin/activate
    ```

3.  **Instale as dependências necessárias:**

    ```bash
    pip install selenium beautifulsoup4 webdriver-manager
    ```

## Como Usar

1.  **Prepare a lista de EANs**: Abra o arquivo `eans.txt` e adicione os códigos de barras que você deseja pesquisar, colocando um código por linha.

2.  **Execute o script**: Com o ambiente virtual ativado, execute o script principal no seu terminal.

    ```bash
    python scraper_paguemenos.py
    ```

O script iniciará o navegador, percorrerá cada EAN da lista, buscará os dados e imprimirá o progresso no terminal.

## Saída

Ao final da execução, um arquivo chamado `produtos_paguemenos.csv` será criado no mesmo diretório, contendo os dados dos produtos encontrados. O arquivo terá o seguinte formato:

```csv
ean,name,price
7908324405125,Shampoo Ox Mari Maria Hair Vita Glow 240ml,26.99
7891066006749,Desodorante Aerosol Nivea Men Deep 150ml,17.99
1234567890123,NAO_ENCONTRADO,NAO_ENCONTRADO
