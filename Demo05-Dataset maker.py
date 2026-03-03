import math
import os

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    src_file = "Part2_excel_sample_n32/"
    lines = os.listdir(src_file)
    print(lines)
    half_size = 32
    save_path = "DataForML/"
    for line in tqdm(lines):
        layer = line.replace(".xlsx", "")
        melt_pool_path = "../PR_Data/MeltPool/Part2/{}/".format(layer)
        file_path = src_file + line
        df = pd.read_excel(file_path, engine="openpyxl")  # 确保安装openpyxl
        img_list = []
        for i in range(0, 80):
            row = df.iloc[:, i].tolist()
            row = [str(int(f)).zfill(8) for f in row if not math.isnan(f)]
            img_list.append(row)

        for idx in range(0, 80):
            img_path = img_list[idx]
            cropped_images = []
            output_path = save_path + "{}_Box{}.npy".format(layer, idx)
            if os.path.exists(output_path):
                continue
            for img_name in img_path:
                gray_img = cv2.imread(melt_pool_path + "{}.jpg".format(img_name), 0)
                _, binary = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
                # 查找轮廓
                contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                max_contour = max(contours, key=cv2.contourArea)
                M = cv2.moments(max_contour)
                x, y = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # 计算裁剪边界（防止越界）
                top = max(0, y - half_size)
                bottom = y + half_size
                left = x - half_size
                right = x + half_size
                # 执行裁剪
                cropped = gray_img[top:bottom, left:right]
                cropped_images.append(cropped)
            if len(cropped_images) != 32:
                pad_num = 32 - len(cropped_images)
                for i in range(0, pad_num):
                    cropped_images.append(np.zeros((64, 64)))
            channels = []
            if len(cropped_images) != 32:
                print("error")
            for cropped in cropped_images:
                # 3. 归一化到 [0, 1] 范围
                img_normalized = cropped.astype(np.float32) / 255.0
                # 4. 扩展为3D张量 (H x W x 1)
                img_expanded = np.expand_dims(img_normalized, axis=0)
                channels.append(img_expanded)
            # 5. 按通道拼接 (H x W x C)
            # print(channels)
            tensor = np.concatenate(channels, axis=0)
            # 6. 保存为.npy文件
            output_path = save_path + "{}_Box{}.npy".format(layer, idx)
            np.save(output_path, tensor)
