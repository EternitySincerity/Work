# -*- coding: cp936 -*-
import os
import time

start = time.time()
#time.sleep(5)
c = time.time() - start
cwd=os.getcwd()
print('�������к�ʱ:%0.2f'%(c))
print('������Ŀ¼:%s'%(cwd))
