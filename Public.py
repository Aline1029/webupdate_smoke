# -*- coding: utf-8 -*-
import os
import configparser
"""
    ====================
    Auther：林雅静
    Time：2023/3/920:06
    Project:webupdate_smoke
    =========================
"""
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

