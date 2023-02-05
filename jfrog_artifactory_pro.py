#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import time
from pyartifactory import Artifactory
# from collections import Counter


class TestArtifactory:
    def __init__(self, url='', username="", password="", log=None):
        self.log = log
        # 网址
        self.url = url
        # 用户名
        self.username = username
        # 密码
        self.password = password
        # 实例
        # self.art = None
        self.art = Artifactory(url=self.url, auth=(self.username, self.password))

    def download_artifact_artifactory(self, repo='', remove_dir='', name='', start='', end='', download_path='',
                                      version=''):
        """
        下载固件
        Args:
            repo:  仓库名称 e.g. tc_firmware
            job:   任务名称 e.g. dailybuild
            num:   编译号 e.g. 157
            start: 文件名称头 e.g. factory
            end:   文件类型 e.g. zip
            download_path:  下载路径 e.g. ./pkg
            version:    下载版本号 e.g. V2022.0.0

        Returns: image path
        """
        target = ''
        repo_list = self.get_repo_list(repo)
        if repo not in repo_list:
            self.log.info('仓库:{}不存在'.format(repo))
        else:
            self.log.info('仓库:{}存在'.format(repo))
            self.log.info(repo + '/' + remove_dir + '/')
            if "%s" in name:
                version_p = version.replace(".", "-")
                name = name % version_p
            filename = self.get_file_list(filepath=(repo + '/' + remove_dir + '/'), name=name, version=version)
            # for file in file_list:
            if filename.startswith(start) and filename.endswith(end):
                file_download = filename
                self.log.info('找到以{}开头和{}结尾的文件:{}'.format(start, end, filename))
                # break
            else:
                self.log.info('找不到以{}开头和{}结尾的文件'.format(start, end))
                file_download = None

            if file_download:
                file = repo + '/' + remove_dir + '/' + file_download
                # target = os.path.join(download_path, file_download)
                target = file_download
                self.download_file(src=file, des=download_path)

        return download_path + "/" + target

    def get_repo_list(self, repo_param):
        """
        获取可用仓库名称
        :return: repo_list
        """
        repo_list = []
        # self.art = Artifactory(url=self.url, auth=(self.username, self.password))
        repo_list_tamp = self.art.repositories.list()
        # self.log.info('仓库名称为：{}'.format(repo_list_tamp))

        for repo in repo_list_tamp:
            if repo_param.split("-")[0] in repo.key:
                repo_list.append(repo.key)
        self.log.info('仓库名称为：{}'.format(repo_list))

        return repo_list

    def get_job_list(self, repo=''):
        """
        获取可用job名称
        :return: job_list
        """
        job_list = []
        # self.art = Artifactory(url=self.url, auth=(self.username, self.password))
        job_list_tamp = self.art.artifacts.info(repo).children
        self.log.info('Job对象列表为：{}'.format(job_list_tamp))

        for job in job_list_tamp:
            job_list.append(job.uri[1:])
        self.log.info('Job列表为：{}'.format(job_list))

        return job_list

    def get_file_list(self, filepath='', name='', version=''):
        """
        获取可用文件名称
        :return: file_list
        """
        file_list = []
        # self.art = Artifactory(url=self.url, auth=(self.username, self.password))
        file_list_tamp = self.art.artifacts.info(filepath).children
        self.log.info('File对象列表为：{}'.format(file_list_tamp))
        version1 = "-".join(version.split(".")[:-1]) if version.split(".")[-1] == "0" else version.replace(".", "-")
        # version1 = version.replace(".", "-")
        self.log.info("version1:%s" % version1)
        if not name:
            for file in file_list_tamp:
                if version1 in file.uri[1:] and not file.uri[1:].split(version1)[-1][0].isdigit():
                    file_list.append(file.uri[1:])

            # file_name = max(file_list)
            file_name = max(filter(lambda x:len(x)==max(len(f) for f in file_list), file_list))
            self.log.info('File名称为：{}'.format(file_name))
            return file_name
        else:
            for file in file_list_tamp:
                file_list.append(file.uri[1:])
            if name in file_list:
                return name
            else:
                self.log.info('File名称为：{}'.format(None))
                return None
        # return file_list

    def download_file(self, src='', des=''):
        """
        下载固件
        :param: src: 固件地址，从仓库名称开始，不带url
        :param: des: 下载文件夹，不带文件名称
        :return: None
        """

        # 登录系统
        # self.art = Artifactory(url=self.url, auth=(self.username, self.password))
        t1=time.time()
        self.log.info('开始下载%s:%s'%(src,t1))
        self.art.artifacts.download(src, des)
        t2=time.time()
        self.log.info('下载结束%s:%s'%((src,t2)))
        self.log.info('下载用时%s'%(t2-t1))



class Download:

    def __init__(self, log=None, arg=None):

        self.log = log
        self.config = Config()
        if arg and isinstance(arg, tuple):
            self.config.download_list = arg[1]
            self.config.version = arg[0]["version"]
            self.config.url = arg[0]["url"]
            self.config.username = arg[0]["username"]
            self.config.password = arg[0]["password"]
            self.config.get_version_key = arg[0]["get_version_key"]
            self.config.get_version_path = arg[0]["get_version_path"]
        self.auth = {}
        self.auth["log"] = self.log
        self.auth["url"] = self.config.url
        self.auth["username"] = self.config.username
        self.auth["password"] = self.config.password
        # self.auth["version"]=self.config.version
        if arg and isinstance(arg, str):
            self.params = [param for param in self.config.download_list if param["start"] == arg]
        else:
            self.params = self.config.download_list
        self.artifactory = TestArtifactory(**self.auth)

    def download_artifact_artifactory(self, type=None):
        # 通过远程路径获取最新版本
        if self.config.get_version_key:
            dir_name = max([pname for pname in self.artifactory.get_job_list(repo=self.config.get_version_path) if
                            pname not in ("sftp", "temp")])
            self.log.info("获取最新路径：%s"%dir_name)
            # dir_name = max(self.artifactory.get_job_list(repo=self.config.get_version_path))
            version_list = self.artifactory.get_job_list(repo=self.config.get_version_path + "/" + dir_name)
            version_name = max(filter(lambda x: len(x) == max(len(f) for f in version_list), version_list))
            # version_name = max(self.artifactory.get_job_list(repo=self.config.get_version_path + "/" + dir_name))
            self.log.info("获取最新版本：%s" % version_name)
            last_version = "V" + version_name.split("V")[-1]
        else:
            last_version = self.config.version
        self.log.info(last_version)
        target_list = []
        for param in self.params:
            self.log.info(param)
            if self.config.get_version_key:
                param["version"] = last_version
                version_base = last_version if last_version.endswith(".000") else ".".join(
                    last_version.split(".")[:-1]) + ".000"
            else:
                param["version"] = self.config.version
                version_base = self.config.version if self.config.version.endswith(".000") else ".".join(
                    self.config.version.split(".")[:-1]) + ".000"
            self.log.info(version_base)
            self.log.info(param["remove_dir"])
            if "%s" in param["remove_dir"]:
                param["remove_dir"] = param["remove_dir"] % (param["version"].split(".")[0], version_base)
            self.log.info("%s" % param["version"])
            # self.log.info(param["package_type"],type)
            if type:
                if "package_type" not in param.keys():
                    continue
                if param["package_type"] != type:
                    continue
            # 判断下载包是否是接口包
            if param["package_type"] == "interface":
                del param["package_type"]
                remote_file_list = self.artifactory.get_job_list(repo=param["repo"] + "/" + param["remove_dir"])
                param["download_path"] = param["download_path"] + "/" + param["version"]
                res = self.__prepare_file(remote_file_list, param["download_path"])
                file_list = remote_file_list if res == None else res
                for file in file_list:
                    param["name"] = file
                    target = self.artifactory.download_artifact_artifactory(**param)
                    target_list.append(target)
            else:
                del param["package_type"]
                self.log.info("else param:%s"% param)
                target = self.artifactory.download_artifact_artifactory(**param)
                target_list.append(target)
        return target_list, param["version"]

    def __prepare_file(self, remote_file_list, local_file_path):
        if not os.path.exists(local_file_path):
            os.mkdir(local_file_path)
        local_file_list = list(filter(lambda x: x.endswith(".zip"), os.listdir(local_file_path)))
        remote_file_list_dict=self.__prepare_file_inner(remote_file_list)
        local_file_list_dict=self.__prepare_file_inner(local_file_list)
        remote_file_list_last = [k + "." + v for k, v in remote_file_list_dict.items()]
        local_file_list_last = [k + "." + v for k, v in local_file_list_dict.items()]
        file_list = list(set(remote_file_list_last) - set(local_file_list_last))
        # file_dict = {}
        # for ele in file_list:
        #     x = ".".join(ele.split(".")[:-2]) # 唯一文件名
        #     y = ".".join(ele.split(".")[-2:])  # 版本号
        #     if x in file_dict.keys():
        #         if y > file_dict[x]:
        #             file_dict[x] = y
        #         else:
        #             continue
        #     else:
        #         file_dict[x] = y
        # new_file_list = [k + "." + v for k, v in file_dict.items()]
        # return new_file_list
        return file_list

    def __prepare_file_inner(self,file_list):
        file_dict = {}
        for ele in file_list:
            x = ".".join(ele.split(".")[:-2])  # 唯一文件名
            y = ".".join(ele.split(".")[-2:])  # 版本号
            if x in file_dict.keys():
                if y > file_dict[x]:
                    file_dict[x] = y
                else:
                    continue
            else:
                file_dict[x] = y
        return file_dict

class Config():
    # url = "http://package.hundsun.com/artifactory"
    url = "http://172.28.12.45:80/artifactory"
    username = "caozy305"
    password = "AKCp8krKqPiibTwvPrtjj7mAdmktszEumtb3ytC6iyMmtYPCmCnRnyMv"
    version = 'V202201.2.0'
    get_version_key = True  # 获取最新版本号开关
    get_version_path = "ics4.0-generic-test-local/ICS4.0/os"  # 获取最新版本号路径

    download_list = [
        {
            "package_type": "database",  # service ,database,patch,interface
            'download_path': "./channelPackage/FERM20",
            'repo': "ics4.0-generic-test-local",
            'remove_dir': "FERM2.0/os/FERM2.0%s/FERM2.0%s/script",
            'name': '',  # 远程路径下多个版本的文件是留空
            'start': "FERM20",
            'end': "zip"
        },
        # {
        #     "package_type": "database",# service ,database,patch,interface
        #     'download_path': "./channelPackage/ICS40",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/script",
        #     'name': '',  # 远程路径下多个版本的文件是留空
        #     'start': "ICS40",
        #     'end': "zip"
        # },
        {
            "package_type": "service",  # service ,database,patch,interface
            'download_path': "./channelPackage/RMM",
            'repo': "ics4.0-generic-test-local",
            'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/WEB",
            'name': 'RMM.rar',  # 指定文件时候填写
            'start': "RMM",
            'end': "rar"
        },
        # {
        #     "package_type": "service",# service ,database,patch,interface
        #     'download_path': "./channelPackage/RMM",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/WEB",
        #     'name': 'RMM-NK.rar',  # 指定文件时候填写
        #     'start': "RMM",
        #     'end': "rar"
        # },
        # {
        #     "package_type": "service",# service ,database,patch,interface
        #     'download_path': "./channelPackage/management",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/WEB",
        #     'name': 'management.rar',  # 指定文件时候填写
        #     'start': "management",
        #     'end': "rar"
        # },
        # {
        #     "package_type": "service",# service ,database,patch,interface
        #     'download_path': "./channelPackage/dispatch2",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "FERM2.0/os/FERM2.0%s/FERM2.0%s/WEB",
        #     'name': 'dispatch2.rar',  # 指定文件时候填写
        #     'start': "dispatch2",
        #     'end': "rar"
        # },
        # {
        #     "package_type": "service",# service ,database,patch,interface
        #     'download_path': "./channelPackage/platform",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "FERM2.0/os/FERM2.0%s/FERM2.0%s/WEB",
        #     'name': 'platform.rar',  # 指定文件时候填写
        #     'start': "platform",
        #     'end': "rar"
        # },
        # {
        #     "package_type":"patch", # service ,database,patch,interface
        #     'download_path': "./pkg",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/patch",
        #     'name': '',  # 远程路径下多个版本的文件是留空
        #     'start': "ICS40",
        #     'end': "zip"
        # },
        # {
        #     "package_type": "interface",  # service ,database,patch,interface
        #     'download_path': "./pkg",
        #     'repo': "ics4.0-generic-test-local",
        #     'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/接口",
        #     'name': '',  # 远程路径下多个版本的文件是留空
        #     'start': "ICS40",
        #     'end': "zip"
        # }
    ]


def logger_init():
    log_path = "./log"
    log_filename = "./log/%s.log" % time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    logging_name = ''
    os.makedirs(log_path, mode=0o755, exist_ok=True)
    # 获取logger对象
    logger = logging.getLogger(logging_name)
    logger.setLevel(logging.INFO)
    # 创建一个handler,用于写入日志文件
    fh = logging.FileHandler(log_filename, mode='w', encoding='gb2312')
    fh.setFormatter(logging.Formatter("[%(asctime)s]:%(levelname)s:%(message)s"))
    logger.addHandler(fh)
    # 创建一个handler，输出到控制台
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s]:%(levelname)s:%(message)s"))
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    log = logger_init()
    # 调用方式
    param1 = {
        "url": "http://package.hundsun.com/artifactory",
        "username": "caozy33405",
        "password": "AKCp8krKqPiibTwvPrtjj89kG4Y57YuRA576mF7mAdmktszEumtb3ytC6iyMmtYPCmCnRnyMv",
        "version": 'V202201.2.0',
        "get_version_key": True,  # 获取最新版本号开关
        "get_version_path": "ics4.0-generic-test-local/ICS4.0/os"  # 获取最新版本号路径
    }
    param2=[{
        "package_type": "interface",
        'download_path': "D:\\nk_update\\内控升级\\interface_update_接口\\channelPackage",
        'repo': "ics4.0-generic-test-local",
        'remove_dir': "ICS4.0/os/ICS4.0%s/ICS4.0%s/接口",
        'name': '',
        'start': "ICS40",
        'end': "zip"
    }]
    dd = Download(log=log, arg=(param1,param2))
    res = dd.download_artifact_artifactory(type="interface")  # service ,database,patch,interface
    for x in res[0]:
        print(x)
