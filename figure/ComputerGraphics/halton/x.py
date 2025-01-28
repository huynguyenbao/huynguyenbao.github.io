import cv2

img1 = cv2.imread("permute.png")
size = 100
start1 = 362
start2 = 300
img2 = img1[start1 : start1 + size, start2 : start2 + size]
cv2.imwrite("crop_permute.png", img2)
