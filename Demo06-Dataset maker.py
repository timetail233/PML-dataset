import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


# 保存函数
def save_as_images(arr, folder):
    for i in range(arr.shape[0]):
        img = arr[i]
        img = (img * 255).astype(np.uint8)
        cv2.imwrite(f"{folder}/{i:03d}.png", img)


if __name__ == '__main__':
    files_path = "DataForML_meltpool/train/"
    lines = os.listdir(files_path)
    for npy_name in tqdm(lines):
        npy_path = files_path + npy_name
        img_list = np.load(npy_path)
        area_list = []
        for i in range(0, len(img_list)):
            img = img_list[i, :, :]
            img = (img * 255).astype(np.uint8)
            _, binary = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
            # 查找轮廓
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != 0:
                # 提取面积最大的轮廓
                max_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(max_contour)
                if area > 0:
                    area_list.append(area)
                else:
                    area_list.append(0)
            else:
                area_list.append(0)

        # 核心排序操作
        sorted_indices = np.argsort(area_list)  # 获取排序后的索引
        sorted_data = img_list[sorted_indices]  # 按索引重新排列数据
        save_path = npy_path.replace("pool", "pool_sort")
        np.save(save_path,sorted_data)
