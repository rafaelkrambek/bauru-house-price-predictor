# Importa o undetected_chromedriver para evitar bloqueios de bot durante o scraping
import undetected_chromedriver as uc

# Importa o By do Selenium para localizar elementos na página
from selenium.webdriver.common.by import By

# Importa pandas para criar e manipular o DataFrame
import pandas as pd

# Importa o sleep para pausar o código se necessário (não utilizado no script atual)
from time import sleep

# Configurações do navegador Chrome
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')  # Evita problemas de permissão no Linux
options.add_argument('--disable-dev-shm-usage')  # Evita travamentos em ambientes com pouca memória compartilhada

# Inicializa o driver do Chrome com as opções configuradas
driver = uc.Chrome(options=options)

# Dicionário e listas para armazenar os dados coletados
dados = {}
precos_list = []
bairros_list = []
m2_list = []
quartos_list = []
banheiros_list = []
vagas_list = []

# Loop para percorrer 150 páginas do site do ImovelWeb para a cidade de Bauru
for i in range(150):
    driver.get(f'https://www.imovelweb.com.br/casas-venda-pagina-{i}-q-bauru.html')
    
    # Encontra todos os cards de imóveis na página
    cards = driver.find_elements(By.XPATH, "//*[contains(@class, 'postingCard-module__posting-top')]")
    
    # Loop para cada card de imóvel
    for card in cards:
        # Coleta o preço
        precos = card.find_elements(By.XPATH, ".//*[contains(@data-qa, 'POSTING_CARD_PRICE')]")
        
        # Coleta o bairro
        bairros = card.find_elements(By.XPATH,".//*[contains(@data-qa, 'POSTING_CARD_LOCATION')]")
        
        # Coleta características como m², quartos, banheiros, vagas
        caracteristicas = card.find_elements(By.XPATH,".//*[contains(@class, 'postingMainFeatures-module__posting-main-features-span postingMainFeatures-module__posting-main-features-listing')]")
        
        # Inicializa as variáveis com valores vazios caso algum dado não esteja presente no card
        m2 = quartos = banheiros = vagas = ""
        
        # Para cada preço encontrado, adiciona na lista
        for preco in precos:
            precos_list.append(preco.text)
        
        # Para cada bairro encontrado, adiciona na lista
        for bairro in bairros:
            bairros_list.append(bairro.text)
        
        # Para cada característica, identifica o que é (m², quartos, banheiros ou vagas) e armazena na variável correta
        for carac in caracteristicas:    
            if 'm²' in carac.text:
                m2 = carac.text
            elif 'quarto' in carac.text:
                quartos = carac.text
            elif 'ban' in carac.text:
                banheiros = carac.text
            elif 'vaga' in carac.text:
                vagas = carac.text
        
        # Adiciona os dados coletados nas listas respectivas
        m2_list.append(m2)
        quartos_list.append(quartos)
        banheiros_list.append(banheiros)
        vagas_list.append(vagas)        

# Imprime o tamanho das listas para conferência
print(len(m2_list))
print(len(quartos_list))
print(len(banheiros_list))
print(len(vagas_list))

# Monta o dicionário final com todas as listas de dados
dados['precos'] = precos_list
dados['bairros'] = bairros_list
dados['tamanhos'] = m2_list
dados['quartos'] = quartos_list
dados['banheiros'] = banheiros_list
dados['vagas'] = vagas_list

# Cria o DataFrame com pandas
df = pd.DataFrame(dados)

# Exporta o DataFrame para CSV
df.to_csv('Imoves.csv')

# Encerra o navegador
driver.quit()