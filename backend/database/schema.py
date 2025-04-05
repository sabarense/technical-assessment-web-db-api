def criar_tabelas(conn):
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE operadoras_ativas (
        registro_ans TEXT PRIMARY KEY,
        cnpj TEXT,
        razao_social TEXT,
        nome_fantasia TEXT,
        modalidade TEXT,
        logradouro TEXT,
        numero TEXT,
        complemento TEXT,
        bairro TEXT,
        cidade TEXT,
        uf TEXT,
        cep TEXT,
        ddd TEXT,
        telefone TEXT,
        fax TEXT,
        endereco_eletronico TEXT,
        representante TEXT,
        cargo_representante TEXT,
        regiao_de_comercializacao INTEGER,
        data_registro_ans TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE demonstracoes_contabeis (
        data TEXT,
        reg_ans TEXT,
        cd_conta_contabil INTEGER,
        descricao TEXT,
        vl_saldo_inicial REAL,
        vl_saldo_final REAL,
        PRIMARY KEY (data, reg_ans, cd_conta_contabil),
        FOREIGN KEY (reg_ans) REFERENCES operadoras_ativas (registro_ans)
    );
    ''')

    conn.commit()
