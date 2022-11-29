from torchvision.datasets import VisionDataset, ImageFolder
import os
from os import path
from functools import reduce
from itertools import product
from PIL import Image
import random


class TripletImageFolder(VisionDataset):
    def __init__(self, root, length=100, *args, **kwargs):
        super().__init__(*args, **kwargs, root=root)
        self.length = length
        self.classes = sorted(os.listdir(root))
        self.subjects = reduce(set.intersection, [
            set(os.listdir(path.join(root, cls)))
            for cls in self.classes
        ])
        self.subjects = sorted(list(self.subjects))

        # IDS
        self.num_classes = len(self.classes)
        self.class_ids = list(range(len(self.classes)))
        self.subject_ids = list(range(len(self.subjects)))

        # Database
        self.negative_classes = tuple(
            tuple(id1 for id1 in self.class_ids if id1 != id2)
            for id2 in self.class_ids
        )
        self.database = {
            (cls_id, sbj_id): tuple(
                path.join(root, cls, sbj, file)
                for file in os.listdir(path.join(root, cls, sbj))
            )
            for (cls_id, cls), (sbj_id, sbj) in
            product(
                zip(self.class_ids, self.classes),
                zip(self.subject_ids, self.subjects)
            )
        }

    def __getitem__(self, idx):
        # Random ID
        anchor_class = self.class_ids[idx % self.num_classes]
        negative_class = random.choice(self.negative_classes[anchor_class])
        subject_id = random.choice(self.subject_ids)

        # Get the paths
        anchor, positive = random.choices(
            self.database[(anchor_class, subject_id)],
            k=2
        )
        negative = random.choice(
            self.database[(negative_class, subject_id)]
        )

        # Load data
        anchor = Image.open(anchor)
        positive = Image.open(positive)
        negative = Image.open(negative)

        # Transforming
        if self.transform is not None:
            anchor = self.transform(anchor)
            positive = self.transform(positive)
            negative = self.transform(negative)

        if self.target_transform is not None:
            anchor_class = self.target_transform(anchor_class)
            negative_class = self.target_transform(negative_class)

        return (anchor, positive, negative), (anchor_class, negative_class)

    def extra_repr(self):
        subject_str = "Subjects: " + ', '.join(self.subjects)
        classes_str = "Classes: " + ', '.join(self.classes)
        s = [subject_str, classes_str]
        return '\n'.join(s)

    def __len__(self):
        return self.length


if __name__ == '__main__':
    # Example usages
    from torchvision.transforms import functional as FT
    from torch.utils.data import DataLoader
    from torch import tensor

    def transform(img):
        img = FT.to_tensor(img)
        img = FT.resize(img, (80, 80))
        return img

    # The root folder should be organized as follow
    # root/
    #   label1/
    #       subject1/
    #           ... # images
    #       subject2/
    #           ... # images
    #       ... # other subjects
    #   label2/
    #       subject1/
    #           ... # images
    #       subject2/
    #           ... # images
    #       ... # other subjects
    #   ... # other labels
    tif = TripletImageFolder("root/folder",
                             transform=transform,
                             target_transform=tensor)
    tif_loader = DataLoader(tif, batch_size=4)

    # 1 batch = (anchor, positive, negative), (positive label, negative label)
    (an, po, ne), (po, ne) = next(iter(tif_loader))
