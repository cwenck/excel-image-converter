#!/usr/bin/env python3

from PIL import Image
import csv
import sys

PIXEL_DELIMITER = ','
WHITE = (255, 255, 255)


# Process an image. This handles scaling the image, converting any color modes,
# removing an alpha channel if present, and separating frames if the image is a gif.
def process_image(original_img, size):
    frames = []
    for frame_num in range(original_img.n_frames):
        original_img.seek(frame_num)
        frame = Image.new('RGB', original_img.size, WHITE)
        frame.paste(original_img)
        resized_frame = frame.resize(size)
        frames.append(resized_frame)

    return frames


def to_csv(frames, name):
    width = frames[0].width
    height = frames[0].height

    with open(name + '-r.csv', 'w') as r_file, open(name + '-g.csv', 'w') as g_file, open(name + '-b.csv', 'w') as b_file:
        r_writer = csv.writer(r_file, delimiter=PIXEL_DELIMITER)
        g_writer = csv.writer(g_file, delimiter=PIXEL_DELIMITER)
        b_writer = csv.writer(b_file, delimiter=PIXEL_DELIMITER)

        for row in range(height):
            for col in range(width):
                csv_row_r = []
                csv_row_g = []
                csv_row_b = []

                for frame in frames:
                    (r, g, b) = frame.getpixel((col, row))
                    csv_row_r.append(str(r))
                    csv_row_g.append(str(g))
                    csv_row_b.append(str(b))

                r_writer.writerow(csv_row_r)
                g_writer.writerow(csv_row_g)
                b_writer.writerow(csv_row_b)


def main():
    args = sys.argv

    if len(args) < 2 or len(args) > 4:
        print('Usage:\n  ' + args[0] +
              ' img_name [width] [height]', file=sys.stderr)
        sys.exit(1)

    # Open the image file
    img = Image.open(args[1])

    # Determine the desired resoulution of the output
    size = (img.width, img.height)
    if len(args) == 4:
        size = (int(args[2]), int(args[3]))

    print('Generating output of size %sx%s' % (size[0], size[1]))

    frames = process_image(img, size)
    to_csv(frames, 'data')


if __name__ == '__main__':
    main()