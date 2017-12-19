# -*- coding: cp936 -*-
import os
import time

start = time.time()
#time.sleep(5)
c = time.time() - start
cwd=os.getcwd()
print('程序运行耗时:%0.2f'%(c))
print('程序工作目录:%s'%(cwd))
