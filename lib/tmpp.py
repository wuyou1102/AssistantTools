import os
import time
import Utility

p = 'C:\Users\dell\Desktop\log\\vvv'
files = os.listdir(p)
a = time.time()
import random

for f in files:
    a += random.randint(500, 1000)
    d = Utility.get_timestamp(time_fmt='%Y_%m_%d-%H_%M_%S', t=a)
    os.rename(os.path.join(p, f), os.path.join(p, '%s.log' % d))
