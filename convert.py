import os
import sys
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

def merge_images_to_pdf(input_folder, images_per_page=2):
    output_pdf = generate_output_filename(input_folder)
    c = canvas.Canvas(output_pdf, pagesize=landscape(A4))

    # Get list of image files in the input folder
    image_paths = [os.path.join(input_folder, file) for file in sorted(os.listdir(input_folder)) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    # Calculate the total number of images
    num_images = len(image_paths)

    # Calculate the number of pages needed
    num_pages = num_images // images_per_page + min(1, num_images % images_per_page)

    for i in range(num_pages):
        c.setPageSize(landscape(A4))
        c.saveState()

        # Calculate coordinates for three images on one page
        page_width, page_height = landscape(A4)
        x_offset = 10
        y_offset = 30
        image_width = (page_width - (images_per_page+1) * x_offset) / images_per_page
        image_height = page_height - 2 * y_offset

        for j in range(images_per_page):
            image_index = i * images_per_page + j
            if image_index < num_images:
                image_path = image_paths[image_index]
                img = Image.open(image_path)
                width, height = img.size
                aspect_ratio = width / height

                if aspect_ratio > 1:  # Landscape orientation
                    new_width = image_width
                    new_height = new_width / aspect_ratio
                else:  # Portrait orientation
                    new_height = image_height
                    new_width = new_height * aspect_ratio

                x_position = j * (x_offset + image_width) + x_offset
                y_position = y_offset
                c.drawImage(image_path, x_position, y_position, width=new_width, height=new_height)

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
