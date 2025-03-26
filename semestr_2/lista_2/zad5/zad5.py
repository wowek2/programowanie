import cv2 as cv
import argparse


def add_watermark(filepath, alpha, beta, gamma):
    watermark = cv.imread('watermark.jpg')
    img = cv.imread(filepath)

    h_watermark, w_watermark, _ = watermark.shape

    h_img, w_img, _ = img.shape

    center_x = int(w_img/2)
    center_y = int(h_img/2)

    top_y = center_y - int(h_watermark/2)
    bottom_y =  top_y + h_watermark
    left_x = center_x - int(w_watermark/2)
    right_x = left_x + w_watermark

    dest = img[top_y:bottom_y, left_x:right_x]
    result = cv.addWeighted(dest, alpha, watermark, beta,gamma)
    img[top_y:bottom_y, left_x:right_x] = result 

    cv.imwrite("watermarked.jpg", img) 
    cv.waitKey(0) 
    cv.destroyAllWindows() 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str)
    parser.add_argument('--alpha', type=float, default=1)
    parser.add_argument('--beta', type=float, default=1)
    parser.add_argument('--gamma', type=float, default=0)

    args = parser.parse_args()

    add_watermark(args.filepath, args.alpha, args.beta, args.gamma)
