import os
from backend.scraping.web_scrapper import main as web_scraping_main
from backend.transformation.data_transformation import main as data_transformation_main
from backend.database.import_data import main as import_data_main

def main():
    """
    Pipeline: executa scraping, transformação de dados e importação no banco.
    """
    print("=" * 60)
    print("INICIANDO PIPELINE DE PROCESSAMENTO E IMPORTAÇÃO")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    downloads_dir = os.path.join(data_dir, 'downloads')
    processed_dir = os.path.join(data_dir, 'processed')

    os.makedirs(downloads_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    print("\n[ETAPA 1] Web Scraping para baixar anexos...")
    web_scraping_main(downloads_dir)

    zip_file_path = os.path.join(downloads_dir, "anexos_compactados.zip")
    if not os.path.exists(zip_file_path):
        print(f"❌ ERRO: ZIP não encontrado em {zip_file_path}")
        return
    print(f"✅ Anexos baixados e compactados em: {zip_file_path}")

    print("\n[ETAPA 2] Processamento e transformação do PDF...")
    data_transformation_main(zip_file_path, processed_dir)

    csv_path = os.path.join(processed_dir, "Rol_Procedimentos.csv")
    final_zip_path = os.path.join(processed_dir, "Rol_Procedimentos_Final.zip")

    if not os.path.exists(csv_path):
        print(f"❌ AVISO: CSV não foi gerado em {csv_path}")
        return

    print(f"✅ Dados transformados e salvos em CSV: {csv_path}")

    print("\n[ETAPA 3] Importando dados para o banco de dados...")
    try:
        import_data_main(csv_path)
        print("✅ Importação concluída com sucesso!")
    except Exception as e:
        print(f"❌ ERRO durante a importação para o banco: {str(e)}")
        return

    if os.path.exists(final_zip_path):
        print("\n🎉 PROCESSO FINALIZADO COM SUCESSO!")
        print(f"📁 Arquivo final compactado disponível em: {final_zip_path}")
    else:
        print("⚠️ Arquivo ZIP final não foi localizado.")

    print("=" * 60)

if __name__ == "__main__":
    main()
