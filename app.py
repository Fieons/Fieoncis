# 程序入口
import os
from files_search_milvus import files_query

print("app have started !")

def files_insert_process():
    print("启动文件导入功能")


def files_query_process():
    files_query()


def main():
    while True:
        print("\n请选择要开启的功能:")
        print("1. 文件导入")
        print("2. 文件内容查询")
        print("3. 退出")

        try:
            choice = int(input("\n请输入功能对应的数字:"))
        except ValueError:
            print("输入无效，请输入正确的数字！")
            continue

        if choice == 1:
            files_insert_process()
        elif choice == 2:
            files_query_process()
        elif choice == 3:
            print("程序退出。")
            break
        else:
            print("输入错误,请输入1、2或3!")


if __name__ == "__main__":
    main()

