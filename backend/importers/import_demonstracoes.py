import os
import pandas as pd
from backend.utils.file_utils import extract_pdf_from_zip


def importar_demonstracoes_contabeis(conn, pasta_contabeis="demonstracoes_contabeis"):
    extract_pdf_from_zip(pasta_contabeis)
    if not os.path.exists(pasta_contabeis):
        print(f"❌ Pasta não encontrada: {pasta_contabeis}")
        return

    arquivos = [f for f in os.listdir(pasta_contabeis) if f.endswith(".csv")]
    for arquivo in arquivos:
        try:
            caminho_arquivo = os.path.join(pasta_contabeis, arquivo)
            df = pd.read_csv(caminho_arquivo, encoding="utf-8", delimiter=";", on_bad_lines='skip', dtype=str)
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df.columns = df.columns.str.lower().str.replace(r'__\d+$', '', regex=True)

            df['reg_ans'] = df['reg_ans'].str.zfill(6)
            df['cd_conta_contabil'] = pd.to_numeric(df['cd_conta_contabil'], errors='coerce').fillna(0).astype(int)
            df['vl_saldo_inicial'] = pd.to_numeric(df['vl_saldo_inicial'], errors='coerce')
            df['vl_saldo_final'] = pd.to_numeric(df['vl_saldo_final'], errors='coerce')
            df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.strftime('%Y-%m-%d')

            valid_ans = pd.read_sql("SELECT registro_ans FROM operadoras_ativas", conn)['registro_ans']
            df = df[df['reg_ans'].isin(valid_ans)]

            with conn:
                df.to_sql("demonstracoes_contabeis", conn, if_exists="append", index=False, dtype={'reg_ans': 'TEXT'})
            print(f"✅ {arquivo} importado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao importar {arquivo}: {e}")