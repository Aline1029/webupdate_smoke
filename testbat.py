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
