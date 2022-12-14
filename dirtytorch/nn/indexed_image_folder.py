# short_desc: IndexedImageFolder, image folder with annotation index file
from torchvision.datasets import VisionDataset
from os import path
from typing import Optional, Callable


class IndexedImageFolder(VisionDataset):
    def __init__(self,
                 index: str,
                 transform: Optional[Callable] = None,
                 target_transform: Optional[Callable] = None,
                 transforms: Optional[Callable] = None,
                 index_encoding: str = 'utf-8',
                 **kwargs):
        root = path.dirname(index)
        super().__init__(
            root=root,
            transforms=transforms
        )

        self.transform = transform
        self.target_transform = target_transform
        self.root = root
        self.index = index
        with open(self.index, encoding=index_encoding) as f:
            lines = [line.strip() for line in f.readlines()]
            lines = [path.join(root, line) for line in lines if len(line) > 0]
        self.samples = lines

    def load_sample(self, sample: str):
        raise NotImplementedError("Error")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index: int):
        image, target = self.load_sample(self.samples[index])
        if self.transforms is not None:
            image = self.transforms(image)
            target = self.transforms(target)
        if self.transform is not None:
            image = self.transform(image)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return image, target
