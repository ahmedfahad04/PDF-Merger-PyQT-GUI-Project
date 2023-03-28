
import fitz
from crop_image import get_cropped_images
from img_to_pdf import merge_pdf


def pdf_to_images(input_pdf, output_dir, ui_obj):
   
    # Open the input PDF
    print('[FILE] ', input_pdf)
    pdf = fitz.open(input_pdf)

    # Iterate through the pages of the input PDF
    for i, page in enumerate(pdf):
        # Extract the page as an image
        pix = page.get_pixmap()
        output = f"{output_dir}/page{i}.png"
        
        # show output to Desktop UI
        ui_obj.edit_status.append("[CONVERTING] converting page {} to image.......".format(i))
        pix.save(output)


def start_conversion(filepath, page_size, ui_obj):
    
    ui_obj.edit_status.append("[MERGING] merging is progress.......\n")
    print("[MERGING] merging is progress.......")
    
    pdf_to_images(filepath, 'temp', ui_obj)
    get_cropped_images()
    merge_pdf(page_size)
    
    ui_obj.edit_status.append("\n[DONE] check 'output' folder for the merged file.......")
    print("[DONE] check output folder for the merged file.......")

