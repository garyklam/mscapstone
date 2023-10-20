import os

import torch
from torchvision import transforms
from CustomDataset import CustomDataset
from torchvision.models import resnet50
from efficientnet_pytorch import EfficientNet
import torch.nn as nn

def test_model():
    testset = CustomDataset(root_dir='C:\\Users\\garyk\\Downloads\\Capstone\\selectset2_test',
                            transform=transforms.ToTensor())
    testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False, num_workers=2)

    # model = resnet50()

    PATH = "CNN_test\\6_11_selectset2_effnet0_adam_10.pt"

    model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=45)
    model.load_state_dict(torch.load(PATH))

    # Replace the final fully connected layer, for resnet
    # num_features = model.fc.in_features
    # model.fc = nn.Linear(num_features, 46)
    #
    # state_dict = torch.load(PATH)
    # model.load_state_dict(state_dict)
    model.eval()

    print('Start')
    correct_1 = 0
    correct_3 = 0
    correct_5 = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            # print(labels[0])
            outputs = model(images)
            # print(outputs[0])
            _, top1 = torch.max(outputs.data, 1)
            _, top3 = torch.topk(outputs, k=3, dim=1)
            _, top5 = torch.topk(outputs, k=5, dim=1)
            total += labels.size(0)
            correct_1 += (top1 == labels).sum().item()
            correct_3 += (top3 == labels.view(-1, 1)).sum().item()
            correct_5 += (top5 == labels.view(-1, 1)).sum().item()

    print('Top1 Acc: %d %% Top3 Acc: %d %% Top5 Acc: %d %%' % (
        100 * correct_1 / total, 100 * correct_3 / total, 100 * correct_5 / total))

def test_by_species():

    PATH = "CNN_test\\6_11_selectset2_effnet0_adam_10.pt"
    model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=45)
    model.load_state_dict(torch.load(PATH))

    src = 'C:\\Users\\garyk\\Downloads\\Capstone\\selectset2_test'
    dest = 'C:\\Users\\garyk\\Downloads\\selectspecies_tester'
    print('Start')
    for dir in os.listdir(src):
        for filename in os.listdir(os.path.join(src, dir)):
            os.rename(os.path.join(src, dir, filename), os.path.join(dest, dir, filename))
        testset = CustomDataset(root_dir=dest,
                                transform=transforms.ToTensor())
        testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False, num_workers=2)

        correct_1 = 0
        correct_3 = 0
        correct_5 = 0
        total = 0
        model.eval()
        with torch.no_grad():
            for data in testloader:
                images, labels = data
                # print(labels[0])
                outputs = model(images)
                # print(outputs[0])
                _, top1 = torch.max(outputs.data, 1)
                _, top3 = torch.topk(outputs, k=3, dim=1)
                # print(top3)
                # _, top5 = torch.topk(outputs, k=5, dim=1)
                total += labels.size(0)
                correct_1 += (top1 == labels).sum().item()
                correct_3 += (top3 == labels.view(-1, 1)).sum().item()
                # correct_5 += (top5 == labels.view(-1, 1)).sum().item()

        print(f'{dir} {100 * correct_1 / total} {len(os.listdir(os.path.join(dest, dir)))}')
        # print(f'{100 * correct_1 / total}')
        for filename in os.listdir(os.path.join(dest, dir)):
            os.rename(os.path.join(dest, dir, filename), os.path.join(src, dir, filename))

def reset():
    src = 'C:\\Users\\garyk\\Downloads\\Capstone\\selectset_test'
    dest = 'C:\\Users\\garyk\\Downloads\\selectspecies_tester'
    print('file reset')
    for dir in os.listdir(dest):
        for filename in os.listdir(os.path.join(dest, dir)):
            os.rename(os.path.join(dest, dir, filename), os.path.join(src, dir, filename))

if __name__ == '__main__':
    test_model()
    # src = 'C:\\Users\\garyk\\Downloads\\Capstone\\selectset2_test'
    # dest = 'C:\\Users\\garyk\\Downloads\\selectspecies_tester'
    # print('Start')
    # for dir in os.listdir(src):
    #     os.mkdir(os.path.join(dest, dir))
    # reset()
    # test_by_species()
