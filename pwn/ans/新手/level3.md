0、查找函数地址的典型方法是从泄漏的同一个库中的另一个函数的地址计算到所需函数的偏移量，然而，要使这种方法有效地工作，gLibc的远程服务器版本需要与我们的相同。我们还可以通过泄漏一些函数并在libcdb.com中搜索找到gLibc的远程版本，但有时这种方法会失败

write函数的第一个参数为1，2，3时有特殊用途：
（1） 是标准输出 (屏幕)
（2） 是标准错误输出 (屏幕)
（0） 是标准输入 （键盘）
这三个是系统定制的，程序启动后，默认打开的，不需要专门open()。


1、程序编译时会采用两种表辅助：PIT表（内部函数表）和GOT表（全局函数表），这两个表一一对应，PIT中的数据对应GOT表中的地址。PLT表的数据不是函数真实地址，而是起到过渡作用，而是GOT表中的地址。可以通过PLT表跳到GOT表得到函数的真实地址。
2、该题的思路为发现缓冲区溢出点，调用system函数和/bin/sh字符串，而这两者在lib库中，因此找到write函数充当媒介，找到lib库的基址，加上system函数和/bin/sh字符串的偏移值。
该题分为两个部分：一是得到lib库的基地址（write函数相当于媒介），二是根据lib库中的system函数和/bin/sh字符串的值构造payload
1）在vulnerable_function()函数中，发现溢出点函数read(0,&buf,0x100u)。
2）libc中的函数的相对地址是固定的，要想获取到system函数的地址，可以通过write()函数进行offset计算。
（1） 首先利用write()函数计算出write()函数的真实地址；
（2） 利用相对offset计算出system和"/bin/sh"的真实地址。
在vulnerable_function()中，先调用了write()函数，然后调用read()函数。write()函数返回到vulnerable_function()后，再进行read()函数调用，这样我们就可以进行二次攻击。 - 第一次攻击我们利用栈溢出将write()函数在got表中的真实地址leak出来，然后减去libc中的offset，就可以得到libc的base address。- 第二次攻击重新进入main函数，再次通过栈溢出，利用system函数进行getshell
这样的话，第一次使用的payload构成如下：

payload = ‘A’*0x88 + p32(0xdeadbeef) + p32(write_plt) + p32(main_addr) + p32(1) + p32(write_got) + p32(0xdeadbeef)
其中p32(write_got)为.got.plt节的地址。利用第一次攻击，就可以获取到libc的基地址。由于返回地址我们添的是main_addr，因此执行完这条payload之后，会继续返回到主函数之中(eip需要压栈)。然后进行第二次攻击，使用的payload构成为：
payload0 = ‘A’*0x88 + p32(0xdeadbeef) + p32(sys_addr) + p32(0xdeadbeef) + p32(bin_sh_addr）

1、先通过栈溢出，利用 write 函数将其本身在GOT表中的地址泄露出来，减去在 libc_32.so 中的偏移，得到基址，紧接着重新进入 main 函数，再次通过栈溢出，利用 system 函数完成get shell

first stack 		                                                    second stack
0x88 * 'a' 		                                                         0x88 * 'a'
ebp 		                                                                ebp
write@plt 		                                                        system_addr
main_addr 	//返回地址	                                                        xxxx		//返回地址为填充
1 		                                                                    bin_sh_addr
write@got 		
4

2、有一个缓冲区buf，在read函数中进行了调用。可以进行溢出。攻击思路：libc中的函数的相对地址是固定的，要想获取到system函数的地址，可以通过write()函数进行offset计算。1. 首先利用write()函数计算出write()函数的真实地址；2. 利用相对offset计算出system和"/bin/sh"的真实地址。

3、在vulnerable_function()中，先调用了write()函数，然后调用read()函数。write()函数返回到vulnerable_function()后，再进行read()函数调用，这样我们就可以进行二次攻击。  - 第一次攻击我们利用栈溢出将write()函数在got表中的真实地址leak出来，然后减去libc中的offset，就可以得到libc的base address。- 第二次攻击重新进入main函数，再次通过栈溢出，利用system函数进行getshell


我们将会从 got 中获得库函数（write 和 read 函数）的地址
我们将会用 plt 来调用它们


4、
.plt与.got是实现重定向的一种方式。
.got
GOT（Global Offset Table）全局偏移表。这是「链接器」为「外部符号」填充的实际偏移表。（动态表，相当于指针，实际偏移表）

.plt
PLT（Procedure Linkage Table）程序链接表。它有两个功能，要么在 .got.plt 节中拿到地址，并跳转。要么当 .got.plt 没有所需地址的时，触发「链接器」去找到所需地址，并填充到.got.plt节中，并跳转，其是由代码片段组成的，每个代码片段都跳转到GOT表中的一个具体的函数调用（每个程序中该表都不会变化，因此是静态表，指针的指针）

.got.plt
这个是 GOT 专门为 PLT 专门准备的节。说白了，.got.plt 中的值是 GOT 的一部分。它包含上述 PLT 表所需地址（已经找到的和需要去触发的）。相当于.plt的GOT全局偏移表，内容有两种情况：1）如果之前查找到该符号，内容为外部函数的具体地址，2）如果没查找过，内容为跳转会.plt的地址。（快速查找表）

.plt.got
这个表。。。

.plt 的作用简而言之就是先去 .got.plt 里面找地址，如果找的到，就去执行函数，如果是下一条指令的地址，说明没有，就会去触发链接器找到地址
.got.plt 显而易见用来存储地址，.got.plt 确实是 GOT 的一部分

作者：madao756
链接：https://www.jianshu.com/p/5092d6d5caa3
来源：简书


https://blog.csdn.net/linyt/article/details/51635768的图挺好


dynelf 其基本代码模板如下:
p = process('./xxx')
def leak(address):
  #各种预处理
  payload = "xxxxxxxx" + address + "xxxxxxxx"
  p.send(payload)
  #各种处理
  data = p.recv(4) )#接受的字节要看程序是32位还是64位来决定 ，32位接受4个字节的数据 而64位接受8个字节的数据
  log.debug("%#x => %s" % (address, (data or '').encode('hex')))#这里是测试 可省略
  return data
d = DynELF(leak, elf=ELF("./xxx"))      #初始化DynELF模块 
systemAddress = d.lookup('system', 'libc')  #在libc文件中搜索system函数的地址
