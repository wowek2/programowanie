import argparse
import cv2 as cv

def generate_miniature(filepath: str, size: list=[100,100], output_filename: str = 'output.jpg'):
    """
    Generates a miniature image from the input filepath and saves it as a .jpg file.

    Parameters:
    - filepath: The path to the input image.
    - size: The desired size for the miniature image (width, height).
    - output_filename: The desired jpg output filename.
    """
    img = cv.imread(filepath)
    img_resized = cv.resize(img, tuple(size))

    out = output_filename
    cv.imwrite(out, img_resized)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str)
    parser.add_argument('--width', type=int, default=100)
    parser.add_argument('--height', type=int, default=100)
    parser.add_argument('--out', type=str, default='output.jpg')

    args = parser.parse_args()

    size = [args.width, args.height]

    generate_miniature(args.filepath, size, args.out)

    print(f"Miniatura obrazu pomyślnie zapisana jako: {args.out}")
