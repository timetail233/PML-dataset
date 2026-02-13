import cv2
import numpy as np

npy_file = "layer0513_Box14.npy"
npy = np.load(npy_file)
print(npy.shape)
for i in range(0, 5):
    print(npy.shape)
    img = npy[i, :, :, :]
    img = (img * 255).astype(np.uint8)
    # 先调整维度顺序，再转换通道（如果是RGB格式）
    display_img = np.transpose(img, (1, 2, 0))
    cv2.imshow('Image', display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()