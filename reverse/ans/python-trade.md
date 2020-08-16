pyc文件是python编译产生的中间文件。python是一个先编译再解释型语言。python解释器由一个编译器和一个虚拟机构成，python.exe先将源码编译成字节码(即将.py 文件换转成.pyc 文件)，.pyc不是二进制码，而是一种字节码文件，它是与平台无关的中间代码，不管是在Windows 还是Linux 平台都可以执行。运行时再由虚拟机逐行把字节码翻译成目标代码。


在线pyc反汇编网站：
https://tool.lu/pyc/

将pyc文件放入在线工具进行反汇编，得到源码：
import base64

def encode(message):
    s = ''
    for i in message:
        x = ord(i) ^ 32
        x = x + 16
        s += chr(x)
    
    return base64.b64encode(s)

correct = 'XlNkVmtUI1MgXWBZXCFeKY+AaXNt'
flag = ''
print 'Input flag:'
flag = raw_input()
if encode(flag) == correct:
    print 'correct'
else:
    print 'wrong'

通过阅读代码可知，flag的每一个字符通过异或、加16、base64加密后得到密文XlNkVmtUI1MgXWBZXCFeKY+AaXNt；
直接推导程序：

import base64

correct = 'XlNkVmtUI1MgXWBZXCFeKY+AaXNt'
mid_flag = base64.b64decode(corrent)
print "the corrent message's frrst fflag is:"
print mid_flag

flag=' '
for i in mid_flag:
#x=ord(chr(i))-16
x=i-16
x=x^32
flag+=chr(x)
print flag


wp第6条
