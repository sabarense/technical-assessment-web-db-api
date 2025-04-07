import zipfile


def extract_pdf_from_zip(zip_file_path, extract_path, pdf_filename):
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extract(pdf_filename, extract_path)
    print(f"PDF extraído: {pdf_filename}")