import csv
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configurações ---
EAN_LIST_FILE = 'eans.txt'
OUTPUT_CSV_FILE = 'produtos_paguemenos.csv'
BASE_URL = 'https://www.paguemenos.com.br/busca?termo='

def setup_driver():
    """Configura e retorna uma instância do WebDriver do Chrome."""
    print("Configurando o WebDriver...")
    options = webdriver.ChromeOptions()
    # Para rodar sem abrir uma janela do navegador, descomente a linha abaixo
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    # Altera a estratégia de carregamento da página.
    # 'eager' faz com que o Selenium não espere por todos os recursos (como imagens e CSS)
    # para terminar de carregar, retornando o controle mais cedo e evitando timeouts.
    # O 'WebDriverWait' no script já garante que vamos esperar pelo elemento específico que precisamos.
    options.page_load_strategy = 'eager'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver configurado com sucesso.")
    return driver

def scrape_product_data(driver, ean: str) -> dict | None:
    """
    Navega até a página do produto usando o EAN e extrai os dados das tags HTML.
    """
    url = BASE_URL + ean
    driver.get(url)
    
    try:
        # Espera até que o nome do produto esteja presente na página.
        # Isso garante que a página carregou o suficiente para o scraping.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.paguemenos-store-theme-7-x-productName"))
        )
        
        # Pequena pausa para garantir que todos os scripts renderizaram.
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extrair o nome do produto
        name_element = soup.find('h2', class_='paguemenos-store-theme-7-x-productName')
        if not name_element:
            print(f"  -> Nome do produto não encontrado para o EAN {ean}.")
            return None
        name = name_element.get_text(strip=True)

        # Extrair o preço do produto
        price_element = soup.find('div', class_='paguemenos-store-theme-7-x-price')
        if not price_element:
            print(f"  -> Preço do produto não encontrado para o EAN {ean}.")
            return None
            
        price_text = price_element.get_text(strip=True)
        # Limpa o texto do preço: 'R$ 37,99' -> '37.99'
        cleaned_price = price_text.replace('R$', '').replace('\xa0', '').strip().replace(',', '.')
        price = float(cleaned_price)

        return {
            'ean': ean,
            'name': name,
            'price': price
        }

    except Exception as e:
        print(f"  -> Ocorreu um erro ao raspar dados para o EAN {ean}: {e}")
        return None

def main():
    """
    Função principal que orquestra a leitura dos EANs, a raspagem dos dados
    e a escrita no arquivo CSV.
    """
    try:
        with open(EAN_LIST_FILE, 'r', encoding='utf-8') as f:
            eans = [line.strip() for line in f if line.strip()]
        if not eans:
            print(f"O arquivo '{EAN_LIST_FILE}' está vazio. Adicione os códigos de barras (EANs) para continuar.")
            return
    except FileNotFoundError:
        print(f"Erro: Arquivo '{EAN_LIST_FILE}' não encontrado.")
        print("Por favor, crie este arquivo e adicione um código de barras (EAN) por linha.")
        # Cria um arquivo de exemplo para o usuário
        with open(EAN_LIST_FILE, 'w', encoding='utf-8') as f:
            f.write("7908324405125\n")
            f.write("7891066006749\n") # EAN de exemplo para um produto diferente
            f.write("1234567890123\n") # EAN de exemplo que não será encontrado
        print(f"Um arquivo de exemplo '{EAN_LIST_FILE}' foi criado para você.")
        return

    driver = setup_driver()
    all_products_data = []

    print(f"\nIniciando a raspagem de {len(eans)} produto(s)...")

    for ean in eans:
        print(f"Buscando dados para o EAN: {ean}")
        product_data = scrape_product_data(driver, ean)
        if product_data:
            print(f"  -> Produto encontrado: {product_data['name']}")
            all_products_data.append(product_data)
        else:
            print(f"  -> Nenhum produto encontrado para o EAN {ean}.")
            # Adiciona uma linha ao CSV para indicar que a busca falhou
            all_products_data.append({'ean': ean, 'name': 'NAO_ENCONTRADO', 'price': 'NAO_ENCONTRADO'})

    driver.quit()

    if not all_products_data:
        print("Nenhum dado de produto foi coletado.")
        return

    print(f"\nRaspagem concluída. Escrevendo {len(all_products_data)} linha(s) no arquivo '{OUTPUT_CSV_FILE}'...")
    
    try:
        colunas = ['ean', 'name', 'price']
        with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            writer.writeheader()
            writer.writerows(all_products_data)
        print("Dados salvos com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo CSV: {e}")

if __name__ == '__main__':
    main()
