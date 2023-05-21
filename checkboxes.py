from boxdetect import config
from boxdetect.pipelines import get_boxes, get_checkboxes
import matplotlib.pyplot as plt
from pdf2image import convert_from_path


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
    # Store Pdf with convert_from_path function
    images = convert_from_path(pdf_file_path)

    for i in range(len(images)):
        # Save pages as images in the pdf
        file_name = 'page' + str(i) + '.jpg'
        images[i].save(file_name, 'JPEG')

        # rects, grouping_rects, image, output_image = get_boxes(
        #     file_name, cfg=get_config(), plot=False)
        #
        #
        #
        # plt.figure(figsize=(20, 20))
        # plt.imshow(output_image)
        # # plt.show()
        # # save image
        # plt.savefig(f'output_image_{i}.jpg')
        # # output_image.save(f'output_image_{i}.jpg')
        # check_box_dict[i] = rects

        checkboxes = get_checkboxes(file_name, cfg=get_config(), px_threshold=0.1, plot=False, verbose=True)

        # print("Output object type: ", type(checkboxes))
        _page_key = f"page_{i}"
        check_box_dict[_page_key] = []
        for checkbox in checkboxes:
            # print("Checkbox bounding rectangle (x,y,width,height): ", checkbox[0])
            # print("Result of `contains_pixels` for the checkbox: ", checkbox[1])
            # print("Display the cropout of checkbox:")
            # plt.figure(figsize=(1, 1))
            # plt.imshow(checkbox[2])
            # plt.show()

            check_box_dict[_page_key].append(
                {
                    "x": checkbox[0][0],
                    "y": checkbox[0][1],
                    "width": checkbox[0][2],
                    "height": checkbox[0][3],
                    "contains_pixels": checkbox[1]
                }
            )

    return check_box_dict


if __name__ == '__main__':
    _pdf_file_path = '0AB4CD_1.PDF'
    print(get_checkboxes_from_pdf(_pdf_file_path))