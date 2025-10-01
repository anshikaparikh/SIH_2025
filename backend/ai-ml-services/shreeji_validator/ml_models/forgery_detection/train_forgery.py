# ml_models/forgery_detection/train_forgery.py
import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader

# CONFIG - edit as needed
DATA_DIR = "data/forgery"           # expects data/forgery/real & data/forgery/fake
MODEL_OUT = "ml_models/forgery_detection/forgery_resnet18.pth"
BATCH_SIZE = 16
IMG_SIZE = 224
NUM_EPOCHS = 8
LR = 1e-4
NUM_WORKERS = 4
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_data_loaders(data_dir):
    train_transforms = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.1,0.1,0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225]),
    ])
    val_transforms = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225]),
    ])

    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")

    train_dataset = datasets.ImageFolder(train_dir, transform=train_transforms)
    val_dataset = datasets.ImageFolder(val_dir, transform=val_transforms)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    return train_loader, val_loader, train_dataset.classes

def build_model(num_classes=2):
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    return model

def train():
    print("Device:", DEVICE)
    train_loader, val_loader, classes = get_data_loaders(DATA_DIR)
    model = build_model(num_classes=len(classes)).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    best_val_acc = 0.0
    for epoch in range(NUM_EPOCHS):
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total = 0
        t0 = time.time()
        for images, labels in train_loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * images.size(0)
            running_corrects += torch.sum(preds == labels.data).item()
            total += images.size(0)

        epoch_loss = running_loss / total
        epoch_acc = running_corrects / total

        # Validation
        model.eval()
        val_corrects = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(DEVICE)
                labels = labels.to(DEVICE)
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data).item()
                val_total += images.size(0)
        val_acc = val_corrects / val_total

        print(f"Epoch {epoch+1}/{NUM_EPOCHS} - loss: {epoch_loss:.4f} train_acc: {epoch_acc:.3f} val_acc: {val_acc:.3f} time: {time.time()-t0:.1f}s")

        # Save best
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
            torch.save({
                'model_state_dict': model.state_dict(),
                'classes': classes
            }, MODEL_OUT)
            print(f"Saved best model with val_acc={best_val_acc:.3f} to {MODEL_OUT}")

    print("Training finished. Best val acc:", best_val_acc)

if __name__ == "__main__":
    train()
