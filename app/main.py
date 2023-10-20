import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from CustomDataset import CustomDataset
# from torchvision.models import resnet50, ResNet50_Weights
from efficientnet_pytorch import EfficientNet

if __name__ == '__main__':

    trainset = CustomDataset(root_dir='C:\\Users\\garyk\\Downloads\\Capstone\\selectset2_train_aug', transform=transforms.ToTensor())
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True, num_workers=2)

    testset = CustomDataset(root_dir='C:\\Users\\garyk\\Downloads\\Capstone\\selectset2_test', transform=transforms.ToTensor())
    testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False, num_workers=2)

    # weights = ResNet50_Weights.DEFAULT
    # model = resnet50(weights=weights)

    # model = EfficientNet.from_pretrained('efficientnet-b5', num_classes=46)
    model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=45)

    # model.load_state_dict(torch.load('ns_weights_pytorch/efficientnet-b5.pth'))

    for param in model.parameters():
        param.requires_grad = False

    #resnet
    # num_classes = 46
    # in_features = model.fc.in_features
    # model.fc = nn.Linear(in_features, num_classes)

    #Efficientnet
    num_features = model._fc.in_features
    model._fc = nn.Linear(num_features, 45)

    #vgg
    # model.features[0] = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
    # num_features = model.classifier[6].in_features
    # model.classifier[6] = nn.Linear(num_features, 46)

    criterion = nn.CrossEntropyLoss()
    # optimizer = optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)
    optimizer = optim.Adam(model._fc.parameters(), lr=0.001)


    print('start')
    for epoch in range(50):
        # print(f'Epoch: {epoch}\n')
        # running_loss = 0.0
        model.train()
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        with torch.no_grad():
            model.eval()
            correct = 0
            total = 0
            all_val_loss = []
            for data in testloader:
                images, labels = data
                outputs = model(images)
                predicted = torch.argmax(outputs, dim=1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                all_val_loss.append(criterion(outputs, labels).item())

            mean_val_loss = sum(all_val_loss) / len(all_val_loss)
            mean_val_acc = 100 * (correct / total)

        print(f'Epoch[{epoch+1}, Loss:{loss.item()}, Val-loss:{mean_val_loss}, Val-acc:{mean_val_acc}%')
        PATH = f"6_11_selectset2_effnet0_adam_{epoch+1}.pt"
        torch.save(model.state_dict(), PATH)


    # Save the trained model
    # PATH = "5_4_species_res18_adam_50.pt"
    # torch.save(model.state_dict(), PATH)

    # model.eval()
    # correct = 0
    # total = 0
    # with torch.no_grad():
    #     for data in testloader:
    #         images, labels = data
    #         outputs = model(images)
    #         _, predicted = torch.max(outputs.data, 1)
    #         total += labels.size(0)
    #         correct += (predicted == labels).sum().item()
    #
    # print('Accuracy of the network on test images: %d %%' % (
    #         100 * correct / total))


