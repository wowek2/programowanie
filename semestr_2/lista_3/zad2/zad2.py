import os
import argparse

def convert_line_endings(file_path, to_windows=True):
    with open(file_path, 'rb') as file:
        content = file.read()

    if to_windows:
        new_content = content.replace(b'\n', b'\r\n')
    else:
        new_content = content.replace(b'\r\n', b'\n')

    if new_content != content:
        with open(file_path, 'wb') as file:
            file.write(new_content)
        print(f"Zmieniono format: {file_path}")
    else:
        print(f"Bez zmian: {file_path}")

def process_directory(source_dir, extensions, to_windows=True):
    """Przechodzi przez katalog i konwertuje pliki o podanych rozszerzeniach."""
    for foldername, subfolders, filenames in os.walk(source_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(foldername, filename)
                convert_line_endings(file_path, to_windows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Konwersja znaków końca linii w plikach tekstowych.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--extensions", nargs='+')
    parser.add_argument("--to-windows", action="store_true")
    parser.add_argument("--to-unix", action="store_true")

    args = parser.parse_args()

    if args.to_windows and args.to_unix:
        print("Wybierz tylko jedną opcję: --to-windows lub --to-unix.")
    elif not args.to_windows and not args.to_unix:
        print("Podaj opcję konwersji: --to-windows lub --to-unix.")
    else:
        process_directory(args.source, args.extensions, to_windows=args.to_windows)
