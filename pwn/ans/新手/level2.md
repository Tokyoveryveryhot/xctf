第一步，进入IDA中查看，发现主函数执行
vulnerable_function();
system("echo 'Hello World!'")
进入vulnerable_function()函数，发现buf的大小为88h，而read的值为100h，存在缓冲区溢出漏洞。可以通过溢出覆盖返回地址。
第二步，主函数中出现system函数，但是与level0不同的是system函数的参数不是/bin/sh而是普通的字符串"echo 'Hello World！'"和"echo Input:"。同时发现Fountion name中出现system，_system函数，有个大坑需要注意，要找的是_system的地址，即pit段的地址0x8048320。
第三步，查找字符串，找到字符串/bin/sh，其地址为0x804a024，
第四步，写脚本函数，这里溢出覆盖返回地址的payload的构成为0x88+4个缓冲区字符，注意4是覆盖ebp地址的字符，之后接上system函数的地址，需要注意的是在执行sytem函数时栈存放的是函数的返回地址，之后才是参数，即需要执行的命令。因此需要4字节的填充（具体可看ps的第4点）。

PS:
1、需要注意的是system的地址不是load字段的，而是.plt里的，也可以使用主函数中的call _system，参考writeup第五条
2、x64和x32的汇编参数存放的位置不同，32位中的stdcall于cdcel调用约定存在栈里，直接压入四个随意字节，再压入system的参数命令地址，而64位优先存在寄存器里，所以需要一个把参数复制到寄存器里的指令，然后再调用system
3、gdb调试时会出现进入不了sytem函数的情况，为此需要run之前执行set follow-fork-mode parent，步入子进程。

4、写payload的时候要注意一个问题：在32位程序运行中，函数参数直接压入栈中调用函数时栈的结构为：调用函数地址->函数的返回地址->参数n->参数n-1->···->参数1
4、函数调用栈的结构，如果是正常调用system函数，我们调用的时候会有一个对应的返回地址，这里以'aaaa'作为虚假的地址，其后参数对应的参数内容。具体见加密与解密P106

writeup第2个不错
writeup的第5条中payload = 'a' * (0x88 + 4) + p32(0x0804845c) + p32(0x0804A024)
其中0x0804845c为call _system的地址，相当于重写了int system(const char *command){return system(command);}函数，因此不需要返回地址。
