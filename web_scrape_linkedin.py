import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def main():
    find_linkedin()


def find_linkedin():
    while True:
        key_word = input("Informe a vaga de tecnologia desejada: ")
        base_url = f"https://www.linkedin.com/jobs/search/?keywords={key_word}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=2&position=1&pageNum=0"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }

        page = requests.get(base_url, headers=headers)

        soup = soup_result(page)
        elements = soup.findAll("div", class_="filter-values-container__filter-value")

        jobs_data = []

        for element in elements:
            text = element.text.strip()
            # Usando expressão regular para extrair tipo de trabalho e contagem
            match = re.match(r'(.+)\s\((\d+)\)', text)
            if match:
                job_title = match.group(1).strip()
                job_count = match.group(2).strip()
                jobs_data.append([job_title, job_count])

        df = pd.DataFrame(jobs_data, columns=["Categoria", "Número de Vaga"])
        print(df)

        df.to_csv("web_scrape_linkedin.csv")

        sair = input("Digite 'q' para sair da aplicação: ")
        if sair.lower() == 'q':
            print("Saindo da aplicação...")
            break


def soup_result(page):
    soup = BeautifulSoup(page.text, "html.parser")
    return soup


if __name__ == "__main__":
    main()