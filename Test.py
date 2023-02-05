# -*- coding: UTF-8 –*-
import paramiko
# from unrar import rarfile
import os
import configparser
import datetime as datetime
import logging
from logging import handlers
import zipfile
import rarfile
import shutil
from jfrog_artifactory_pro import Download
from unRarFile import unrar_file
LOCAL_ZIP_PATH = ['E:\\开发部署工具\\4.0\\SCM40-合规升级包(基于V202204-0-0)_V202204-2-0V202212080318.zip']
global LOCAL_PATH
LOCAL_PATH = "E:/00环境部署/01-测试安装包/1.9测试包升级/02-dc-interface/DCT4.0-AMLinterface-V202201-09-000-20230215/sql"

global DELETE_PATH
DELETE_PATH="D:/apache-tomcat-7.0.90/applications/bsaml"

DELETE_DIR='proscript 公共脚本 行业脚本'.split(" ")
#print(DELETE_DIR)

global TNSNAME
TNSNAME = "BS38.95"
global USER_PWD
USER_PWD = "bsaml"

LINES_START = '''@echo off
color a
:loop
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *     恒生4.1反洗钱系统2021基线升级                        *
echo *                                                          *
echo *                                                          *
echo ************************************************************
echo.
title 恒生反洗钱系统升级
set /p hsconuser=请输入用户名:
set /p hsconpwd=请输入密码：
set /p tnsname=请输入数据库别名：

:choose
echo.
echo ************************************************************
echo *                                                          *
echo * 请选择升级的系统和行业:                        			*
echo *     1－BS基金                     						*
echo *     2－BS信托 											*
echo *     3－CS基金											*
echo *     4－CS信托											*											*
echo *     C－退出安装                                          *
echo *                                                          *
echo ************************************************************
echo.
set /p dropbackflag=如果输入"C"将退出升级过程:
if %dropbackflag%==C goto end
if %dropbackflag%==c goto end
if %dropbackflag%==1 goto installbsjj
if %dropbackflag%==2 goto installbsxt
if %dropbackflag%==3 goto installcsjs
if %dropbackflag%==4 goto installcsxt
goto end


:installbsjj
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             正在升级:BS基金-2021基线                              *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsjj.sql %tnsname% %hsconpwd% %hsconuser% 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "警告" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

:installbsxt
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             正在升级:BS信托-2021基线                              *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsxt.sql %tnsname% %hsconpwd% %hsconuser% 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "警告" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

if %errorlevel% == 0 (
echo.
echo ************************************************************
echo *                                                          *
echo *        升级完毕，但出现错误，请查看上面错误信息          *
echo *                                                          *
echo ************************************************************
echo.
goto end
) else (
echo.
echo ************************************************************
echo *                                                          *
echo *                         升级成功                         *
echo *                                                          *
echo ************************************************************
echo.
goto finsh
)
:finsh
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *              恒生反洗钱4.1-2021基线升级完毕              *
echo *                                                          *
echo *                                                          *
echo ************************************************************
echo.
goto end
:end
echo 按任意键退出
pause > nul
    '''
LINES_END = '''type .\log\install.log | find /i /n "ora-" > .\log\install.txt
        type .\log\install.log | find /i /n "警告" >> .\log\install.txt
        type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
        '''

class Public:
    # def re_name1(self):
    #     filename = "E:/01"
    #     newname="E:/02"
    #     os.rename(filename,newname)


    # def un_zip(self):
    #     file_name = "F:/dowloadftp/DCT4.0-BSAML-V202201-08-000-20221228.202212140627(cz)/BSAMLApp/bsaml.zip"
    #     file_name1 = "F:/dowloadftp/DCT4.0-BSAML-V202201-08-000-20221228.202212140627(cz)/BSAMLApp/bsaml"
    #     rar = zipfile.ZipFile(file_name)
    #
    #     rar.extractall(file_name1)
    #
    #     rar.close()
    # def unrarfile(self):
    #     # from unRarFile import unrar_file
    #     for rarname in self.res_service:
    #
    #         # unrar_file(log.logger, rarname, LOCAL_PATH)
    #         oldName = ''
    #         zip_file_contents = zipfile.ZipFile(rarname, 'r')
    #         for file in zip_file_contents.namelist():
    #             if oldName == '':
    #                 oldName = LOCAL_PATH + "/" + file
    #             fileName = file.encode('cp437').decode('gbk')  # 先使用cp437编码，然后再使用gbk解码
    #             # print(file)
    #             zip_file_contents.extract(file, LOCAL_PATH)  # 解压缩ZIP文件
    #             os.chdir(LOCAL_PATH)  # 切换到目标目录
    #             os.rename(file, fileName)  # 重命名文件
    #         zip_file_contents.close()
    #         # shutil.rmtree(oldName)  # 删除旧文件夹




    def newbatrun(self):
        for localPatchName in LOCAL_ZIP_PATH:

            batFile = localPatchName.split('.zip')[0]  + '\\install.bat'
            print("batFile",batFile)
            installbatNew = localPatchName.split('.zip')[0] + '\\installNew.bat'
            installbat = open(batFile, 'r')
            installbatNewFile = open(installbatNew, 'w+')
            new_lines = ''
            #用于移动文件的读取指针到指定位置
            installbat.seek(0)
            # print("=========installbat==============",installbat.seek(0))
            # print("=========END installbat==============")
            for line in installbat:
                if '用户的密码' in line:
                    line = line.replace(' /p ', ' ')
                    # print(line)
                    line = line.split('=')[0] + '=' + USER_PWD + '/n'
                    # print(line)
                    new_lines = new_lines + line

                if '数据库别名' in line:
                    line = line.replace(' /p ', ' ')
                    line = line.split('=')[0] + '=' + TNSNAME + '/n'
                    new_lines = new_lines + line

                if 'Install.sql' in line or 'install.sql' in line:
                    new_lines = new_lines + line
            new_lines = LINES_START + new_lines + LINES_END
            print("===new_lines==",new_lines)
            print("===END new_lines==",new_lines)
            installbatNewFile.seek(0)
            installbatNewFile.truncate()
            installbatNewFile.write(new_lines)
            # installbatNewFile.flush()
            installbat.close()
            installbatNewFile.close()

            os.chdir(localPatchName.split('.zip')[0])
            # print localPatchName.split('.zip')[0].encode('gb2312')
            os.system('call installNew.bat')
            # log.logger.info('升级{0}完毕'.format(localPatchName))





if __name__ == '__main__':
    public=Public()
    # public.re_name1()
    # public.un_rar()
    # public.clean_local()
    # public.getAlldirInDiGui(r"E:/00环境部署/00-21年所有/21年BS基线/DCT4.0-BSAMLFxq.V202101.00.000/sql")
    # public.getAllContent(r"E:\00环境部署\00-21年所有\21年BS基线\DCT40-BSAML-V202101-00-000(20210330)\sql\行业脚本\信托\信托行业-BS")
    # public.newbatrun()
    public.getSpecContent(r"E:/00环境部署/01-测试安装包/1.9测试包升级/03-BS/DCT4.0-BSAML-V202201-09-000-20230215/sql")
