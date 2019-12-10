import stenography

from skimage import io
from PIL import ImageFilter, Image


def main():
    data_in = "files/initial.txt"
    image_in = "files/initial_image.JPG"
    image_out = "files/final_image.JPG"

    with open(data_in, 'r+') as f:
        input_text = f.read()

    print('Input data: ', input_text)
    print('Input image file: ', image_in)
    image_out_file, _ = stenography.encrypt(input_text, image_in, image_out)

    io.imsave(image_out, image_out_file)

    image = Image.open(image_out)
    im1 = image.filter(ImageFilter.BLUR)
    im1.show()


if __name__ == '__main__':
    main()
