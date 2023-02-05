import time
import zipfile, os, shutil
from pathlib import Path
from unrar import rarfile
import subprocess



def unrar_file(log, fileName, outPath):
    t1 = time.time()
    type = os.path.splitext(fileName)[-1][1:]
    if type == 'rar':
        # proc = subprocess.Popen(["unrar x %s %s"%(fileName,outPath)], shell=True)
        try:
            fileget = rarfile.RarFile(fileName, 'r')
            fileget.extractall(outPath)
            # fileget.close()
        except Exception as e:
            log.error("unrar error:%s" % e)
    elif type == 'zip':
        zf = zipfile.ZipFile(fileName)
        zf.extractall(path=outPath)
        zf.close()
    else:
        pass

    t2 = time.time()
    log.info("%s解压时间:%s" % (fileName.split("\\")[-1], (t2 - t1)))
