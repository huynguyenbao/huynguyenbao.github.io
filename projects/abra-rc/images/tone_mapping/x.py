import cv2

img1 = cv2.imread("after.jpeg")
size = 256
start1 = 370
start2 = 120
img2 = img1[start1 : start1 + size, start2 : start2 + size]
cv2.imwrite("crop_after.jpeg", img2)
