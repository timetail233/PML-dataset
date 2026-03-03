import os
from itertools import zip_longest

import cv2
import pandas as pd


def is_point_in_rect(px, py, x, y, w, h):
    return (x <= px <= x + w) and (y <= py <= y + h)


def analyze_vectors(vector_list):
    if not vector_list:
        return None, None, None  # 处理空列表的情况

    lengths = [len(vector) for vector in vector_list]
    max_length = max(lengths)
    min_length = min(lengths)
    avg_length = sum(lengths) / len(lengths)

    return max_length, min_length, avg_length


if __name__ == '__main__':
    # 读取Excel文件
    file_path = "ROI_BOX_4x.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")  # 确保安装openpyxl
    # 获取第一行数据（示例）
    rectangles = []
    for i in range(0, 80):
        row = df.iloc[i].tolist()
        rectangles.append(row)

    area_threshold = 10
    layer_list = os.listdir("../PR_Data/MeltPool/Part2/")
    use_layer_list = os.listdir("../PR_Data/MeltPool_LunKuo/Part2")
    for layer_name in use_layer_list:
        layer = layer_name.replace(".png", "")
        melt_pool_path = "../PR_Data/MeltPool/Part2/{}/".format(layer)
        lines = os.listdir(melt_pool_path)
        idx_num = []
        for i in range(0, 80):
            idx_num.append([])
        for line in lines:
            img_path = melt_pool_path + line
            gray_img = cv2.imread(img_path, 0)
            _, binary = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
            # 查找轮廓
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != 0:
                # 提取面积最大的轮廓
                max_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(max_contour)
                M = cv2.moments(max_contour)
                if area > area_threshold and M["m00"] > 0:
                    px, py = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    for target_idx in range(0, 80):
                        x, y, w, h = rectangles[target_idx]
                        if is_point_in_rect(px, py, x, y, w, h):
                            save_list = idx_num[target_idx]
                            save_list.append(int(line.replace(".jpg", "")))
                            idx_num[target_idx] = save_list

        max_len, min_len, avg_len = analyze_vectors(idx_num)
        print(f"{layer} -- 最长向量的长度: {max_len},最短向量的长度: {min_len},所有向量的平均长度: {avg_len:.2f}")
        with open('Box_list.txt', 'a') as file:
            file.write(f"{layer}:max_len={max_len},min_len={min_len},avg_len={avg_len:.2f}\n")
        # 数据对齐：用None填充不等长部分
        aligned_data = list(zip_longest(*idx_num, fillvalue=None))
        # 创建带列名的DataFrame
        # columns = [f"Vector_{i + 1}" for i in range(16)]
        df = pd.DataFrame(aligned_data)
        # 保存为Excel（自动处理None值为空单元格）
        df.to_excel("Part2_excel/{}.xlsx".format(layer), index=False, engine="openpyxl")
