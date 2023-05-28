import glob
import json
import os
import shutil

import cv2 as cv
from boxdetect.pipelines import get_checkboxes
from pdf2jpg import pdf2jpg

from config import get_config


# Resize to a specific width
def resize_images_in_a_dir(input_dir, width):
    output_dir = "input_images"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    for index, image_path in enumerate(sorted(glob.glob(f"{input_dir}/*.jpg"))):
        image = cv.imread(image_path)
        h, w = image.shape[:2]
        new_h = int(h * width / w)
        image = cv.resize(image, (width, new_h))
        cv.imwrite(f"{output_dir}/image_{index + 1}.jpg", image)

    return output_dir


def get_checkboxes_from_pdf(pdf_file_path, output=False):
    check_box_dict = dict()

    # Convert PDF to images
    result = pdf2jpg.convert_pdf2jpg(pdf_file_path, "", pages="ALL")
    image_dir = result[0]["output_pdfpath"]

    # Resize all the images
    output_image_dir = resize_images_in_a_dir(image_dir, width=2500)

    # Loop through extracted images
    for i, image_path in enumerate(sorted(glob.glob(f"{output_image_dir}/*.jpg"))):
        out_image = cv.imread(image_path)

        # Detect checkboxes
        checkboxes = get_checkboxes(image_path, cfg=get_config(), px_threshold=0.1, plot=False, verbose=False)
        _page_key = f"page_{i}"
        check_box_dict[_page_key] = []

        # Add to a dictionary
        for checkbox in checkboxes:
            _x, _y, _w, _h = checkbox[0]
            is_checked = checkbox[1]
            check_box_dict[_page_key].append(
                {
                    "x": _x,
                    "y": _y,

                    "width": _w,
                    "height": _h,
                    "contains_pixels": is_checked
                }
            )
            if output:
                # draw the rectangle on the image
                color = (0, 0, 255) if is_checked else (0, 255, 0)
                out_image = cv.rectangle(out_image, (_x, _y), (_x + _w, _y + _h), color, 2)

        if output:
            output_path = f"output/{image_dir}_{i:04d}_out.jpg"
            cv.imwrite(output_path, out_image)
            print("Output image saved to:", output_path)

    if not output:
        shutil.rmtree(image_dir)

    return check_box_dict


if __name__ == '__main__':
    for _file_path in glob.glob("input/*.pdf"):
        print("*" * 80)
        print(_file_path)
        output = get_checkboxes_from_pdf(_file_path, output=False)
        print(json.dumps(output, indent=4))
