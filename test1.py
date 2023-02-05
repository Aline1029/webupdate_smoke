# -*- coding: UTF-8 –*-
"""
    ====================
    Auther：林雅静
    Time：2023/1/2512:34
    Project:webupdate_smoke
    =========================
怎么用
指定文件夹的路径。
指定文件格式，以空格分隔。
指定的关键词，以空格分隔。
"""

import os

base_path = "E:/00环境部署/01-测试安装包/1.9测试包升级/03-BS/DCT4.0-BSAML-V202201-09-000-20230215/sql"
search_exts = '.sql .pkg'.split(" ")
search_word = 'proscript 公共脚本 行业脚本'.split(" ")

def find():
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            for ext in search_exts:
                if(filename.endswith(ext)):
                    file = os.path.join(root, filename)
                    search_file(file, search_word)

def search_file(file, word):
    with open(file, 'r',encoding='gb18030', errors='ignore') as f:
        #可列出序列和下标位置对应的值
        for num, content in enumerate(f.readlines(), 1):
            for key in word:
                if str(key) in content:
                    print(f'found <{content}> at Line {num} in file: {file}')


if __name__ == "__main__":
    find()
