import os
from PIL import Image

def resize_images(directory, target_size=(250, 250)):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):  # Filter image files
                file_path = os.path.join(root, file)
                try:
                    # Open the image file
                    with Image.open(file_path) as img:
                        # Resize the image
                        img_resized = img.resize(target_size)
                        # Save the resized image, overwriting the original
                        img_resized.save(file_path)
                        print(f"Resized {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Directory containing subdirectories with images
dataset_directory = "dataset"

# Call the function to resize images in the dataset directory
resize_images(dataset_directory)
