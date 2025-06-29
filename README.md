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


## PDF to PPTX Converter Tool

This tool converts each page of a PDF document into a high-quality image slide in a PowerPoint (PPTX) file, preserving the original dimensions and aspect ratio of each page.

### Key Features

- **Pixel-perfect conversion**: Each PDF page becomes a slide with identical dimensions
- **High-quality output**: Configurable DPI (300-600) for crystal clear images
- **Aspect ratio preservation**: Maintains original PDF proportions
- **Batch processing**: Handles multi-page documents efficiently
- **Cross-platform**: Works on Windows, macOS, and Linux

### 1. Install Python Dependencies

```bash
pip install pdf2image pillow python-pptx
```


### Command Line Interface

```bash
python pdf2pptx.py
```

### How It Works

1. **PDF Processing**:
   - Converts each PDF page to a high-resolution PNG image
   - Uses poppler for accurate PDF rendering
   - Processes pages in parallel for speed

2. **Slide Preparation**:
   - Calculates maximum dimensions across all pages
   - Creates uniformly sized slides
   - Centers each page image proportionally

3. **PPTX Generation**:
   - Creates a new PowerPoint presentation
   - Adds each image as a separate slide
   - Maintains original aspect ratios
   - Preserves image quality without recompression
