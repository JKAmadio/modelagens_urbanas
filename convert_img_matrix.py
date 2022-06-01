import cv2

path_to_image = './image.png'
img = cv2.imread(path_to_image)
resized = cv2.resize(img, (20, 20), cv2.INTER_LINEAR)
print(resized)
