import glob
import shutil

from boxdetect import config
from boxdetect.pipelines import get_checkboxes
from pdf2jpg import pdf2jpg


def get_config():
    cfg = config.PipelinesConfig()

    # important to adjust these values to match the size of boxes on your image
    cfg.width_range = (30, 55)
    cfg.height_range = (25, 40)

    # the more scaling factors the more accurate the results but also it takes more time to processing
    # too small scaling factor may cause false positives
    # too big scaling factor will take a lot of processing time
    cfg.scaling_factors = [0.7]

    # w/h ratio range for boxes/rectangles filtering
    cfg.wh_ratio_range = (0.5, 1.7)

    # group_size_range starting from 2 will skip all the groups
    # with a single box detected inside (like checkboxes)
    # cfg.group_size_range = (2, 100)
    cfg.group_size_range = (1, 1)

    # num of iterations when running dilation tranformation (to engance the image)
    cfg.dilation_iterations = 0

    return cfg


def get_checkboxes_from_pdf(pdf_file_path):
    check_box_dict = dict()

    result = pdf2jpg.convert_pdf2jpg(pdf_file_path, "", pages="ALL")
    image_dir = result[0]["output_pdfpath"]

    for i, image_path in enumerate(sorted(glob.glob(f"{image_dir}/*.jpg"))):
        checkboxes = get_checkboxes(image_path, cfg=get_config(), px_threshold=0.1, plot=False, verbose=True)
        _page_key = f"page_{i}"
        check_box_dict[_page_key] = []
        for checkbox in checkboxes:
            check_box_dict[_page_key].append(
                {
                    "x": checkbox[0][0],
                    "y": checkbox[0][1],
                    "width": checkbox[0][2],
                    "height": checkbox[0][3],
                    "contains_pixels": checkbox[1]
                }
            )

    shutil.rmtree(image_dir)

    return check_box_dict


if __name__ == '__main__':
    _pdf_file_path = '0AB4CD_1.PDF'
    print(get_checkboxes_from_pdf(_pdf_file_path))
