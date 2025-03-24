import zipfile
import os
import argparse
from enum import Enum
import datetime

class CompressionMethod(Enum):
    deflated = zipfile.ZIP_DEFLATED
    bzip2 = zipfile.ZIP_BZIP2
    lzma = zipfile.ZIP_LZMA

def zip_folder(folder_path, compression_method):
    zip_filename = f"{args.folder_path.rstrip(os.sep)}_backup_{datetime.date.today()}.zip"
    with zipfile.ZipFile(zip_filename, 'w', compression_method) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    print(f"Stworzono kopię bezpieczeństwa dla katalogu: {folder_path} w pliku {zip_filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path', type=str, help='Path to the folder to zip')
    args = parser.parse_args()

    print("Wybierz metodę kompresji z poniższych:")

    for opt in CompressionMethod:
        print(opt.name)

    choice = input("Wprowadź metodę kompresji (np. deflated): ")

    try:
        selected_opt = CompressionMethod[choice]
    except KeyError:
        print("Nieprawidłowo wpisana metoda kompresji! Wybieram domyślną: deflated.")
        selected_opt = CompressionMethod.deflated

    zip_folder(args.folder_path, selected_opt.value)
