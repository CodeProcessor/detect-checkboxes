
from boxdetect import config


def get_config():
    cfg = config.PipelinesConfig()

    # important to adjust these values to match the size of boxes on your image
    cfg.width_range = (30, 70)
    cfg.height_range = (25, 70)

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
    cfg.dilation_iterations = 1

    return cfg
