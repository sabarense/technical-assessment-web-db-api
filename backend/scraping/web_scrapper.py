import requests
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile


def baixar_arquivos(file_links, download_folder):
    downloaded_files = []

    for file_link in file_links:
        if not file_link.startswith('http'):
            file_link = f"https://www.gov.br{file_link}"

        file_name = file_link.split('/')[-1]
        file_path = os.path.join(download_folder, file_name)

        try:
            response = requests.get(file_link, timeout=10)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
            downloaded_files.append(file_path)
            print(f"Arquivo {file_name} baixado em: {file_path}")
        except Exception as e:
            print(f"Erro ao baixar {file_name}: {str(e)}")

    return downloaded_files


def compactar_arquivos(downloaded_files, zip_path):
    try:
        with ZipFile(zip_path, 'w') as zipf:
            for file_path in downloaded_files:
                zipf.write(file_path, os.path.basename(file_path))
        print(f"Compactação concluída: {zip_path}")
        return True
    except Exception as e:
        print(f"Erro na compactação: {str(e)}")
        return False


def limpar_arquivos(downloaded_files):
    for file_path in downloaded_files:
        try:
            os.remove(file_path)
            print(f"Arquivo {file_path} removido")
        except Exception as e:
            print(f"Erro ao remover {file_path}: {str(e)}")


def main(download_folder):
    page_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

    zip_path = os.path.join(download_folder, "anexos_compactados.zip")

    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        file_links = [
            link['href'] for link in soup.find_all('a', href=True)
            if ("Anexo_I" in link['href'] or "Anexo_II" in link['href'])
               and link['href'].endswith(".pdf")
        ]

        if not file_links:
            print("Nenhum PDF encontrado.")
            return

        downloaded_files = baixar_arquivos(file_links, download_folder)

        if compactar_arquivos(downloaded_files, zip_path):
            limpar_arquivos(downloaded_files)

    except Exception as e:
        print(f"Erro no processo: {str(e)}")
