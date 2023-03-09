# -*- coding: utf-8 -*-
import time

import os

import logging
from datetime import datetime
from logging import handlers
import zipfile
import rarfile
import shutil

from jfrog_artifactory_pro import Download
import FileFind
from Public import *

global LINES_START
global LINES_END



LINES_START = '''@echo off
color a
:loop
echo.
echo ************************************************************
echo *                                                          *
echo *                                                         	*
echo *     恒生4.1反洗钱系统BS                                	    *
echo *                                                          *
echo *                                                          *
echo ************************************************************
echo.
title 恒生4.1反洗钱系统升级
    '''
LINES_END = ''':choose
echo.
echo ************************************************************
echo *                                                          *
echo * 请选择升级的系统和行业:                        		        *
echo *     1－BS基金                     			            *
echo *     2－BS信托 				                            *
echo *     3－CS基金					                            *
echo *     4－CS信托					                            *											
echo *     C－退出安装                                          	*
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
echo *             正在升级:BS基金                                 *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsjj.sql 
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
echo *             正在升级:BS信托                                *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsxt.sql 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "警告" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

if %errorlevel% == 0 (
echo.
echo ************************************************************
echo *                                                         	*
echo *        升级完毕，但出现错误，请查看上面错误信息          	    *
echo *                                                          *
echo ************************************************************
echo.
goto end
) else (
echo.
echo ************************************************************
echo *                                                          *
echo *                         升级成功                    	    *
echo *                                                          *
echo ************************************************************
echo.
goto finsh
)
:finsh
echo.
echo ************************************************************
echo *                                                           	*
echo *                                                           	*
echo *             恒生反洗钱4.1主干升级完毕    	                    *
echo *                                                           	*
echo *                                                           	*
echo ************************************************************
echo.
goto end
:end
echo 按任意键退出
pause > nul
    '''


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)





class ConfigParam:
    # 读取所需要的参数到全局变量中
    def read_param(self):
        # 读取配置
        global BEI_FEN  # 备份路径
        BEI_FEN = Public.readini('beifen', 'path')
        global VERSION  # 当前版本
        VERSION = Public.readini('version', 'version')
        global FERM_PATH  # webapp部署路径
        FERM_PATH = Public.readini('fermpath', 'path')
        global LOCAL_PATH  # 下载到本地路径
        LOCAL_PATH = Public.readini('localpath', 'path')
        # global DELETE_PATH #web刪除路径
        # DELETE_PATH = Public.readini('deleledir','path')

        # global FTP_PATH_DB #DB文件FTP路径
        # FTP_PATH_DB=Public.readini_sec('dbfile',type='2')
        # print("FTP_PATH_DB %s" %FTP_PATH_DB)
        # print('FTP_PATH_DB is {0}'.format(FTP_PATH_DB))
        global FTP_PATH_WEB
        global FILES_WEB_DIR
        global FILES_WEB
        FTP_PATH_WEB = []  # 要下载的ftp全路径
        FILES_WEB_DIR = []  # 下载的文件对应覆盖的文件夹
        FILES_WEB = []  # 要下载的文件名
        # get 上面三个列表
        global baseinfo, download_list,server_name
        baseinfo = eval(Public.readini_sec("baseinfo")[0])
        baseinfo["version"] = VERSION
        download_list = eval(Public.readini_sec("jfrogdownload")[0])
        server_name = eval(Public.readini_sec("servername")[0])
        # tmp = Public.readini_sec('webfiles')
        # #print(len(tmp))
        # i = 0
        # while i < len(tmp):
        #     # print (tmp[i])
        #     t = tmp[i].replace('version', VERSION)
        #     FTP_PATH_WEB.append(t)
        #     t1 =tmp[i].split('/')
        #     FILES_WEB.append(t1[-1])
        #     i += 2
        # #print('FTP_PATH_WEB is {0}'.format(FTP_PATH_WEB))
        # #print('FILES_WEB is {0}'.format(FILES_WEB))
        #
        # j = 1
        # while j < len(tmp):
        #     # print (tmp[i])
        #     t = tmp[j].replace('version', VERSION)
        #     FILES_WEB_DIR.append(t)
        #     j += 2
        # print('FILES_WEB_DIR is {0}'.format(FILES_WEB_DIR))

        global LOCAL_ZIP_PATH
        LOCAL_ZIP_PATH = []  # 下载DB文件后才有值

        global TNSNAME
        TNSNAME = Public.readini('dbuser', 'tnsname')
        global USER_NAME
        USER_NAME = Public.readini('dbuser', 'user_name')
        global USER_PWD
        USER_PWD = Public.readini('dbuser', 'user_pwd')


class WebFiles:
    '''
       step1 备份旧的的bsaml文件夹--重命名
       step2 重命名bsaml.war为bsaml.zip
       step3 解压web zip文件
    '''

    def rename(self):
        """
        重命名war文件
        :return:
        """
        filename = "F:/dowloadftp/DCT4.0-BSAML-V202201-08-000-20221228.202212140627(cz)/BSAMLApp/bsaml.war"
        newname="F:/dowloadftp/DCT4.0-BSAML-V202201-08-000-20221228.202212140627(cz)/BSAMLApp/bsaml.zip"
        os.rename(filename,newname)
    def un_zip(self):
        file_name = "F:/dowloadftp/DCT4.0-BSAML-V202201-08-000-20221228.202212140627(cz)/BSAMLApp/bsaml.zip"
        file_name1 = "F:/dowloadftp/DCT4.0-BSAML-V202201-08-000-20221228.202212140627(cz)/BSAMLApp/bsaml"
        zip = zipfile.ZipFile(file_name)
        zip.extractall(file_name1)
        zip.close()

# 20210910：修改get_beta_by_version适用version=V202101.2.0.20210929时的数据库取包问题 by xiaojw
def get_beta_by_version(betas):
    v = Public.readini('version', 'version')
    if len(v) > 11:
        v = v[0:11]
    else:
        pass
    version = v.replace('.', '-') + 'V'
    beta_filter = []
    for beta in betas:
        if beta.find(version) != -1:
            beta_filter.append(beta)
        else:
            pass
    beta_name = Public.get_lates_beta(beta_filter)
    return beta_name


class DbFiles:
    """
    创建log文件夹
    """
    def newlogpath(self):
        log_path= 'E:\dowloadftp\log'
        if os.path.exists(log_path):
            print(f'文件夹{log_path}已存在')
        else:
            os.mkdir(log_path)
    def download_dbfiles(self):
        # dd = Download(log=log.logger, arg=None)
        res, ver = dd.download_artifact_artifactory(type="database")  # service ,database,patch,interface
        log.logger.info(res)
        global LOCAL_ZIP_PATH
        LOCAL_ZIP_PATH = res
    def extract_files(self):
        zip_files = list(set(LOCAL_ZIP_PATH)) #下载列表
        #add zip文件解压
        # zip_files=[r'E:\\dowloadftp\\05add/DCT4.0-BSAML2019CSDC-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLDataCheck-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLnewBigdataRule-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLInstitutionRiskAssess-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLCRS-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLPBOC2019No63-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLCustomrules-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLFinancingSide-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLSimilarCustManage-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLLegalBusinRisk-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLMultiCurrency-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLProductRiskAssess-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLBoi-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLInstitutionSelfAssessmentOne-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLAccuity-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLCrg-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLAgencyrisk-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLExternalListUse-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLAgencyCustInfoManage-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLDueDiligence-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLFileManagement-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLWorldCheck-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLPom-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLInfoSec-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLBigdataRule-V202201-10-000-20230315.zip',
        #            r'E:\\dowloadftp\\05add/DCT4.0-BSAMLDowJones-V202201-10-000-20230315.zip']
        for zip_file in zip_files:
            file_dir, file_name = os.path.split(zip_file)
            if zipfile.is_zipfile(zip_file):
                shutil.unpack_archive(zip_file, file_dir)
                log.logger.info('ZIP文件：{0}解压成功'.format(zip_file))
            else:
                rf = rarfile.RarFile(zip_file)
                rf.extractall(file_dir)
                log.logger.info('RAR文件：{0}解压成功'.format(zip_file))

        print('解压完成')
    def an_garcode(self,dir_names):
        """anti garbled code"""
        os.chdir(dir_names)


        for temp_name in os.listdir('.'):
            try:
                #使用cp437对文件名进行解码还原
                new_name = temp_name.encode('cp437')
                #win下一般使用的是gbk编码
                new_name = new_name.decode("gbk")
                #对乱码的文件名及文件夹名进行重命名
                os.rename(temp_name, new_name)
                #传回重新编码的文件名给原文件名
                temp_name = new_name
                if temp_name=="bsaml.war":
                    os.rename('bsaml.war','bsaml.zip')
            except:
                #如果已被正确识别为utf8编码时则不需再编码
                pass


            if os.path.isdir(temp_name):
                #对子文件夹进行递归调用
                self.an_garcode(temp_name)
                #记得返回上级目录
                os.chdir('..')






    def decompression_zip(self):
        zip_files = list(set(LOCAL_ZIP_PATH)) #下载列表
        # zip_files =['E:\\dowloadftp\\01dc/DCT4.0-DCAML-V202201-10-000-20230315.zip', 'E:\\dowloadftp\\02dcinterface/DCT4.0-AMLinterface-V202201-10-000-20230315.202302200644.zip']
        for filename in zip_files:
            expresspath = filename[:filename.find('/')]
            findpath = filename[:filename.rfind('.')]
            print("findpath",findpath)
            # unrar_file(log.logger,filename,LOCAL_PATH)
            oldName = ''
            if zipfile.is_zipfile(filename):
                zip_file_contents = zipfile.ZipFile(filename, 'r')
                for file in zip_file_contents.namelist():
                    # if oldName == '':
                    # oldName = LOCAL_PATH + "/" + file
                    fileName = file.encode('cp437').decode('gbk')  # 先使用cp437编码，然后再使用gbk解码
                    zip_file_contents.extract(file,expresspath)  # 解压缩ZIP文件
                    os.chdir(expresspath)  # 切换到目标目录
                    os.rename(file, fileName)  # 重命名文件

            else:
                zip_file_contents = rarfile.RarFile(filename, 'r')
                for file in zip_file_contents.namelist():
                    if oldName == '':
                        oldName = LOCAL_PATH + "/" + file
                    fileName = file.encode('utf8').decode('utf8')
                    # print(file)
                zip_file_contents.extract(file, LOCAL_PATH)  # 解压缩ZIP文件
                os.chdir(LOCAL_PATH)  # 切换到目标目录
                os.rename(file, fileName)  # 重命名文件
            zip_file_contents.close()
            # shutil.rmtree(oldName)  # 删除旧文件夹

            log.logger.info('{0}解压成功'.format(filename))
    def remove_empty(self):
        if os.path.isdir(LOCAL_PATH):
            for root_path, dir_names, file_names in os.walk(LOCAL_PATH):
                for dn in dir_names:
                    # LOCAL_PATH 下面的所有目录，都会经过这个 dir_path 这里了，至于为什么，你要去看 os.walk() 了。
                    dir_path = os.path.join(root_path, dn)
                    if not len(os.listdir(dir_path)):
                        os.rmdir(dir_path)


    # 解压db zip文件
    def unzipfile(self):
        # from unRarFile import unrar_file
        zip_files = list(set(LOCAL_ZIP_PATH))
        zip_files = [r'E:\dowloadftp\02dcinterface\DCT4.0-AMLinterface-V202201-10-000-20230315.202302170916.zip']
        for filename in zip_files:
            # unrar_file(log.logger,filename,LOCAL_PATH)
            oldName = ''
            zip_file_contents = zipfile.ZipFile(filename, 'r')
            for file in zip_file_contents.namelist():
                if oldName == '':
                    oldName = LOCAL_PATH + "/" + file  #E:\dowloadftp/DCT4.0-AMLinterface-V202201-09-000-20230215/
                fileName = file.encode('cp437').decode('gbk')  # 先使用cp437编码，然后再使用gbk解码
                zip_file_contents.extract(file, LOCAL_PATH)  # 解压缩ZIP文件
                os.chdir(LOCAL_PATH)  # 切换到目标目录
                os.rename(file, fileName)  # 重命名文件
                # time.sleep(1)

            zip_file_contents.close()
            #shutil.rmtree(oldName)  # 删除旧文件夹
            log.logger.info('{0}解压成功'.format(filename))

    #解压rar文件
    def unrarfile(self):
        # from unRarFile import unrar_file
        rar_files = list(set(LOCAL_ZIP_PATH))
        for rarname in rar_files:
            log.logger.info('开始解压{0}'.format(rarname))
            # unrar_file(log.logger, rarname, LOCAL_PATH)
            oldName = ''
            zip_file_contents = rarfile.RarFile(rarname, 'r')
            for file in zip_file_contents.namelist():
                if oldName == '':
                    oldName = LOCAL_PATH + "/" + file
                fileName = file.encode('utf8').decode('utf8')  # 先使用cp437编码，然后再使用gbk解码
                # print(file)
                zip_file_contents.extract(file, LOCAL_PATH)  # 解压缩ZIP文件
                os.chdir(LOCAL_PATH)  # 切换到目标目录
                os.rename(file, fileName)  # 重命名文件
            zip_file_contents.close()
            shutil.rmtree(oldName)  # 删除旧文件夹
            log.logger.info('{0}解压成功'.format(rarname))


class UpdateWeb:
    '''覆盖webrar和dispatchcenter
    '''

    def update_rar(self):
        log.logger.info('web升级开始')

        i = 0
        while i < len(FILES_WEB):
            # file = FILES_WEB[i].split('.')[0]
            # file = server_name[FILES_WEB[i].split("-V")[0]]
            file=FILES_WEB[i]
            local = LOCAL_PATH + '\\' + file
            ferm = FERM_PATH + '\\' + FILES_WEB_DIR[i]
            log.logger.info('{0}复制到{1}中'.format(local, ferm))
            Public.vanxkr_copy_tree(local, ferm, write_exists=True, tabnum=0)
            log.logger.info('{0}复制完毕'.format(local))
            i += 1
        log.logger.info('web升级结束')

    def upate_dispatchcenter(self):
        local = ''
        for path in LOCAL_ZIP_PATH:  # E:/dowloadftp/SCM40-合规升级包(基于V202001-00-000)_V202002-0-0beta12.zip
            path0 = path.split('.zip')[0]
            path1 = path0 + '\\' + 'dispatchcenter'
            if os.path.exists(path1):
                local = path1
                ferm = FERM_PATH + "\dispatch2\webapps\Artemis\WEB-INF\classes\config\dispatchcenter"
                log.logger.info('{0}复制开始'.format(local))
                Public.vanxkr_copy_tree(local, ferm, write_exists=True, tabnum=0)
                log.logger.info('{0}复制完毕'.format(local))
            else:
                pass


class UpdateDb:
    def newsql(self,file,old_string,new_string):
        """
        替换文件中的字符串
        :param file:
        :param old_string:
        :param new_string:
        :return:
        """
        file_data=""
        with open(file,"r",encoding="GB2312") as  f:
            for line in f:
                if old_string in line:
                    line=line.replace(old_string,new_string)
                file_data+=line
        with open(file,"w",encoding="GB2312") as f:
            f.write(file_data)
    def newbatrun(self):
        installbatNew = LOCAL_PATH + '/installNew.bat'
        installbat = open('install.bat', 'r', encoding='GB2312')
        installbatNewFile = open(installbatNew, 'w+',encoding='GB2312')
        new_lines = ''
        installbat.seek(0)
        for line in installbat:
            if '数据库别名' in line:
                line = line.replace(' /p ', ' ')
                line = line.split('=')[0] + '=' + TNSNAME + '\n'
                new_lines = new_lines + line

            if '用户名' in line:
                line = line.replace(' /p ', ' ')
                line = line.split('=')[0] + '=' + USER_NAME + '\n'
                new_lines = new_lines + line

            if '密码' in line:
                line = line.replace(' /p ', ' ')
                # print(line)
                line = line.split('=')[0] + '=' + USER_PWD + '\n'
                # print(line)
                new_lines = new_lines + line



            if 'Install.sql' in line or 'install.sql' in line:
                new_lines = new_lines + line
        new_lines = LINES_START + new_lines + LINES_END
        # print new_lines
        installbatNewFile.seek(0)
        installbatNewFile.truncate()
        installbatNewFile.write(new_lines)
        # installbatNewFile.flush()
        installbat.close()
        installbatNewFile.close()

        os.chdir(LOCAL_PATH)
        os.system('call installNew.bat')
        log.logger.info('升级BS完毕')


if __name__ == '__main__':
    log = Logger('log/all.log', level='debug')
    con = ConfigParam()
    con.read_param()

    dd = Download(log=log.logger, arg=(baseinfo, download_list))



    #DB部署
    log.logger.info('BS DB开始升级')
    db = DbFiles()
    # log.logger.info('下载包')
    # db.download_dbfiles()
    # log.logger.info('解压包')
    # db.extract_files()
    # log.logger.info('解决乱码')
    # db.an_garcode('E:\dowloadftp')
    # db.remove_empty()

    #生成sql文件
    FileFind.findfilefinal(FileFind.BSALLfiles(1),1)
    FileFind.findfilefinal(FileFind.BSALLfiles(2),2)

    db.newlogpath()

    ''' 升级数据库bat'''
    runbat = UpdateDb()
    runbat.newsql('E:\dowloadftp\installbsjj.sql','@E:\dowloadftp','@.')
    runbat.newsql('E:\dowloadftp\installbsxt.sql','@E:\dowloadftp','@.')
    runbat.newbatrun()
    log.logger.info('数据库升级完毕')





    log.logger.info('BS DB升级完毕')


    # web部署
    web = WebFiles()
    t0 = datetime.now()
    # web.rename()
    # web.un_zip()
    t1 = datetime.now()


    # input('输入任意字符退出：')
    # exit(0)
