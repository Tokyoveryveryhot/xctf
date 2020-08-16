1、打开IDA，发现main()函数没有问题，找到echo函数。
但发现echo(buf)函数，其中buf的大小为0x400，在该函数中存在赋值语句：
 for ( i = 0; *(_BYTE *)(i + a1); ++i )
    s2[i] = *(_BYTE *)(i + a1);
赋值的终止条件是当读取到a1中\x00的时候。其中s2的大小为0x10。
存在溢出。输入payload的时候，就会在覆盖eip地址后截断(地址一般都有\x00)。

Welpwn题解首先用IDA查看发现主函数不能栈溢出，我们看看echo这个函数，echo会把主函数输入的字符串复制到局部的s2里，并且s2只有16字节，可以造成溢出。
Echo函数先循环复制字符到s2，如果遇到0，就结束复制，然后输出s2。
因此，我们如果想直接覆盖函数返回地址，那么我们的目标函数必须没有参数，否则，我们用p64(...)包装地址时，必然会出现0。
比如我们的payload为payload = 'a'*0x18+ p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)由于是64为包装，因此payload字符串为’a’*0x18 + ‘\xa3\x08\x40\x00\x00\x00\x00\x00’+ ‘......’
这意味着，payload后面的两个地址不会被复制到s2，因为前面遇到了0，那么这样我们就不能正确调用出system(“/bin/sh”)。

首先，进入echo函数后，栈中数据：


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


假如我们在buf中输入的0x400个a字符，那么栈变成这样了


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

因为没有在中途遇到0，所以echo中的循环一直复制buf中的数据到s2中，造成溢出。现在，假如我们的payload = 'a'*0x18+ p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)
那么，栈中的数据变成这样
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
这样的话，echo执行完后，跳到pop_rdi地址处执行，然而，pop_rdi执行完后，栈顶指针esp指向buf+0x8 ，即aaaaaaaa，这里不是地址，因此程序崩溃结束。
然而，如果，我们在buf+0x8处存储其他函数地址，也是不可行的，因为该地址是64位，末尾几位有0，这会导致我们还没溢出s2就已停止数据复制


因此，我们有以下总结
buf的前24字节不能存地址数据，只存普通数据。
buf+24处应该存某一地址，且该地址处有四个pop指令，和一个retn指令。这样，
四次pop后，就相当于跳过了24字节数据和自己本身8字节地址数据。
在接下来的地址处，我们就可以写其他函数。

在0x40089C处正好有四个pop和一个retn

假如我们的payload = 'a'*0x18 + p64(pop_24) + p64(pop_rdi) + p64(write_got) + p64(puts_plt) + p64(main_addr)
那么栈布局如下

那么栈布局如下
aaaaaaaa
aaaaaaaa	0x10字节数据区
aaaaaaaa	echo函数栈的ebp
pop_24_addr	echo函数返回地址
aaaaaaaa
aaaaaaaa
aaaaaaaa
pop_24_addr
pop_rdi
write_got
puts_plt
main_addr	0x400字节数据区
main函数栈的ebp

那么，echo函数执行完以后，跳到pop_24地址处，由于跳转后，栈顶指针指向buf，出栈4个后，指针指向buf+32 ，
接下来遇到retn，出栈一个元素为(pop_rdi)作为pop_24的返回地址，这样跳转到了pop_rdi，后面类似。
我们调用system 获取到shell

