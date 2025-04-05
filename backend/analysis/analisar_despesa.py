import pandas as pd

def analisar_despesas(conn):
    ultimo_trimestre_inicio = '2025-01-01'
    ultimo_trimestre_fim = '2025-03-31'
    ultimo_ano_inicio = '2024-01-01'
    ultimo_ano_fim = '2024-12-31'

    try:
        print("\n🔍 Top 10 Operadoras - Último Trimestre (Q1 2025):")
        query_trimestre = """
        SELECT o.razao_social AS Operadora,
               SUM(d.vl_saldo_final) AS Despesas
        FROM demonstracoes_contabeis d
        JOIN operadoras_ativas o ON d.reg_ans = o.registro_ans
        WHERE d.descricao = ?
          AND d.data BETWEEN ? AND ?
        GROUP BY o.razao_social
        ORDER BY Despesas DESC
        LIMIT 10;
        """
        df_trimestre = pd.read_sql(query_trimestre, conn, params=[
            'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR',
            ultimo_trimestre_inicio,
            ultimo_trimestre_fim
        ])
        print(df_trimestre.to_markdown(index=False, floatfmt=",.2f") if not df_trimestre.empty else "Nenhum dado encontrado para o período")

        print("\n🔍 Top 10 Operadoras - Último Ano (2024):")
        query_ano = """
        SELECT o.razao_social AS Operadora,
               SUM(d.vl_saldo_final) AS Despesas
        FROM demonstracoes_contabeis d
        JOIN operadoras_ativas o ON d.reg_ans = o.registro_ans
        WHERE d.descricao = ?
          AND d.data BETWEEN ? AND ?
        GROUP BY o.razao_social
        ORDER BY Despesas DESC
        LIMIT 10;
        """
        df_ano = pd.read_sql(query_ano, conn, params=[
            'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR',
            ultimo_ano_inicio,
            ultimo_ano_fim
        ])
        print(df_ano.to_markdown(index=False, floatfmt=",.2f") if not df_ano.empty else "Nenhum dado encontrado para o período")

    except Exception as e:
        print(f"❌ Erro ao analisar despesas: {e}")
