# -*- coding: UTF-8 –*-
"""
    ====================
    Auther：林雅静
    Time：2023/1/2512:34
    Project:webupdate_smoke
    =========================
"""

import os
from pathlib import Path
#指定文件夹的路径到sql
base_path = r"E:\dowloadftp\01dc\DCT4.0-DCAML-V202201-10-000-20230315\sql"
#指定文件格式，以空格分隔。
search_exts = '.sql .pck .fnc .prc'.split(" ")


#保存文件名的列表


#找到sql文件夹
def findsqldir(path):
    dc_base_path = Path((path).strip())
    keyword = 'sql'.strip()
    base_path = list(dc_base_path.rglob(keyword))[0]
    print(base_path)
    return base_path

#sql根目录文件处理
def findroot(base_path):
    filelist=[]
    ext=".sql"
    ##遍历sql文件夹下的所有文件和目录
    dirFil = os.listdir(base_path)
    ##取出根目录的文件
    for fl in dirFil:
        flpath = os.path.join(base_path, fl)
        if (os.path.isfile(flpath) and flpath[-4:]==ext):
            filelist.append(flpath);
    print("filelist",filelist)
    return filelist

#取出sql文件夹下的指定文件夹的所有文件（递归）
def findrootnext(base_path):
    #要排除的文件夹，以空格分隔。
    exclude_dir ='个性化脚本 行业脚本 03-个性化脚本 02-行业脚本 10-专用脚本 个性化 大数据版1.0 database bsaml-bdata 01-个性化脚本 02-平台脚本'.split(" ")

    filelistnext=[]
    ##遍历sql文件夹下的所有文件和目录
    dirFil = os.listdir(base_path)

    #循环读取list，排除目录
    for i in range(len(exclude_dir)):
        try:
            dirFil.remove(exclude_dir[i])
        except ValueError:
            print('Item not in list')
    print('当前目录下排除部分文件夹以外的所有子目录及文件：', dirFil)

    ##拼接新的地址
    for item in dirFil:
        #目录连接
        nowPath = base_path + '/' + item
        # print("nowPath:",nowPath)
        #遍历目录及其子文件
        for root,dirs,files in os.walk(nowPath):
            for file in files:
                for ext in search_exts:
                    if(file.endswith(ext)):
                        # 使用join函数将文件名称和文件所在根目录连接起来
                        print("sql文件夹下的指定文件夹的所有文件（递归）",os.path.join(root, file))
                        filelistnext.append(os.path.join(root, file));
    return filelistnext


#遍历行业目录及其子文件
def findbshy(base_path,hy):
    filelist=[]
    #拼接行业路径
    JJPath= base_path+ "\行业脚本\基金行业"
    XTPath= base_path+ "\行业脚本\信托行业"
    if hy==1:
        for root,dirs,files in os.walk(JJPath):
            for file in files:
                for ext in search_exts:
                    if(file.endswith(ext)):
                        # 使用join函数将文件名称和文件所在根目录连接起来
                        print("基金行业子文件夹下的所有文件",os.path.join(root, file))
                        filelist.append(os.path.join(root, file));
    else:
        for root,dirs,files in os.walk(XTPath):
            for file in files:
                for ext in search_exts:
                    if(file.endswith(ext)):
                        # 使用join函数将文件名称和文件所在根目录连接起来
                        print("信托行业子文件夹下的所有文件",os.path.join(root, file))
                        filelist.append(os.path.join(root, file));
    return filelist

def findaddhy(base_path,hy):

    #拼接行业路径
    HYRoot= base_path+ r"\02-行业脚本"
    JJPath= base_path+ r"\02-行业脚本\基金行业"
    JJPath1= base_path+ r"\02-行业脚本\证券标准（适用基金、证券、信托）"
    XTPath= base_path+ r"\02-行业脚本\信托行业"
    filelist=findroot(HYRoot)
    if hy==1:
        for root,dirs,files in os.walk(JJPath):
            for file in files:
                for ext in search_exts:
                    if(file.endswith(ext)):
                        # 使用join函数将文件名称和文件所在根目录连接起来
                        print("【基金行业】子文件夹下的所有文件",os.path.join(root, file))
                        filelist.append(os.path.join(root, file));
        for root,dirs,files in os.walk(JJPath1):
            for file in files:
                for ext in search_exts:
                    if(file.endswith(ext)):
                        # 使用join函数将文件名称和文件所在根目录连接起来
                        print("【证券标准（适用基金、证券、信托）】子文件夹下的所有文件",os.path.join(root, file))
                        filelist.append(os.path.join(root, file));
    else:
        for root,dirs,files in os.walk(XTPath):
            for file in files:
                for ext in search_exts:
                    if(file.endswith(ext)):
                        # 使用join函数将文件名称和文件所在根目录连接起来
                        print("【信托行业】子文件夹下的所有文件",os.path.join(root, file))
                        filelist.append(os.path.join(root, file));
    return filelist

def findDCfiles():

    dc_base_path = r"E:\dowloadftp\01dc"
    base_path=str(findsqldir(dc_base_path))
    fileDClist=findroot(base_path)+findrootnext(base_path);
    return fileDClist
    # print('*'*10)
    # print(fileDClist)

def findDCInterfacefiles():
    dcinterface_base_path= r"E:\dowloadftp\02dcinterface"
    base_path=str(findsqldir(dcinterface_base_path))
    findDCInterfacelist=findroot(base_path)+findrootnext(base_path);
    # print('*'*10)
    print(findDCInterfacelist)
    return findDCInterfacelist


def findbsfiles(hy):
    bs_base_path = r"E:\dowloadftp\03BS"
    base_path=str(findsqldir(bs_base_path))
    filebslist=findroot(base_path)+findrootnext(base_path)+findbshy(base_path,hy);
    # print('*'*10)
    # print(filebslist)
    return filebslist

def findFXQfiles():
    FXQ_base_path=r"E:\dowloadftp\04fxq"
    base_path=str(findsqldir(FXQ_base_path))
    findFXQlist=findroot(base_path)+findrootnext(base_path);
    # print('*'*10)
    # print(findFXQlist)
    return findFXQlist

def findADDfiles(hy):
    add_base_path=r"E:\dowloadftp\05add"
    base_path=str(findsqldir(add_base_path))
    findADDfiles=findroot(base_path)+findrootnext(base_path)+findaddhy(base_path,hy);
    print('*'*10)
    print(findADDfiles)
    return findADDfiles

def BSALLfiles(hy):
    bsallfiles= findDCfiles()+findDCInterfacefiles()+findbsfiles(hy)+findFXQfiles()+findADDfiles(hy)
    print(bsallfiles)
    return bsallfiles

#list拼接@字符
def findfilefinal(filelist,hy):
    sqlstring=r"@"
    filelistfinal=[]
    #循环读取list，拼接字符串
    for i in range(len(filelist)):
        filelistfinal.append(sqlstring+(filelist[i]))
    print(filelistfinal)
    #写入sql文件
    str='\n'
    if hy== 1 :
        f=open(r"E:\dowloadftp\installbsjj.sql", 'w')
    else:
        f=open(r"E:\dowloadftp\installbsxt.sql", 'w')
    f.write('set define off;\n')
    f.write(str.join(filelistfinal))
    f.close


if __name__ == "__main__":

    findfilefinal(BSALLfiles(1),1)
    findfilefinal(BSALLfiles(2),2)
    # findDCfiles()
    # findDCInterfacefiles()
    # findADDfiles()
    # findfilefinal()
    # getAllContent()
    # getSpecContent()
    # findfile(r'E:\00环境部署\01-测试安装包\1.9测试包升级\03-BS\DCT4.0-BSAML-V202201-09-000-20230215\sql')
