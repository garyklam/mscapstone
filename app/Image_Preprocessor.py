from PIL import Image
import torchvision.transforms as transforms
import torch


class Image_Preprocessor:
    def __init__(self):
        self.max_dim = 224

    def resize(self, img, img_path):
        img.save(img_path)
        img = Image.open(img_path)
        width, height = img.size
        scale_factor = self.max_dim / max(width, height)

        # Calculate the new dimensions while maintaining the aspect ratio
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Resize the image
        resized_img = img.resize((new_width, new_height))
        resized_img.save(img_path)

    def to_tensor(self, img_path):
        process = transforms.ToTensor()
        image = Image.open(img_path).convert('RGB')
        tensor = process(image)
        tensor = torch.unsqueeze(tensor, 0)
        return tensor
