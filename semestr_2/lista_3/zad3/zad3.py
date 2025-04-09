import argparse
import os
from pypdf import PdfReader, PdfWriter

def get_pdf_files(input_list):
    pdf_files = []
    for path in input_list:
        if os.path.isfile(path) and path.lower().endswith('.pdf'):
            pdf_files.append(path)
        elif os.path.isdir(path):
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isfile(full_path) and full_path.lower().endswith('.pdf'):
                    pdf_files.append(full_path)
        else:
            print(f"Pomijam: {path} (bo, nie jest plikiem PDF ani katalogiem)")
    return pdf_files

def merge_pdfs(pdf_files, output_pdf):
    pdf_writer = PdfWriter()
    for pdf_file in pdf_files:
        try:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            print(f"Dołączono: {pdf_file}")
        except Exception as e:
            print(f"Błąd przy przetwarzaniu {pdf_file}: {e}")
    with open(output_pdf, 'wb') as out:
        pdf_writer.write(out)
    print(f"Utworzono plik PDF: {output_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Łączenie plików PDF w jeden duży dokument.")
    parser.add_argument("--input", nargs='+', required=True, help="Lista plików PDF lub katalogów")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    pdf_files = get_pdf_files(args.input)
    if not pdf_files:
        print("Nie znaleziono żadnych plików PDF do połączenia.")
    else:
        merge_pdfs(pdf_files, args.output)
