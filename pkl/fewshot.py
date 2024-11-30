import os
import pickle
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split


def create_pretraining_and_few_shot_splits(root_path, output_dir, image_size=80, val_split_ratio=0.2):
    """
    Divide the dataset into two parts (pretraining and few-shot learning), and split them into
    training, validation, and test sets separately.

    Parameters:
    - root_path: Path to the directory containing class folders with images.
    - output_dir: Path where the .pickle files will be saved.
    - image_size: Size to which images will be resized.
    - val_split_ratio: Proportion of training images to allocate to the validation set.
    """
    # Collect all classes and their images
    class_names = sorted(os.listdir(root_path))  # Sort class names for consistent indexing
    class_to_images = {}

    for class_name in class_names: # 枚举每个类
        class_path = os.path.join(root_path, class_name) # 找到每个类的路径
        if not os.path.isdir(class_path):
            continue

        images = []
        for img_file in os.listdir(class_path): # 枚举每个类的图片
            img_path = os.path.join(class_path, img_file)
            try:
                img = Image.open(img_path).convert("RGB").resize((image_size, image_size))
                
                if os.path.exists('/home/liuzilong/bbox/' + img_file[:9] + '/' + img_file[:len(img_file) - 5] + '/bbox.txt') :
                    with open('/home/liuzilong/bbox/' + img_file[:9] + '/' + img_file[:len(img_file) - 5] + '/bbox.txt') as f:
                        line = f.readline().strip()  # 读取第一行并去除首尾空白字符
                        numbers = [float(num) for num in line.split()]  # 使用 split() 分割并转换为指定类型
                        # print(numbers)
                else :
                    width, height = img.size
                    numbers = [width / 3, height / 3, width / 3, height / 3]

                images.append([np.array(img), numbers]) # 把图片加进这个类的图片集images中
            except Exception as e:
                print(f"Error processing file {img_path}: {e}")

        if images:
            class_to_images[class_name] = images
            
            
            # bbox[class_name] = 

    # Split all classes into pretraining and few-shot learning groups
    class_names = list(class_to_images.keys())
    pretraining_classes, few_shot_classes = train_test_split(class_names, test_size=0.4, random_state=42)

    # Function to split data into train, val, and test splits
    def split_data(classes):
        train_data, train_labels = [], []
        val_data, val_labels = [], []
        test_data, test_labels = [], []

        label_offset = 0
        for class_name in classes:
            images = class_to_images[class_name]
            train_images, test_images = train_test_split(images, test_size=0.4, random_state=42)
            train_images, val_images = train_test_split(train_images, test_size=val_split_ratio, random_state=42)

            train_data.extend(train_images)
            train_labels.extend([label_offset] * len(train_images))
            val_data.extend(val_images)
            val_labels.extend([label_offset] * len(val_images))
            test_data.extend(test_images)
            test_labels.extend([label_offset] * len(test_images))

            label_offset += 1

        return (train_data, train_labels), (val_data, val_labels), (test_data, test_labels)

    # Split pretraining and few-shot learning classes
    pretraining_splits = split_data(pretraining_classes)
    few_shot_splits = split_data(few_shot_classes)

    # Save splits to pickle files
    os.makedirs(output_dir, exist_ok=True)

    # Helper function to save splits
    def save_split(splits, prefix):
        split_names = ["train_phase_train", "train_phase_val", "test"]
        for split_name, (data, labels) in zip(split_names, splits):
            output_file = os.path.join(output_dir, f"{prefix}_{split_name}.pickle")
            with open(output_file, "wb") as f:
                
                image = [d[0] for d in data]
                bbox = [d[1] for d in data]
                print(len(image))
                pickle.dump({"data": image, "labels": labels, "bbox": bbox}, f)
                # exit(0)
            print(f"Saved {split_name} with {len(labels)} samples to {output_file}")

    save_split(pretraining_splits, "pretraining")
    save_split(few_shot_splits, "few_shot")


# Example usage
create_pretraining_and_few_shot_splits(
    root_path="/home/liuzilong/data2/datasets/pinpp/images",  # Folder containing class folders
    output_dir="./", # Folder to save .pickle files
    image_size=80,                # Resize images to 80x80
    val_split_ratio=0.2           # 20% of training images for validation
)