import os
import sys

import cv2

from web_project.settings import BASE_DIR


class dark:
    def __init__(self):
        if 'darknet' not in sys.modules:
            path = r""
            sys.path.append(path)
            import darknet
            sys.path.pop()
        self.dn = darknet

        cfg = r""
        config_path = os.path.join(cfg, "yolov3.cfg")
        meta_path = os.path.join(cfg, "coco.data")
        weight_path = os.path.join(cfg, "yolov3.weights")

        self.net_main = darknet.load_net_custom(config_path.encode("ascii"), weight_path.encode("ascii"), 0, 1)
        self.meta_main = darknet.load_meta(meta_path.encode("ascii"))
        with open(meta_path) as metaFH:
            meta_contents = metaFH.read()
            import re
            match = re.search("names *= *(.*)$", meta_contents, re.IGNORECASE | re.MULTILINE)
            result = match.group(1) if match else None
            if os.path.exists(result):
                with open(result) as namesFH:
                    names_list = namesFH.read().strip().split("\n")
                    self.alt_names = [x.strip() for x in names_list]

        print(f"({self.dn.network_width(self.net_main)} {self.dn.network_height(self.net_main)}")
        self.darknet_image = darknet.make_image(darknet.network_width(self.net_main),
                                                darknet.network_height(self.net_main), 3)

    def test(self):
        print("It's test message for dark class")


dnn = None
