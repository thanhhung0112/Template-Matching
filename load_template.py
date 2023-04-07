import cv2
import numpy as np
import matplotlib.pyplot as plt

# # Load image as BGR
# img = cv2.imread('Dataset/template_custom.jpg')

# # Convert BGR to RGBA
# rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

# # Set alpha channel to zero for pixels you want to be transparent
# # In this example, we set the alpha channel to zero for all pixels
# rgba[..., 3] = 0

# # Save image as PNG with transparent background
# cv2.imwrite('transparent_template.png', rgba, [cv2.IMWRITE_PNG_COMPRESSION, 0])

# Load the transparent template
template = cv2.imread('transparent_template.png', cv2.IMREAD_UNCHANGED)

# Split the template into its color and alpha components
b, g, r, a = cv2.split(template)

# Threshold the alpha channel to create a binary mask
_, mask = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY)

# Extract the non-transparent part of the template using the binary mask
result = cv2.merge((b & mask, g & mask, r & mask))

# Display the result
plt.imshow(result)
plt.show()


