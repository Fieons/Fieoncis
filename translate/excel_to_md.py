import pandas as pd

def excel_to_md(excel_path, md_path):
    # 读取 Excel 文件
    df = pd.read_excel(excel_path)

    # 获取第一列和第二列的数据
    col1 = df["原文"]
    col2 = df["译文"]

    # 创建 Markdown 文件
    md_file = open(md_path, "w")

    # 从上至下轮流遍历两列
    for row in range(df.shape[0]):
        md_file.write(f"{col1[row]}\n{col2[row]}\n\n")

    # 关闭 Markdown 文件
    md_file.close()

if __name__ == "__main__":
    excel_path = "E:\我的坚果云\SciFi media\银河系漫游系列\第一部\第二章\第二章_翻译.xlsx"
    md_path = "E:\我的坚果云\SciFi media\银河系漫游系列\第一部\第二章\第二章_翻译.md"
    excel_to_md(excel_path=excel_path, md_path=md_path)