import os
import torch
from torch.utils.data import Dataset
from PIL import Image


class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.labels = []
        self.filepaths = []
        indx = -1
        for label in os.listdir(self.root_dir):
            indx += 1
            sub_dir = os.path.join(self.root_dir, label)
            for file in os.listdir(sub_dir):
                if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.JPG'):
                    self.filepaths.append(os.path.join(sub_dir, file))
                    self.labels.append(indx)


    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = Image.open(self.filepaths[idx]).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label, dtype=torch.long)

