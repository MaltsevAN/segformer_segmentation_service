import torch.nn as nn
import torch
import numpy as np
from PIL import Image
from transformers import (
    AutoModelForSemanticSegmentation,
    AutoFeatureExtractor
)

from utils import random_color_generator


class SegformerSegmenter(object):
    def __init__(self, model_path: str):
        self.extractor = AutoFeatureExtractor.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSemanticSegmentation.from_pretrained(model_path, local_files_only=True).eval()
        self.id2label = self.model.config.to_dict()['id2label']

        self.__generate_calor_map()

    def get_segments_img(self, image):
        upsampled_logits = self.get_upsamples_logits(image)
        seg_labels = upsampled_logits.argmax(dim=0)

        return self.labels2img(seg_labels)

    def get_upsamples_logits(self, image) -> torch.Tensor:
        """
        Функция для сегментации изображения
        :param image:
        :return:
        """
        inputs = self.extractor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits.cpu()

        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image.size[::-1],
            mode="bilinear",
            align_corners=False,
        )

        return upsampled_logits[0]

    def labels2img(self, seg_labels: torch.Tensor) -> Image.Image:
        t2np = np.zeros((seg_labels.shape[0], seg_labels.shape[1], 3), dtype=np.uint8)

        for label, color in self.id_color_map.items():
            t2np[seg_labels == label, :] = color
        t2np = t2np[..., ::-1]
        return Image.fromarray(t2np)

    def __generate_calor_map(self):
        self.id_color_map = {}
        for id in self.id2label.keys():
            self.id_color_map[id] = random_color_generator()
