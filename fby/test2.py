# -*- coding: UTF-8 –*-
"""
    ====================
    Auther：林雅静
    Time：2023/1/2512:34
    Project:webupdate_smoke
    =========================
"""

import os
#指定文件夹的路径到sql
base_path = r"E:\0"
#指定文件格式，以空格分隔。
search_exts = '.sql .pkg .txt  '.split(" ")
#要排除的文件夹，以空格分隔。
exclude_dir ='01 02'.split(" ")
print(exclude_dir)


def find():
#保存文件名的列表
    filelist=[]
    ext=".txt"
    sqlstring=r"@.\ "


    #遍历sql文件夹下的所有文件和目录
    dirFil = os.listdir(base_path)
    #取出根目录的文件
    for fl in dirFil:
        flpath = os.path.join(base_path, fl)
        if (os.path.isfile(flpath) and flpath[-4:]==ext):
            filelist.append(flpath);
    print("files",filelist)



    #循环读取list，排除目录
    for i in range(len(exclude_dir)):
        try:
            dirFil.remove(exclude_dir[i])
        except ValueError:
            print('Item not in list')
    print('当前目录下排除部分文件夹以外的所有子目录及文件：', dirFil)

    #拼接新的地址
    for item in dirFil:
        #目录连接
        nowPath = base_path + '/' + item
        # print("nowPath:",nowPath)


        #遍历目录及其子文件
        for root,dirs,files in os.walk(nowPath):
            for file in files:
                # 使用join函数将文件名称和文件所在根目录连接起来
                print("子文件夹下的所有文件",os.path.join(root, file))
                filelist.append(os.path.join(root, file));

    print("filelist",filelist)






def findfile(path):
    for root, dirs, files in os.walk(path):
        print("===root绝对路径===")
        print(root)

        print("===DIRS文件夹===")
        print(dirs)

        print("===files文件===")
        print(files)


#将文件夹下的所有目录及文件读取出来
def getAllContent():
    # dirFil = 列出当前文件夹下的所有文件夹及文件
    dirFil = os.listdir(base_path)
    print('当前目录下所有子目录及文件：', dirFil)
    dirFil.remove('02')

    for root,dirs,files in os.walk(base_path):
        # print("root:",root)
        # print("dirs:",dirs)
        # print("files:",files)
        for file in files:
            # 使用join函数将文件名称和文件所在根目录连接起来
            print(os.path.join(root, file))
# def getAllContent1():
#     # dirFil = 列出当前文件夹下的所有文件夹及文件
#     dirFil = os.listdir(base_path)
#     print('当前目录下所有子目录及文件：', dirFil)
#     for item in dirFil:
#         #目录连接
#         nowPath = base_path + '/' + item
#         state = any(name.endswith('.py') for name in filenames)
#         print("nowPath",nowPath)
#         for root,dirs,files in os.walk(base_path):
#             for dir in dirs:
#                 if dir in search_dir:
#                     for file in files:
#                         # 使用join函数将文件名称和文件所在根目录连接起来
#                         print(os.path.join(root, file))
#指定文件目录：去除【个性化脚本】
def getSpecContent():
    # dirFil = 列出当前文件夹下的所有文件夹及文件
    dirFil = os.listdir(base_path)
    try:
        dirFil.remove('02')
    except ValueError:
        print('Item not in list')
    print('当前目录下所有子目录及文件：', dirFil)
    # for item in dirFil:
    #     #目录连接
    #     nowPath = path + '/' + item
    #     print(nowPath)
    for root,dirs,files in os.walk(base_path):
        for file in files:

            # 使用join函数将文件名称和文件所在根目录连接起来
            print(os.path.join(root, file))

#
# #递归遍历目录
#     def getAlldirInDiGui(self,path):
#         for root,dirs,files in os.walk(path):
#             for file in files:
#             # 使用join函数将文件名称和文件所在根目录连接起来
#                 print(os.path.join(root, file))


if __name__ == "__main__":
    find()
    # getAllContent()
    # getSpecContent()
    # findfile(r'E:\00环境部署\01-测试安装包\1.9测试包升级\03-BS\DCT4.0-BSAML-V202201-09-000-20230215\sql')
