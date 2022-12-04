from typing import Optional, Callable
from itertools import groupby
from onnxruntime import InferenceSession, get_available_providers
from PIL import Image
from typing import Callable
import numpy as np


def to_ndarray(images: Image, normalize=True):
    images = [np.array(image) for image in images]
    for i, image in enumerate(images):
        if normalize and image.max() > 2:
            images[i] = image / 255
    images = np.stack(images, axis=0)
    # N H W C -> N C H W
    images = images.transpose((0, 3, 1, 2)).astype('float32')
    print(images.shape)
    return images


def ctc_greedy_decode(logits, blank_id, vocab=None):
    preds = logits.argmax(axis=-1)
    outputs = []
    for pred in preds:
        output = [c for c, _ in groupby(pred) if c != blank_id]
        outputs.append(output)
    if vocab is not None:
        outputs = [
            ''.join([vocab[i] for i in output])
            for output in outputs
        ]
    return outputs


def read_vocab_file(file: str, blank_first=True) -> dict:
    with open(file) as f:
        vocab = f.read()
        vocab = vocab.strip("\r\n\t")
        assert len(set(vocab)) == len(
            list(vocab)), "Duplicate character in vocab"
        if blank_first:
            d_vocab = {i + 1: c for i, c in enumerate(vocab)}
            d_vocab[0] = "<blank>"
        else:
            d_vocab = dict(enumerate(vocab))
            d_vocab[len(vocab)] = "<blank>"
        return d_vocab


class CTCClassifier:
    def __init__(self,
                 onnx_file: str,
                 preprocess: Callable = to_ndarray,
                 postprocess: Callable = ctc_greedy_decode,
                 blank_id: int = 0,
                 vocab: Optional[dict] = None,
                 silent: bool = False):

        if isinstance(vocab, str):
            if not silent:
                print("`vocab` is a string (expected `dict`), using `blank_id = 0`")
            blank_id = 0
            vocab = " " + vocab

        self.model = InferenceSession(
            onnx_file,
            providers=get_available_providers()
        )
        self.input_name = self.model.get_inputs()[0].name
        self.preprocess = preprocess
        self.postprocess = postprocess
        self.blank_id = blank_id
        self.vocab = vocab

    def __call__(self, images: Image):
        if not isinstance(images, (list, tuple, set)):
            images = (images,)
        if self.preprocess is not None:
            images = self.preprocess(images)
        logits, = self.model.run(None, {self.input_name: images})
        predictions = self.postprocess(logits, self.blank_id, self.vocab)
        return predictions
