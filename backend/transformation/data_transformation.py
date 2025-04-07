import os
import zipfile
import pandas as pd
import pdfplumber
from backend.utils.file_utils import extract_pdf_from_zip

def process_pdf_to_dataframe(pdf_path):
    dfs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                dfs.append(df)

    if not dfs:
        raise ValueError("Nenhuma tabela encontrada no PDF")

    full_df = pd.concat(dfs, ignore_index=True)

    full_df.columns = [
        'PROCEDIMENTO', 'RN', 'VIGÊNCIA', 'Seg. Odontológico',
        'Seg. Ambulatorial', 'HCO', 'HSO', 'REF',
        'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO'
    ]

    return full_df


def save_dataframe_to_csv(full_df, csv_path):
    full_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Arquivo CSV gerado: {csv_path}")


def compress_csv_to_zip(csv_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=os.path.basename(csv_path))
    print(f"Arquivo ZIP criado: {zip_path}")


def main(zip_file_path, processed_dir):
    pdf_filename = 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'
    csv_filename = 'Rol_Procedimentos.csv'

    pdf_path = os.path.join(processed_dir, pdf_filename)
    csv_path = os.path.join(processed_dir, csv_filename)
    final_zip_path = os.path.join(processed_dir, 'Rol_Procedimentos_Final.zip')

    try:
        extract_pdf_from_zip(zip_file_path, processed_dir)

        full_df = process_pdf_to_dataframe(pdf_path)

        save_dataframe_to_csv(full_df, csv_path)

        compress_csv_to_zip(csv_path, final_zip_path)

        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"Arquivo PDF excluído: {pdf_filename}")

    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
