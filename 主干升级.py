# -*- coding: utf-8 -*-
import time

import os
import configparser
import logging
from logging import handlers
import zipfile
import rarfile
import shutil
from jfrog_artifactory_pro import Download

global LINES_START
global LINES_END



LINES_START = '''@echo off
    color a
    :loop
    echo.
    echo ************************************************************
    echo *                                                          *
    echo *                                                          *
    echo *      4.1开始升级                                          *
    echo *                                                          *
    echo *                                                          *
    echo ************************************************************
    echo.
    title 恒生反洗钱系统4.1升级
    '''
LINES_END = '''type .\log\install.log | find /i /n "ora-" > .\log\install.txt
    type .\log\install.log | find /i /n "警告" >> .\log\install.txt
    type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
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


class Public:
    # 把A文件夹下的文件复制到B文件夹下
    def vanxkr_copy_tree(in_dir, out_dir, write_exists=False, tabnum=0):
        if (0 == tabnum):
            print('文件目录复制模式为: %s' % ('覆盖' if write_exists else '跳过'))
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        print('%s当前目录: %s' % ('\t' * tabnum, in_dir))
        copy_file_counts = 0
        copy_dir_counts = 0
        for f in os.listdir(in_dir):
            in_f = os.path.join(in_dir, f)
            out_f = os.path.join(out_dir, f)
            if os.path.isfile(in_f):
                copy_file_counts += 1
                if write_exists or not os.path.exists(out_f):  # 文件不存在
                    open(out_f, "wb").write(open(in_f, "rb").read())
                    try:
                        file1 = os.path.split(in_f)[1]
                        print('%s第 %s 个文件已复制完毕: %s' \
                              % ('\t' * (tabnum + 1),
                                 copy_file_counts, \
                                 file1))
                    except Exception as e:
                        print('复制完毕，但是源文件名有中文乱码，请检查')
                else:
                    pass
            if os.path.isdir(in_f):
                copy_dir_counts += 1
                print('%s第 %s 个文件夹: %s' % ('\t' * (tabnum + 1), copy_dir_counts, in_f))
                Public.vanxkr_copy_tree(in_f, out_f, write_exists, tabnum + 1)

    # 读取单一配置
    def readini(sec, usr):
        config = configparser.ConfigParser()
        filename = 'confignew.ini'
        config.read(filename, encoding='utf-8')
        conf = config.get(sec, usr)
        return conf

    # 读取整个section配置 1:返回整个的items元祖（配置名+配置值）列表 2：返回配置值的列表
    def readini_sec(sec, type=1):  # [('lib1', 'F:\\Ferm'), ('lib2', 'F:\\Ferm1')]
        config = configparser.ConfigParser()
        filename = 'confignew.ini'
        config.read(filename, encoding='utf-8')
        if type == '1':
            conf = config.items(sec)
        else:
            conf = []
            conf1 = config.items(sec)
            for c in conf1:
                conf.append(c[1])
        return conf

    # 清空文件夹
    def del_directory(path):
        # path=r'E:\2.upgrade\AML4升级包\V202001.02\AML\webapps\Artemis\WEB-INF\lib'
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def get_lates_beta(self):
        num = []
        # for beta in self:
        #     if beta.find('beta') != -1:
        #         m = beta.strip('.zip')
        #         t = beta.strip('.zip').index('beta') + 4
        #         num.append(int(m[t:]))
        #     else:
        #         self.remove(beta)
        # num.sort(reverse=True)
        # print(num[0])
        # for s in self:
        #     if s.find('beta' + str(num[0])) != -1:
        #         fileName = s
        for beta in self:
            beta1 = beta.split('V')
            last = beta1[-1]  #
            try:
                last1 = int(last)
            except Exception as e:
                last1 = 0
            num.append(last1)
        num.sort(reverse=True)
        # print(num[0])
        for s in self:
            if s.find(str(num[0])) != -1:
                fileName = s
        print('最新数据库包：{0}'.format(fileName))
        return fileName




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
        global USER_PWD
        USER_PWD = Public.readini('dbuser', 'user_pwd')


class WebFiles:
    '''
       step1 备份旧的的bsaml文件夹--重命名
       step2 重命名bsaml.war为bsaml.zip
       step3 解压web zip文件
    '''

    def rename(self):
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
    def download_dbfiles(self):
        # dd = Download(log=log.logger, arg=None)
        res, ver = dd.download_artifact_artifactory(type="database")  # service ,database,patch,interface
        log.logger.info(res)
        global LOCAL_ZIP_PATH
        LOCAL_ZIP_PATH = res
    def extract_files(self):
        zip_files = list(set(LOCAL_ZIP_PATH)) #下载列表
        zip_files =[
                       # r'E:\\dowloadftp\\01dc/DCT4.0-DCAML-V202201-09-000-20230215.zip'
                       r'E:\dowloadftp\02dcinterface/DCT4.0-AMLinterface-V202201-09-000-20230215.202302160406.zip'
                       # r'E:\\dowloadftp\\03BS/DCT4.0-BSAML-V202201-09-000-20230215.202302100545(cz).zip',
                       # r'E:\\dowloadftp\\04fxq/DCT4.0-BSAMLFxq-V202201-09-000-20230215.202302100510.zip',
                       ]
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

    def rename_files_and_folders(self):
        # 遍历当前目录下的所有文件和文件夹
        for file_name in os.listdir(LOCAL_PATH):
            # 拼接文件的完整路径
            file_path = os.path.join(LOCAL_PATH, file_name)
            # 判断当前路径是否为文件夹
            if os.path.isdir(file_path):
                # 对文件夹进行重命名
                os.rename(file_path, file_path.encode('cp437').decode('gbk'))
                # 如果是文件夹，递归调用自身
                self.rename_files_and_folders()

            else:
                #如果是文件，对文件进行重命名
                os.rename(file_path, file_path.encode('cp437').decode('gbk'))
    def fanyizipinterface(self):
        for root, dirs, files in os.walk(LOCAL_PATH):
            for dir_name in dirs:
                try:
                    os.rename(os.path.join(root, dir_name), os.path.join(root, dir_name.encode('utf8').decode('gbk')))
                except Exception as e:
                    print('Error: {}'.format(e))

            for file_name in files:
                try:
                    os.rename(os.path.join(root, file_name), os.path.join(root, file_name.encode('utf8').decode('gbk')))
                except Exception as e:
                    print('Error: {}'.format(e))

    def decompression_zip(self):
        zip_files = list(set(LOCAL_ZIP_PATH)) #下载列表
        for filename in zip_files:
            expresspath = filename[:filename.find('/')]
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
                        time.sleep(1)

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
    def newbatrun(self):
        for localPatchName in LOCAL_ZIP_PATH:
            # LOCAL_ZIP_PATH = ['E:\\dowloadftp\\FERM20-平台基础升级包(基于V202003-0-0)_V202003-1-0beta202008090321.zip',
            #                   'E:\\dowloadftp\\SCM40-合规升级包(基于V202003-0-0)_V202003-1-0beta202008070313.zip']
            # batFile = localPatchName.split('.zip')[0] + '/install.bat'
            sqlFile = localPatchName.split('.zip')[0] + '/sql/install.sql'
            installbatNew = localPatchName.split('.zip')[0] + '/installNew.bat'
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
            log.logger.info('升级{0}完毕'.format(localPatchName))


if __name__ == '__main__':
    log = Logger('log/all.log', level='debug')
    con = ConfigParam()
    con.read_param()

    dd = Download(log=log.logger, arg=(baseinfo, download_list))

    # # web部署
    # web = WebFiles()
    # t0 = datetime.datetime.now()
    # web.rename()
    # web.un_zip()
    # t1 = datetime.datetime.now()

    log.logger.info('开始升级')
    db = DbFiles()


    db.download_dbfiles()
    # db.unzipfile()

    db.decompression_zip()
    for i in range (3):
        db.remove_empty()

    # db.extract_files()
    # db.rename_files_and_folders()

    # db.fanyizipinterface()

    # runbat = UpdateDb()
    # runbat.newbatrun()
    # log.logger.info('升级完毕')
    # input('输入任意字符退出：')
    # exit(0)
