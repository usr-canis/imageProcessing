import numpy as np
import cv2

def modified_mean_filter(image, window_size):
    height, width = image.shape[:2]
    border = window_size // 2 # cause processing pixel is at center
    filtered_image = np.copy(image)

    for i in range(border, height - border):
        for j in range(border, width - border):
            pixel = image[i, j]
            print("processing pixel","(",i,",",j,")","image height and width are ",height,",",width)
            window = image[i-border:i+border+1, j-border:j+border+1]
            
            if pixel == 0 or pixel == 255:
                if np.any(window != pixel) and np.any(window != 255-pixel):
                    non_noisy_pixels = window[(window != pixel) & (window != 255-pixel)]
                    if non_noisy_pixels.size > 0:
                        trimmed_mean = np.mean(np.sort(non_noisy_pixels)[1:-1])
                        winsorized_mean = np.mean(np.clip(non_noisy_pixels, pixel+1, 255-pixel-1))
                        filtered_image[i, j] = trimmed_mean 


    return filtered_image

noiseimage=input("Enter the image path to filter:")
image = cv2.imread(noiseimage, 0) 

if image is None:
    print("Error loading the image.")
else:
    filtered_image = modified_mean_filter(image, window_size=5)

    cv2.imshow('Original Image', image)
    cv2.imshow('Filtered Image', filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    