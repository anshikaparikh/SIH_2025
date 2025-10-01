# ml_models/ocr/train_ocr.py
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import pandas as pd
from sklearn.model_selection import train_test_split

# =========================
# 1. Dataset Loader
# =========================
class OCRDataset(Dataset):
    def __init__(self, csv_path, img_dir, transform=None):
        """
        csv_path: CSV with columns [image, label]
        img_dir: directory containing images
        """
        self.data = pd.read_csv(csv_path)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = os.path.join(self.img_dir, self.data.iloc[idx, 0])
        label = int(self.data.iloc[idx, 1])

        image = Image.open(img_name).convert("L")  # grayscale
        if self.transform:
            image = self.transform(image)

        return image, label

# =========================
# 2. Model (CNN for OCR)
# =========================
class OCR_CNN(nn.Module):
    def __init__(self, num_classes=26):  # default = A-Z
        super(OCR_CNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        self.fc = nn.Sequential(
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

# =========================
# 3. Training Function
# =========================
def train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs=10):
    model.to(device)
    for epoch in range(epochs):
        model.train()
        running_loss, correct, total = 0.0, 0, 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        acc = correct / total
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss:.4f}, Train Acc: {acc:.4f}")

        # validation
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)
        print(f"Validation Acc: {val_correct / val_total:.4f}")

    return model

# =========================
# 4. Main Training Entry
# =========================
if __name__ == "__main__":
    # Paths
    CSV_PATH = "data/labels/ocr_labels.csv"   # CSV: image,label
    IMG_DIR = "data/raw/ocr_images/"
    SAVE_MODEL = "ml_models/ocr/ocr_cnn.pth"

    # Hyperparams
    batch_size = 32
    lr = 0.001
    epochs = 10
    num_classes = 26  # alphabets, modify if needed

    # Transforms
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # Dataset split
    full_data = pd.read_csv(CSV_PATH)
    train_df, val_df = train_test_split(full_data, test_size=0.2, random_state=42)

    train_df.to_csv("data/labels/train.csv", index=False)
    val_df.to_csv("data/labels/val.csv", index=False)

    train_dataset = OCRDataset("data/labels/train.csv", IMG_DIR, transform)
    val_dataset = OCRDataset("data/labels/val.csv", IMG_DIR, transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = OCR_CNN(num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Train
    trained_model = train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs)

    # Save
    torch.save(trained_model.state_dict(), SAVE_MODEL)
    print(f"✅ Model saved at {SAVE_MODEL}")
