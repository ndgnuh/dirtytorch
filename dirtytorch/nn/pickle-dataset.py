# short_desc: dataset with single pickle file, fast and easy to move arround
from torch.utils.data import Dataset


class PickleDataset(Dataset):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.positions = []
        self.io = open(path, "rb")
        while self.io.peek(1):
            self.positions.append(self.io.tell())
            pickle.load(self.io)

    def __len__(self):
        return len(self.positions)

    def load_sample(self, index):
        pos = self.positions[index]
        self.io.seek(pos)
        return pickle.load(self.io)

    def __getitem__(self, index):
        return self.load_sample(index)


def create_dataset(path, iterable):
    try:
        from tqdm import tqdm
        tqdm(iterable, "creating dataset")
    except Exception:
        pass
    for data in iterable:
        with open(path, "ab") as f:
            pickle.dump(data, f)
    return path
