import os
import sys
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas

def merge_images_to_pdf(input_folder):
    output_pdf = generate_output_filename(input_folder)
    c = canvas.Canvas(output_pdf, pagesize=landscape((0, 0)))  # Set initial page size to (0, 0)

    # Get list of image files in the input folder
    image_paths = [os.path.join(input_folder, file) for file in sorted(os.listdir(input_folder)) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    # Iterate through each pair of images and add them to PDF
    for i in range(0, len(image_paths), 2):
        img1_path = image_paths[i]
        img1 = Image.open(img1_path)
        img2_path = image_paths[i + 1] if i + 1 < len(image_paths) else None
        if img2_path:
            img2 = Image.open(img2_path)

            # Adjust image widths if greater than 600
            img1_width, img1_height = img1.size
            if img1_width > 600:
                ratio = 600 / img1_width
                img1 = img1.resize((600, int(img1_height * ratio)), Image.ANTIALIAS)

            img2_width, img2_height = img2.size
            if img2_width > 600:
                ratio = 600 / img2_width
                img2 = img2.resize((600, int(img2_height * ratio)), Image.ANTIALIAS)

            # Calculate total width and height for the combined image
            total_width = img1.width + img2.width
            max_height = max(img1.height, img2.height)

            # Create a new blank image with the calculated size
            combined_img = Image.new('RGB', (total_width, max_height))
            combined_img.paste(img1, (0, 0))
            combined_img.paste(img2, (img1.width, 0))

            # Set page size based on combined image size
            c.setPageSize((total_width, max_height))
            c.drawImage(combined_img, 0, 0)  # Draw combined image at (0, 0) coordinate
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

    output_pdf = merge_images_to_pdf(input_folder)
    print(f"PDF file '{output_pdf}' has been created.")
