import cv2
img1 = cv2.imread("model1.jpg")
img2 = cv2.imread("background1.jpg")
print("rest")
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]


result1 = cv2.bitwise_and(img1, img1, mask=thresh2)
result2 = cv2.bitwise_and(img2, img2, mask=255-thresh2)
result = cv2.add(result1, result2)

cv2.imshow("img", result)
cv2.imshow("img1", result1)
cv2.imshow("img2", result2)

cv2.waitkey(0)

