'''
Author: Manohar Mukku
Date: 06.12.2018
Desc: Watershed Segmentation algorithm
GitHub: https://github.com/manoharmukku/watershed-segmentation
'''

import sys
import cv2
import numpy
import matplotlib.pyplot as plt
from datetime import datetime

def neighbourhood(image, x, y):
    # Save the neighbourhood pixel's values in a dictionary
    neighbour_region_numbers = {}
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            if (x+i < 0 or y+j < 0): # If coordinates out of image range, skip
                continue
            if (x+i >= image.shape[0] or y+j >= image.shape[1]): # If coordinates out of image range, skip
                continue
            if (neighbour_region_numbers.get(image[x+i][y+j]) == None):
                neighbour_region_numbers[image[x+i][y+j]] = 1 # Create entry in dictionary if not already present
            else:
                neighbour_region_numbers[image[x+i][y+j]] += 1 # Increase count in dictionary if already present

    # Remove the key - 0 if exists
    if (neighbour_region_numbers.get(0) != None):
        del neighbour_region_numbers[0]

    # Get the keys of the dictionary
    keys = list(neighbour_region_numbers)

    # Sort the keys for ease of checking
    keys.sort()

    if (keys[0] == -1):
        if (len(keys) == 1): # Separate region
            return -1
        elif (len(keys) == 2): # Part of another region
            return keys[1]
        else: # Watershed
            return 0
    else:
        if (len(keys) == 1): # Part of another region
            return keys[0]
        else: # Watershed
            return 0

def watershed_segmentation(image):
    # Convert to grayscale if image has multiple channels
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a list of pixel intensities along with their coordinates
    intensity_list = []
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            # Append the tuple (pixel_intensity, xy-coord) to the end of the list
            intensity_list.append((image[x][y], (x, y)))

    # Sort the list with respect to their pixel intensities, in ascending order
    intensity_list.sort()

    # Create an empty segmented_image numpy ndarray initialized to -1's
    segmented_image = numpy.full(image.shape, -1, dtype=int)

    # Iterate the intensity_list in ascending order and update the segmented image
    region_number = 0
    for i in range(len(intensity_list)):
        # Print iteration number in terminal for clarity
        sys.stdout.write("\rPixel {} of {}...".format(i, len(intensity_list)))
        sys.stdout.flush()

        # Get the pixel intensity and the x,y coordinates
        intensity = intensity_list[i][0]
        x = intensity_list[i][1][0]
        y = intensity_list[i][1][1]

        # Get the region number of the current pixel's region by checking its neighbouring pixels
        region_status = neighbourhood(segmented_image, x, y)

        # Assign region number (or) watershed accordingly, at pixel (x, y) of the segmented image
        if (region_status == -1): # Separate region
            region_number += 1
            segmented_image[x][y] = region_number
        elif (region_status == 0): # Watershed
            segmented_image[x][y] = 0
        else: # Part of another region
            segmented_image[x][y] = region_status

    # Return the segmented image
    return segmented_image


def main():
    # Read the input image
    directory = r"E:\1. Documente Facultate\_Master SIVA Anul 1, SEM 2\CV2\foreground_background_segmentation_graph_cut"
    image = 'apple.jpg'
    img = cv2.imread(directory + '/resource/' + image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resize = (128, 128)
    img = cv2.resize(img, resize)

    # Perform segmentation using watershed_segmentation on the input image
    start = datetime.now()
    segmented_image = watershed_segmentation(img)
    print('Segmentation time:', datetime.now() - start, 's')

    # Save the segmented image as png to disk
    cv2.imwrite(directory + "/resource\segmented_" + image, segmented_image)

    # Show the segmented image and original image side by side
    img_output = cv2.imread(directory + "/resource\segmented_" + image, 0)
    img_output = cv2.resize(img_output, resize)
    img_output = cv2.cvtColor(img_output, cv2.COLOR_GRAY2RGB)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(img)
    axs[0].set_title('Original image')
    axs[1].imshow(img_output)
    axs[1].set_title('Watershed segmentation result')

    plt.savefig(directory + '/resource/segmentation_' + image)

if __name__ == "__main__":
    main()