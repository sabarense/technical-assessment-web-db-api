import os
import pandas as pd

def importar_operadoras(conn, pasta_operadoras="data/processed"):
    arquivo = os.path.join(pasta_operadoras, "Relatorio_cadop.csv")

    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return
    try:
        df = pd.read_csv(arquivo, encoding="utf-8", delimiter=";", on_bad_lines='skip', dtype=str)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df.columns = df.columns.str.lower().str.replace(r'__\d+$', '', regex=True)

        df['registro_ans'] = df['registro_ans'].str.zfill(6)
        df['cnpj'] = df['cnpj'].str.zfill(14)
        df['uf'] = df['uf'].str.upper().str[:2]
        df['cep'] = df['cep'].str.replace(r"\D", "", regex=True).str.zfill(8)
        df['ddd'] = df['ddd'].str.zfill(4)
        df['data_registro_ans'] = pd.to_datetime(df['data_registro_ans'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['regiao_de_comercializacao'] = pd.to_numeric(df['regiao_de_comercializacao'], errors='coerce').fillna(0).astype(int)

        with conn:
            df.to_sql("operadoras_ativas", conn, if_exists="append", index=False, dtype={'registro_ans': 'TEXT'})
        print("✅ Operadoras importadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao importar operadoras: {e}")
