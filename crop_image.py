import os
import cv2
import numpy as np

def crop_image(image_path, ui_obj, img_id):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the edges of the image using Canny edge detection
    edges = cv2.Canny(gray, 50, 100)

    # Find the contours of the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Find the bounding box of all the contours
    bounding_boxes = [cv2.boundingRect(c) for c in contours]

    # Find the bounding box that contains all the bounding boxes
    left = min(x for (x, _, _, _) in bounding_boxes)
    top = min(y for (_, y, _, _) in bounding_boxes)
    right = max(x + w for (x, _, w, _) in bounding_boxes)
    bottom = max(y + h for (_, y, _, h) in bounding_boxes)

    # Crop the image to the bounding box
    edited_image = image[top:bottom, left:right]
    resized_image = cv2.resize(edited_image, (1109, 809)) # A4

    # Add 200px of white space at the bottom of the image
    white_space = np.ones((300, resized_image.shape[1], 3), dtype=np.uint8) * 255
    resized_image = np.concatenate((resized_image, white_space), axis=0)

    # Add a 35.4px border around the image
    border_thickness = 34
    border_color = (255, 255, 255) # white
    resized_image = cv2.copyMakeBorder(resized_image, border_thickness, border_thickness, border_thickness, border_thickness, cv2.BORDER_CONSTANT, value=border_color, dst=None)
    resized_image = cv2.resize(resized_image, (1180, 1180))
    
    border_color = (0, 0, 0) # white
    resized_image = cv2.copyMakeBorder(resized_image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=border_color, dst=None)
    resized_image = cv2.resize(resized_image, (1181, 1181))

    # print("TOP: {}, BOTTOM: {}, LEFT: {}, RIGHT: {}".format(top, bottom, left, right))
    # cv2.imwrite(os.path.join(os.getcwd(), "temp", "cropped_{}.png".format(img_id)), resized_image)
    print(resized_image.shape)
    ui_obj.edit_status.append("[CROPPING] cropping image {} .......".format(img_id))
    return resized_image




def get_cropped_images(ui_obj):
    image_dir = (os.path.join(os.getcwd(), "temp"))

    img_id = 1
    # Loop through the images in the directory
    for filename in os.listdir(image_dir):
        # Skip non-image files
        if not filename.endswith('.png'):
            continue

        # Load the image
        filepath = os.path.join(image_dir, filename)

        # Trim the whitespaces from the image
        trimmed_image = crop_image(filepath, ui_obj, img_id)
        img_id += 1
        
        # Save the trimmed image
        cv2.imwrite(filepath, trimmed_image)
