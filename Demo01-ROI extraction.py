import pandas as pd


def divide_rectangle(x, y, w, h):
    half_w = w / 2
    half_h = h / 2
    sub_rectangles = [
        (x, y, half_w, half_h),  # 左上
        (x + half_w, y, half_w, half_h),  # 右上
        (x, y + half_h, half_w, half_h),  # 左下
        (x + half_w, y + half_h, half_w, half_h)  # 右下
    ]
    return sub_rectangles


# 示例
# 读取Excel文件
if __name__ == '__main__':
    box_list = []
    file_path = "../OR_Data/ROI_BOX.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")  # 确保安装openpyxl
    # 获取第一行数据（示例）
    rectangles = []
    for i in range(0, 20):
        row = df.iloc[i].tolist()
        rectangles.append(row)
    for i, [x, y, w, h] in enumerate(rectangles):
        sub_rects = divide_rectangle(x, y, w, h)
        for idx, rect in enumerate(sub_rects, 1):
            x_new = rect[0]-4
            y_new = rect[1]-4
            w_new = rect[2]+8
            h_new = rect[3]+8
            box = [x_new, y_new, w_new, h_new]
            box_list.append(box)
    # 转换为DataFrame并指定列名
    df = pd.DataFrame(box_list, columns=["x", "y", "w", "h"])
    # 保存为Excel文件（自动按行写入，每个单元占4列）
    df.to_excel("ROI_BOX_4x.xlsx", index=False, engine="openpyxl")