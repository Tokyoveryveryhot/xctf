1、打开IDA F5，进入hello函数，发现危险函数，脆弱点gets(&s)，可以在该函数下溢出，共需要0x26+4个字节来填充，从而覆盖返回地址。
2、找到system函数的plt表的地址，但是没有/bin/sh字符串。
3、我们发现name为全局变量，地址不变，因此可以利用该空间存放/bin/sh
4、payload的构造为0x26加4字节的填充，system函数的地址加上返回地址（参照level2）加上name全局变量的地址。


wp：
1、函数大致流程：main函数首先定义三个流的缓冲区，然后调用hello函数，然后打印“thank you”,然后程序结束
2、结合gets函数不限制输入字符个数和程序没有开启stack保护两点，我们可以在使用输入时让输入的字符串覆盖栈上hello函数的返回地址，让程序执行完hello函数之后执行我们设计的部分
3、name位于bss区，可将字符串写入name变量。
