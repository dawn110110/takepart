#!/usr/bin/env python
import os

for i in range(1000):
    os.system('curl -d "setno=1&cb=hello" http://map.baidu.com/maps/services/captcha')

