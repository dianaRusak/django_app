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


class object_detection():
    def __init__(self, *args, **kwargs):
        global dnn
        super().__init__(*args, **kwargs)
        print("coin worker created", flush=True)

        if not dnn:
            dnn = dark()

        self.dn = dnn.dn
        self.net_main = dnn.net_main
        self.meta_main = dnn.meta_main
        self.alt_names = dnn.alt_names
        self.darknet_image = dnn.darknet_image
        self.response_min_cnt = 4


    def recognize(self, path_to_img):
        frame_rgb = cv2.imread(path_to_img)
        frame_resized = cv2.resize(frame_rgb,
                                   (self.dn.network_width(self.net_main),
                                    self.dn.network_height(self.net_main)),
                                   interpolation=cv2.INTER_LINEAR)

        print((self.dn.network_width(self.net_main),
               self.dn.network_height(self.net_main)))

        self.dn.copy_image_from_bytes(self.darknet_image, frame_resized.tobytes())

        detections = self.dn.detect_image(self.net_main, self.meta_main, self.darknet_image, thresh=0.3)
        response = []
        kx = frame_rgb.shape[1] / self.dn.network_width(self.net_main)
        ky = frame_rgb.shape[0] / self.dn.network_height(self.net_main)

        print(*(d[0].decode() for d in detections))
        for i, detection in enumerate(detections):
            detections[i] = (self.category_to_id[detections[i][0].decode()], *detections[i][1:])

        for label, confidence, (x1, y1, width, height) in detections:
            x1 = x1 * kx
            y1 = y1 * ky

            coords = [
                int(y1 - height * ky / 2), int(x1 - width * kx / 2),
                int(y1 + height * ky / 2), int(x1 + width * kx / 2)
            ]

            print(f"y: {coords[0]}\tx:  {coords[1]}\th: {coords[2] - coords[0]}\tw: {coords[3] - coords[1]}")
            return coords
