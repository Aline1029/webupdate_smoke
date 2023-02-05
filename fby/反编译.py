#!/usr/bin/env python
# coding: utf-8

# 提取exe中的pyc
import os
import sys
import pyinstxtractor
from uncompyle6.bin import uncompile
import shutil


# 预处理pyc文件修护校验头
def find_main(pyc_dir):
    for pyc_file in os.listdir(pyc_dir):
        if not pyc_file.startswith("pyi-") and pyc_file.endswith("manifest"):
            main_file = pyc_file.replace(".exe.manifest", "")
            result = f"{pyc_dir}/{main_file}"
            if os.path.exists(result):
                return main_file


def uncompyle_exe(exe_file, complie_child=False):
    sys.argv = ['pyinstxtractor', exe_file]
    pyinstxtractor.main()
    # 恢复当前目录位置
    os.chdir("../../../python/Python反编译工具包（exe）")

    pyc_dir = os.path.basename(exe_file)+"_extracted"
    main_file = find_main(pyc_dir)

    pyz_dir = f"{pyc_dir}/PYZ-00.pyz_extracted"
    for pyc_file in os.listdir(pyz_dir):
        if pyc_file.endswith(".pyc"):
            file = f"{pyz_dir}/{pyc_file}"
            break
    else:
        print("子文件中没有找到pyc文件，无法反编译！")
        return
    with open(file, "rb") as f:
        head = f.read(4)

    if os.path.exists("pycfile_tmp"):
        shutil.rmtree("pycfile_tmp")
    os.mkdir("pycfile_tmp")
    main_file_result = f"pycfile_tmp/{main_file}.pyc"
    with open(f"{pyc_dir}/{main_file}", "rb") as read, open(main_file_result, "wb") as write:
        write.write(head)
        write.write(b"\0"*12)
        write.write(read.read())
    
    if os.path.exists("py_result"):
        shutil.rmtree("py_result")
    os.mkdir("py_result")
    sys.argv = ['uncompyle6', '-o',
                f'py_result/{main_file}.py', main_file_result]
    uncompile.main_bin()

    if not complie_child:
        return
    for pyc_file in os.listdir(pyz_dir):
        if not pyc_file.endswith(".pyc"):
            continue
        pyc_file_src = f"{pyz_dir}/{pyc_file}"
        pyc_file_dest = f"pycfile_tmp/{pyc_file}"
        print(pyc_file_src, pyc_file_dest)
        with open(pyc_file_src, "rb") as read, open(pyc_file_dest, "wb") as write:
            write.write(read.read(12))
            write.write(b"\0"*4)
            write.write(read.read())

    os.mkdir("py_result/other")
    for pyc_file in os.listdir("pycfile_tmp"):
        if pyc_file==main_file+".pyc":
            continue
        sys.argv = ['uncompyle6', '-o',
                    f'py_result/other/{pyc_file[:-1]}', f'pycfile_tmp/{pyc_file}']
        uncompile.main_bin()

# exe_file = "C:/Users/Administrator/Desktop/新建文件夹/翻译小工具.exe"
exe_file = "E:/开发部署工具/webupdate_smoke/fby/HsScriptTool.exe"

uncompyle_exe(exe_file)
