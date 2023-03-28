import os
from PyPDF2 import PdfMerger
from PIL import Image

output_dir = (os.path.join(os.getcwd(), "output"))
image_dir = (os.path.join(os.getcwd(), "temp"))


def del_file(dir, ui_obj):
        
    # Delete the files in directories
    for filename in os.listdir(dir):
                    
        filepath = os.path.join(dir, filename)
        if not filepath:
            continue
        
        os.remove(filepath)


def getImageSize(page_size):
    
    if page_size == 'Legal':
        spacing = 150
        margin = 30

        width = 2596
        height = 4248
        
        bulk = 6
    
    elif page_size == 'A4':
        spacing = 118
        margin = 118

        width = 2480
        height = 3508
        
        bulk = 4
        
    elif page_size == 'A3':
        spacing = 350
        margin = 350

        width = 3505
        height = 4956
        
        bulk = 8
        
    elif page_size == '30x20':
        spacing = 90
        margin = 23

        width = 8991
        height = 5994
        
        bulk = 35
    
    elif page_size == '15x20':
        spacing = 239
        margin = 150

        width = 4496
        height = 5994
        
        bulk = 15
        
    elif page_size == '15x10':
        spacing = 220
        margin = 318

        width = 4496
        height = 2997
        
        bulk = 6      
        
    return spacing, margin, width, height, bulk


def img_pdf(page_size, ui_obj):
    
    del_file(output_dir, ui_obj)

    # Create an image object for each image file
    images = [Image.open(os.path.join(image_dir, filename)) for filename in os.listdir(image_dir)]
    
    spacing, margin, width, height, bulk = getImageSize(page_size=page_size)
    
    # Iterate over the images in groups of bulk
    for i in range(0, len(images), bulk):
               
        # Create a blank image with a white background
        page = Image.new('RGB', (width, height), 'white')
        
        k = 1
        
        # Paste the images into the page
        for j in range(bulk):
            
            if i + j >= len(images):
                break
            
            if page_size == '30x20':                

                if j<7:
                    page.paste(
                        images[i+j], 
                        ( (int)((images[0].width+spacing)*(j%7)+80) , 
                        50 
                        )
                    )
                    print("UP: ", (int)(images[0].width*j+spacing), 0)                    
                    
                else:
                    
                    page.paste(
                        images[i+j], 
                        ( (int)((images[0].width+spacing)*(j%7)+80), 
                        (int)((images[0].height+80)*(j//7)) +50
                        )
                    )
                    print("DOWN: ", (int)(images[0].width*(j%3)+spacing+margin),(int)(images[0].height))
                    k += 1 
                    
            elif page_size == '15x20':
                
                if j<3:
                    page.paste(
                        images[i+j], 
                        ( (int)((images[0].width+spacing)*(j%3)+margin) , 
                        20 
                        )
                    )
                    print("UP: ", (int)(images[0].width*j+spacing), 0)                    
                    
                else:
                    
                    page.paste(
                        images[i+j], 
                        ( (int)((images[0].width+spacing)*(j%3)+margin), 
                        (int)((images[0].height+10)*(j//3)) + 20 
                        )
                    )
                    print("DOWN: ", (int)(images[0].width*(j%3)+spacing+margin),(int)(images[0].height))
                    k += 1
                    
            elif page_size == '15x10':
                
                if j<3:
                    page.paste(
                        images[i+j], 
                        ( (int)((images[0].width+spacing)*(j%3)+margin) , 
                        80 
                        )
                    )
                    print("UP: ", (int)(images[0].width*j+spacing), 0)                    
                    
                else:
                    
                    page.paste(
                        images[i+j], 
                        ( (int)((images[0].width+spacing)*(j%3)+margin), 
                        (int)((images[0].height+margin)*(j//3)) + 80
                        )
                    )
                    print("DOWN: ", (int)(images[0].width*(j%3)+spacing+margin),(int)(images[0].height))
                    k += 1
                    
            elif page_size == 'A4':
                
                if j%2 == 0:
                    page.paste(
                        images[i+j], 
                        ( 30 , 
                        (int) (images[0].height+margin+spacing)*(j-k+1) + 50
                        )
                    )
                    print("EVEN: ", 0, (images[0].height+spacing)*(j-k+1))
                    
                else:
                    page.paste(
                        images[i+j], 
                        ( (int)(images[0].width+80), 
                        (int)(images[0].height+margin+spacing)*(j-k) + 50
                        )
                    )
                    print("ODD: ", (images[0].width+spacing), (images[0].height+spacing)*(j-k))
                    k += 1
            
            else:
     
                if j%2 == 0:
                    page.paste(
                        images[i+j], 
                        ( margin , 
                        (int) (images[0].height+40)*(j-k+1)+40 
                        )
                    )
                    print("EVEN: ", 0, (images[0].height+spacing)*(j-k+1))
                    
                else:
                    page.paste(
                        images[i+j], 
                        ( (int)(images[0].width+spacing+margin), 
                        (int)(images[0].height+40)*(j-k) +40
                        )
                    )
                    print("ODD: ", (images[0].width+spacing), (images[0].height+spacing)*(j-k))
                    k += 1
                

        # Save the page to a PDF file     
        page.save('{}/output_{}.pdf'.format(output_dir, i), 'PDF', resolution=300.0, quality=95, dpi=(300, 300))
        ui_obj.edit_status.append("[CONVERTING] converting image to pdf.......")
        
        print("Page: ", i)

def merge_pdf(page_size, ui_obj):
    
    img_pdf(page_size, ui_obj)
    
    # Create a PDF file merger
    merger = PdfMerger()

    # Loop through the PDF files in the directory
    for filename in os.listdir(output_dir):
        # Skip non-PDF files
        if not filename.endswith('.pdf'):
            continue

        # Add the PDF file to the merger
        filepath = os.path.join(output_dir, filename)
        merger.append(filepath)

    # Save the merged PDF file
    output_file_name = 'merged_'+page_size+'.pdf'
    merged_filepath = os.path.join(output_dir, output_file_name)
    merger.write(merged_filepath)
    # Close the merger
    merger.close()

    # Delete the files in directories
    for filename in os.listdir(output_dir):
        
        if filename.endswith('.pdf') and filename != output_file_name:
            filepath = os.path.join(output_dir, filename)
            os.remove(filepath)