import math

import cv2
import pandas as pd

if __name__ == '__main__':
    # 读取Excel文件
    file_path = "ROI_BOX_4x.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")  # 确保安装openpyxl
    # 获取第一行数据（示例）
    rectangles = []
    for i in range(0, 80):
        row = df.iloc[i].tolist()
        rectangles.append(row)

    # 读取Excel文件
    file_path = "Part2_excel/layer0625.xlsx"
    layer = file_path.split("/")[-1].split(".")[0]
    melt_pool_path = "../PR_Data/MeltPool/Part2/{}/".format(layer)
    df = pd.read_excel(file_path, engine="openpyxl")  # 确保安装openpyxl
    # 获取第一行数据（示例）

    # 创建视频写入器
    output_video = layer + ".mp4"
    fps = 30
    width, height = 610, 450
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码格式
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    img_list = []
    for i in range(0, 80):
        row = df.iloc[:, i].tolist()
        row = [str(int(f)).zfill(8) for f in row if not math.isnan(f)]
        img_list.append(row)

    for idx in range(0, 80):
        x, y, w, h = rectangles[idx]
        lines = img_list[idx]
        for line in lines:
            frame = cv2.imread(melt_pool_path + "{}.jpg".format(line))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            video_writer.write(frame)
    # print(img_list)
    video_writer.release()
    print(f"视频已生成：{output_video}")
