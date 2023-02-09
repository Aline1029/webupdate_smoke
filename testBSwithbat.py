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
base_path = r"E:\00环境部署\01-测试安装包\1.9测试包升级\03-BS\DCT4.0-BSAML-V202201-09-000-20230215\sql"
#指定文件格式，以空格分隔。
search_exts = '.sql .pck .fnc .prc'.split(" ")
#要排除的文件夹，以空格分隔。
exclude_dir ='个性化脚本 行业脚本'.split(" ")
print(exclude_dir)
#保存文件名的列表
filelist=[]
#行业
hy=1
global LINES_START
global LINES_END

LINES_START = '''@echo off
    color a
    :loop
    echo.
    echo ************************************************************
    echo *                                                          *
    echo *                                                          *
    echo *      恒生4.1反洗钱系统BS开始升级                                          *
    echo *                                                          *
    echo *                                                          *
    echo ************************************************************
    echo.
    title 恒生反洗钱系统4.1BS升级
    set /p hsconuser=请输入用户名:
    set /p hsconpwd=请输入密码：
    set /p tnsname=请输入数据库别名：
    sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsjj.sql
    '''
LINES_END = '''type .\log\install.log | find /i /n "ora-" > .\log\install.txt
    type .\log\install.log | find /i /n "警告" >> .\log\install.txt
    type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
    '''


def find():
    #sql根目录文件处理
    ext=".sql"
    ##遍历sql文件夹下的所有文件和目录
    dirFil = os.listdir(base_path)
    ##取出根目录的文件
    for fl in dirFil:
        flpath = os.path.join(base_path, fl)
        if (os.path.isfile(flpath) and flpath[-4:]==ext):
            filelist.append(flpath);
    print("files",filelist)

    #取出指定文件夹的所有文件
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
                        print("子文件夹下的所有文件",os.path.join(root, file))
                        filelist.append(os.path.join(root, file));
    #遍历行业目录及其子文件
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


    # print("filelist",filelist)
    return(filelist)



def findfilefinal(filelist):
    sqlstring=r"@"
    filelistfinal=[]
    #循环读取list，拼接字符串
    for i in range(len(filelist)):
        filelistfinal.append(sqlstring+(filelist[i]))
    print(filelistfinal)
    #写入sql文件
    str='\n'
    f=open("installBS.sql", 'w')
    f.write(str.join(filelistfinal))
    f.close

def newbatrun():
    LOCAL_ZIP_PATH = ['E:\\00环境部署\\01-测试安装包\\1.9测试包升级\\03-BS\DCT4.0-BSAML-V202201-09-000-20230215.zip']
    for localPatchName in LOCAL_ZIP_PATH:
        # LOCAL_ZIP_PATH = ['E:\\dowloadftp\\FERM20-平台基础升级包(基于V202003-0-0)_V202003-1-0beta202008090321.zip',
        #                   'E:\\dowloadftp\\SCM40-合规升级包(基于V202003-0-0)_V202003-1-0beta202008070313.zip']
        # batFile = localPatchName.split('.zip')[0] + '/install.bat'
        sqlFile = localPatchName.split('.zip')[0] + '/sql/installBS.sql'
        print(sqlFile)
        installbatNew = localPatchName.split('.zip')[0] + '/sql/installNew.bat'
        sqlFile = open(sqlFile, 'r')
        installbatNewFile = open(installbatNew, 'w+')
        new_lines = ''
        for line in sqlFile:
            new_lines = new_lines + line
        new_lines = LINES_START + new_lines + LINES_END
        # print new_lines
        installbatNewFile.seek(0)
        installbatNewFile.truncate()
        installbatNewFile.write(new_lines)
        sqlFile.close()
        installbatNewFile.close()

        os.chdir(localPatchName.split('.zip')[0])
        # print localPatchName.split('.zip')[0].encode('gb2312')
        os.system('call installNew.bat')

if __name__ == "__main__":
    # find()
    # findfilefinal(find())
    newbatrun()
    # getAllContent()
    # getSpecContent()
    # findfile(r'E:\00环境部署\01-测试安装包\1.9测试包升级\03-BS\DCT4.0-BSAML-V202201-09-000-20230215\sql')
