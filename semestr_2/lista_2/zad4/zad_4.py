import pypdf
import argparse
import os
from pathlib import Path

def split_pdf(file_path, pages_per_file):
    reader = pypdf.PdfReader(file_path)

    num_pages = reader.get_num_pages() 
    num_files = (num_pages + pages_per_file - 1) // pages_per_file

    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)

    for i in range(num_files):
        writer = pypdf.PdfWriter()

        start_page = i * pages_per_file
        end_page = min(start_page+pages_per_file, num_pages)

        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        output_file = output_path / f"splitted{i+1}.pdf"
        with output_file.open("wb") as output_pdf:
            writer.write(output_pdf)
        print(f"Zapisano {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str)
    parser.add_argument('pages_per_file', type=int)
    args = parser.parse_args()

    split_pdf(args.file_path, args.pages_per_file)