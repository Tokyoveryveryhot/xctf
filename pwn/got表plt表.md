x86是小端的字节序
https://blog.csdn.net/linyt/article/details/51635768
#include <stdio.h>

void print_banner()
{
    printf("Welcome to World of PLT and GOT\n");
}

int main(void)
{
    print_banner();

    return 0;
}

编译:
gcc -Wall -g -o test.o -c test.c -m32
链接:
gcc -o test test.o -m32

print_banner函数的汇编指令：
80483cc <print_banner>:
 80483cc:    push %ebp
 80483cd:    mov  %esp, %ebp
 80483cf:    sub  $0x8, %esp
 80483d2:    sub  $0xc, %esp
 80483d5:    push $0x80484a8  
 80483da:    call **<printf函数的地址>**
 80483df:    add $0x10, %esp
 80483e2:    nop
 80483e3:    leave
 80483e4:    ret
 print_banner函数内调用了printf函数，而printf函数位于glibc动态库内，所以在编译和链接阶段，链接器无法知知道进程运行起来之后printf函数的加载地址。故上述的**<printf函数地址>** 一项是无法填充的，只有进程运运行后，printf函数的地址才能确定。
 一个简单的方法就是将指令中的**<printf函数地址>**修改printf函数的真正地址即可。

但这个方案面临两个问题：

现代操作系统不允许修改代码段，只能修改数据段
如果print_banner函数是在一个动态库（.so对象）内，修改了代码段，那么它就无法做到系统内所有进程共享同一个动态库。
因此，printf函数地址只能回写到数据段内，而不能回写到代码段上。
运行时修改，更专业的称谓应该是运行时重定位，与之相对应的还有链接时重定位。