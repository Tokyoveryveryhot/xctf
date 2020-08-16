使用printf(“%x”,…);可以输出指定参数的16进制形式，但是在实际的使用中，参数不一定都是32位的整数，有可能是16位的short,8位的char。如果使用printf %x 输出short和char会是什么结果呢？
为此，在VS2015编写简单代码如下：

#include <stdio.h>
#include <stdlib.h>
int main()
{
    int l;
    short s;
    char c;
    l = 0xdeadbeef;
    s = l;
    c = l;
    printf("%x\n", l);
    printf("%x\n", s);
    printf("%x\n", c);
    system("pause");
    return 0;
}

分析
代码比较简单，首先定义了3个变量，然后对三个变量进行赋值，在赋值的过程中会发生宽度溢出。
s=l 将32位的整数放入16位的short，那么s的值只是l的低16位，即s=0xbeef;
c=l 将32位的整数放入8位的char,那么c的值应该只是l的低8位，即s=0xef;
但实际输出：
deadbeef
ffffbeef
ffffffef

那么这些ff是怎么来的呢？
我们在printf(“%x”,s);加断点看反汇编的结果：

0017140E  movsx       eax,word ptr [s]  
00171412  mov         esi,esp  
00171414  push        eax  
00171415  push        175858h  
0017141A  call        dword ptr ds:[179118h]

经过 movsx eax,word ptr [s]后 eax的高16位会变化为ffff

MOVSX 指令：带符号扩展传送指令，将第二个操作数当作有符号类型取其符号位进行扩展。
movsx eax,word ptr [s]
word ptr [s]的值为0xbeef，二进制为1011 1110 1110 1111
最高位（符号位）为1，于是扩展的时候会将eax的高16位全部扩展为1.于是就输出了如上结果。

如果s的最高位为0，结果就变了
#include <stdio.h>
#include <stdlib.h>
int main()
{
    int l;
    short s;
    char c;
    l = 0xdead0eef;
    s = l;
    c = l;
    printf("%x\n", l);
    printf("%x\n", s);
    printf("%x\n", c);
    system("pause");
    return 0;
}

输出为：
deadbeef
beef
ffffffef

可以看到因为s的最高位为0，于是输出的时候没有 了ffff出现。
但是c的最高位为1（因为c==1110 1111),eax的高位全部扩展为1了，于是第三个输出还是扩展的FFFFFFEF。