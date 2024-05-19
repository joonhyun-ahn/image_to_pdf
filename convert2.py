import os
import sys
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas

def merge_images_to_pdf(input_folder, images_per_page=1):
    output_pdf = generate_output_filename(input_folder)
    c = canvas.Canvas(output_pdf, pagesize=landscape((0, 0)))  # Set initial page size to (0, 0)

    # Get list of image files in the input folder
    image_paths = [os.path.join(input_folder, file) for file in sorted(os.listdir(input_folder)) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    # Iterate through each image and adjust page size accordingly
    for image_path in image_paths:
        img = Image.open(image_path)
        width, height = img.size

        # Set page size based on image size
        c.setPageSize((width, height))
        c.drawImage(image_path, 0, 0)  # Draw image at (0, 0) coordinate
        c.showPage()

    c.save()
    return output_pdf

def generate_output_filename(input_folder):
    folder_name = os.path.basename(input_folder)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{folder_name}_{current_time}.pdf"

if __name__ == "__main__":
    input_folder = sys.argv[1]
    # Get the number of images per page from the command line arguments, default to 2 if not provided
    images_per_page = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    output_pdf = merge_images_to_pdf(input_folder, images_per_page)
    print(f"PDF file '{output_pdf}' has been created.")
