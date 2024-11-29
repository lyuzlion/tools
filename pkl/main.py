import os
import pickle
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

def create_pickle(root_path, output_dir, image_size=80):
    """
    Create .pickle files for dataset.

    Parameters:
    - root_path: Path to the directory containing class folders with images.
    - output_dir: Path where the .pickle files will be saved.
    - image_size: Size to which images will be resized.
    """
    # Collect all images and labels
    data = []
    labels = []
    class_names = sorted(os.listdir(root_path))  # Sort class names for consistent label assignment
    class_to_idx = {class_name: idx for idx, class_name in enumerate(class_names)}

    print("Classes and assigned labels:", class_to_idx)

    for class_name in class_names:
        class_path = os.path.join(root_path, class_name)
        if not os.path.isdir(class_path):
            continue
        
        for img_file in os.listdir(class_path):
            img_path = os.path.join(class_path, img_file)
            try:
                img = Image.open(img_path).convert("RGB").resize((image_size, image_size))
                data.append(np.array(img))
                labels.append(class_to_idx[class_name])
            except Exception as e:
                print(f"Error processing file {img_path}: {e}")

    # Split data into train, validation, and test sets
    train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=42)
    val_data, test_data, val_labels, test_labels = train_test_split(test_data, test_labels, test_size=0.5, random_state=42)

    splits = {
        "train_phase_train": (train_data, train_labels),
        "train_phase_val": (val_data, val_labels),
        "test": (test_data, test_labels),
    }

    # Save each split to a .pickle file
    os.makedirs(output_dir, exist_ok=True)
    for split_name, (split_data, split_labels) in splits.items():
        output_file = os.path.join(output_dir, f"miniImageNet_category_split_{split_name}.pickle")
        with open(output_file, "wb") as f:
            pickle.dump({"data": split_data, "labels": split_labels}, f)
        print(f"Saved {split_name} data to {output_file}")


# Example usage
create_pickle(
    root_path="/home/liuzilong/data2/datasets/pinpp/images",  # Folder containing class folders
    output_dir="~/pkl", # Folder to save .pickle files
    image_size=100                 # Resize images to 80x80
)