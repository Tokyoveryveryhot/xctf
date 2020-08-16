在 printf 中，使用 *<a_number_of_chars>%<number>$n* 就可以将相应的第 *<number>* 个参数的位置写为 % 前输出的字符数量
1、由函数调用约定可知，在64位程序下，前六个参数从左到右放入RDI, RSI, RDX, ECX, R8, R9

进入main函数中，发现main函数调用sub_400D72()函数，进入该函数，发现该函数调用sub_400A7D()，sub_400BB9()和sub_400CA6()三个函数，第一个函数为输入east跳出循环。第二个函数中指令printf(&format,&format)存在格式化字符串漏洞，可以进行任意地址写。值得注意的是在他的上面有两个输入点，一个是“%ld”格式，一个是“%s”格式。第三个函数存在指令为((void(*fastcall *)(_QWORD,void *)v1)(0LL,v1)是将v1强制转化为函数指针类型，然后调用该函数。最后一个函数中的强制转换指令类型为脆弱点，该语句将V1一个void指针强制类型转换成函数指针并调用了，所以我们将shellcode通过上面的read写入就会得到shell。而执行该条指令的条件为*(DWORD *)a1 == *(DWORD*)(a1+4)，即a1[0]==a1[1]。回溯该变量，发现该变量为主函数中的v5，而v5=(__int64)v4。*v4=68,v4[1]=85，我们要做的就是将*v4=v4[1]，这里就需要利用第二个函数中的格式化字符串漏洞，从而将v4[0]的值改为85.
PS:
v4=malloc(8uLL)//共申请8字节的空间
*v4=68;//前4字节存放68
v4[1]=85;//后4字节存放85
v5=(__int64)v4;//v5中存在的不是v4的内容，不是68,58俩个数字，而是存放这两个数字的内存空间的地址。
1、sub_400CA6函数中声明变量void *v1;之后满足a1[0]==a[1]时，使用mmap函数映射到内存，之后读入256字节写至其中。
2、sub_400BB9函数中printf(&format,&format)语句中，第一个参数是要溢出的地址，第二个参数是写入的值。
动态调试，查看第一个参数在栈中的位置，第二个参数是将第一个参数在栈中的位置写入85，


由函数调用约定可知，在64位程序下，前六个参数从左到右放入RDI, RSI, RDX, ECX, R8, R9中，利用格式化字符串漏洞，进入脆弱点，写入shellcode
...[overwrite addr]....%[overwrite offset]$n

其中... 表示我们的填充内容，overwrite addr 表示我们所要覆盖的地址，overwrite offset 地址表示我们所要覆盖的地址存储的位置为输出函数的格式化字符串的第几个参数。所以一般来说，也是如下步骤

    确定覆盖地址
    确定相对偏移
    进行覆盖



但是，要运行至此处，要先满足if ( *a1 == a1[1] )a1是前面提到的v4传入函数的形参，就是个地址。
而a[0]=v4[0]=v3[0]=68, a[1]=v4[1]=v3[1]=85。要将a[0]和a[1]修改为相同的值。可以通过前面提到的格式化字符串漏洞来修改。
函数sub_400BB9()内的v2是我们输入的v4的地址，我们需要知道v2在栈内的位置，这样才能通过%?$n向v2指向的地址处写入字符串长度。
程序的格式化字符串漏洞上面有两个输入点，漏洞利用在第二个输入点，那我们可以在第一个输入数组的地址，然后在第二个输入点进行利用。
下面程序为什么这么写，待会在后面的正式的交互代码中解释。这里只说一下最后一句。p.recvuntil('I hearit')必须要写上，否则程序的debug末尾只能看到发送了数据，看不到之后print的format字符串。如下图：
#查看sub_400BB9()栈内情况
from pwn import *
p = remote("111.198.29.45","49404")
context(arch='amd64', os='linux', log_level='debug')

p.recvuntil('secret[0] is ')
v4_addr = int(p.recvuntil('\n')[:-1], 16)

p.sendlineafter("What should your character's name be:", 'cxk')
p.sendlineafter("So, where you will go?east or up?:", 'east')
p.sendlineafter("go into there(1), or leave(0)?:", '1')
p.sendlineafter("'Give me an address'", str(int(v4_addr)))
p.sendlineafter("And, you wish is:",'AAAA'+'-%p'*10)
p.recvuntil('I hear it')


利用思路就是想办法使*a1==a1[1]
a1=v4=v3是前面的秘密
那这里*v3，v3[1]分别赋值68，85，而v3是一个地址
格式化字符串的偏移是7，利用%7$n
前半部正常来讲应该是填地址也就是秘密1，我认为的payload的应该b64(秘密1)+%7$n而实际在看过一些文章后，所有人都一致使用的是%85d/c/x+%7$n，这一块的解释是把85赋值到这个地址，但是这个位置不应该是需要覆盖的地址吗，为什么要传值呢更令我感到奇怪的是sub_400BB9输入地址v2之后并没有使用这个值，但是这个值也不能瞎给。
所以我推断是反编译出现了问题，这里格式化字符串应该是这样printf(&v2&format);
传入值后Printf(要覆盖的地址%85c%7$n)，这样的话把85位字符转换数值写进去，使得if判断成立，进入可读可写可执行空间。

writeup第5条第7条