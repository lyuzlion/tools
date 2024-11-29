# tools
Some tools.

## pkl
This is a script to generate `.pickle` files.

The dataset should be organized like this before running the script:

```
/path/to/dataset/
    class_1/
        img1.jpg
        img2.jpg
        ...
    class_2/
        img1.jpg
        img2.jpg
        ...
    ...
```

This script will generate three `.pickle` files in the specified output directory:
1. `miniImageNet_category_split_train_phase_train.pickle`
2. `miniImageNet_category_split_train_phase_val.pickle`
3. `miniImageNet_category_split_test.pickle`

Each `.pickle` file will contain a dictionary:
- **`data`**: A list of numpy arrays, each representing an image.
- **`labels`**: A list of integers representing the labels corresponding to each image.

**Notes**
1. You can customize the train-validation-test split ratios in the `train_test_split` calls.
2. Add error handling if you anticipate issues with image formats or corrupted files.

