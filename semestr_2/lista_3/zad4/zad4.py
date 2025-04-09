import argparse
import cv2
import qrcode

def generate_qr(text, output_file, box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    print(f"Wygenerowano kod QR i zapisano do {output_file}")

def read_qr(image_file):
    img = cv2.imread(image_file)
    if img is None:
        print(f"Nie udało się wczytać pliku: {image_file}")
        return

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)
    if points is not None:
        print("Odczytany kod QR:", data)
    else:
        print("Nie znaleziono kodu QR w obrazie.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generowanie i odczyt kodów QR"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Tryb działania: generate lub read")

    # Subparser dla generowania kodu QR
    gen_parser = subparsers.add_parser("generate", help="Generuj kod QR z podanego tekstu.")
    gen_parser.add_argument("--text", required=True)
    gen_parser.add_argument("--output", required=True)
    gen_parser.add_argument("--box-size", type=int, default=10)
    gen_parser.add_argument("--border", type=int, default=4)

    # Subparser dla odczytu kodu QR
    read_parser = subparsers.add_parser("read", help="Odczytaj kod QR z podanego pliku obrazu.")
    read_parser.add_argument("--file", required=True)

    args = parser.parse_args()

    if args.command == "generate":
        generate_qr(args.text, args.output, box_size=args.box_size, border=args.border)
    elif args.command == "read":
        read_qr(args.file)
