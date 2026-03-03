import cv2
import pandas as pd

image = cv2.imread("../PR_Data/MeltPool_LunKuo/Part2/layer0171.png")
box_list = []
file_path = "ROI_BOX_4x.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")  # 确保安装openpyxl
rectangles = []
for i in range(0, 80):
    row = df.iloc[i].tolist()
    rectangles.append(row)

for i in range(0, 80):
    vis = image.copy()
    for idx, [x, y, w, h] in enumerate(rectangles):
        color = (255, 0, 0) if i != idx else (0, 255, 255)
        cv2.rectangle(vis, (x, y), (x + w, y + h), color, 2)
    cv2.imshow("Result", vis)
    cv2.waitKey(0)
