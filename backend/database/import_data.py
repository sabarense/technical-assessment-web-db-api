from backend.importers.import_operadoras import importar_operadoras
from backend.importers.import_demonstracoes import importar_demonstracoes_contabeis
from backend.database.connection import create_connection
import os

def main(csv_path):

    conn = create_connection()

    try:
        importar_operadoras(conn, csv_path)
        print("✅ Importação de operadoras concluída com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao importar operadoras: {str(e)}")

    try:
        pasta_contabeis = os.path.join("demonstracoes_contabeis")
        importar_demonstracoes_contabeis(conn, pasta_contabeis)
        print("✅ Importação de demonstrações concluída com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao importar demonstrações: {str(e)}")
