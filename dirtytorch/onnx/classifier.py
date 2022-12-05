# short_desc: generic classifier
import numpy as np
from PIL import Image
from typing import List, Tuple, Callable, Collection
from onnxruntime import InferenceSession, get_available_providers


def preprocess(image: Image):
    image = image.convert("RGB")
    return np.array(image)


def softmax(x: np.ndarray):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


class Classifier:
    def __init__(self,
                 model_file: str,
                 labels: Collection[str],
                 image_size: Tuple[int, int],
                 preprocess: Callable = preprocess,
                 providers: List = get_available_providers()):
        self.model = InferenceSession(
            model_file,
            providers=providers
        )
        self.preprocess = preprocess
        self.image_size = image_size
        self.input_name = self.model.get_inputs()[0].name
        self.labels = labels

    def __call__(self, images: Collection[Image]):
        # Forward pass
        inputs = self.preprocess(images)
        logits, = self.model.run(None, {self.input_name: inputs})
        logits = logits.flatten()
        softmaxs = softmax(logits)

        # Result
        label_idx = np.argmax(softmaxs)
        label = self.labels[label_idx]
        confidence = softmaxs[label_idx]

        result = dict(label=label,
                      label_idx=label_idx,
                      logits=logits,
                      softmaxs=softmaxs,
                      confidence=confidence)
        return result
