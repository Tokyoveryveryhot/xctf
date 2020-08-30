## re1
**题解**：通过String窗口进入函数sub_401000()，关键代码：
```C
_mm_storeu_si128((__m128i *)&v4, _mm_loadu_si128((const __m128i *)&xmmword_413E34));
scanf("%s", (unsigned int)&v8);
v2 = strcmp((const char *)&v4, &v8);
if(v2==0)
    printf("flag get\n");
```
_mm_storeu_si128(），对其进行分析发现它类似于memset(),将xmmword_413E34的值赋值给v5，所以，我们可以得到正确的flag应该在xmmword_413E34中，然后，我们双击413E34进行跟进。可以看到一堆十六进制的数，**点击R变为ASCII码**。**值得注意的是**xmmword_413E34的位置不足，还需要qword_413E44。

这时，我们使用IDA的另一个功能 R ，能够将十进制的数转换为字符串

1、大端与小端:

假设一个十六进制数0x12345678

大端的存储方式是：12,34,56,78，然后读取的时候也是从前往后读

小端的存储方式是：78,56,34,12，然后读取的时候是从后往前读取

2、v2 = -(v2 < 0) | 1;该语句的意思为v2如果小于0的话，v2的值为-1，否则v2的值为1

void _mm_store_si128 ( __m128i *p, __m128i a);可存储128位数据，将__m128i 变量a的值存储到p所指定的变量中去

3、使用OD动态调试可以直接得出flag

**总结**：如果是flag比对，回应一般是已经写在程序里了，用shift+F12查找字符串；一般是给出回应。有的flag是程序运行给出，可以kali动态运行，或者读代码写出类似代码，如第二题game，写代码

##   HelloCTF
**题解**：v10=v8=v4=v9[v3]，v13=a437261636b4d65

```C
     if(strcmp(v10,v13))
    	printf("Success");
```

需要将437261636b4d654a757374466f7246756e转化为ASCII字符串

打开网站进行转换或使用Winhex查看或写程序查看，如果用C程序实现，则使用sscanf函数进行实现

## getit
Linux系统下64位下不同个数的参数传参规则

movsx(先符号扩展，并传送),movzx(将较小值拷贝到较大值,先零扩展，并传送)

符号扩展与零扩展的含义及例子

按位与，AND与TEST的汇编命令相同

IDA中的流程图显示注释

**题解过程**
声明变量v3,v5

对v5进行一系列计算

将变量u写入到文件flag.txt中

用************覆盖写入的flag

移除

```C
for ( i = 0; i < strlen(&t); ++i )
  {
    fseek(stream, p[i], 0);		
    fputc(*(&t + p[i]), stream);	//在此处进行动态调试
    fseek(stream, 0LL, 0);		
    fprintf(stream, "%s\n", u);
  }
```

为此在for循环的fputc函数下进行动态调试，得出结果。
或者直接汇编为c程序

## game
本题没有主函数，运行后发现关键字符串Play a game，在IDA中搜索Strings，找到函数sub_45F400()

我的总结和网上的题解

```C
//每个都亮一遍就可以得到flag
 if ( byte_532E28[0] == 1
      && byte_532E28[1] == 1
      && byte_532E28[2] == 1
      && byte_532E28[3] == 1
      && byte_532E28[4] == 1
      && byte_532E28[5] == 1
      && byte_532E28[6] == 1
      && byte_532E28[7] == 1 )
    {
      sub_457AB4();
    }
```

flag的算法：
```C
  for ( i = 0; i < 56; ++i )
  {
    v5[i] ^= v62[i];
    v5[i] ^= 0x13;
    printf("%c",v5[i])
  }
```

或者直接在OD中patch文件，留一个jz，其他改为jnz

或者在OD中将jnz loc_45F671改为jmp loc_45F671

## open-sourse
VScode配置C++环境编译及调试

直接计算：

unsigned int hash = 0xcafe * 31337 + (25 % 17) * 11 + strlen("h4cky0u") - 1615810207;
python实现


## simple-unpack
使用UPX工具脱壳。upx -d  simple_unpack（文件名），脱壳

## logmein
**题解过程**

根据IDA中的伪代码，编程进行实现：

伪代码的含义为输入一个值，进行比较：s[i] != (char)(*((_BYTE *)&v7 + i % v6) ^ v8[i])，如果二者相等，则得到flag，说明输入的即为flag

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BYTE unsigned char
int main()
 {
    unsigned int i;
    char v8[18] = ":\"AL_RT^L*.?+6/46";
 //   __int64 v7 = 28537194573619560;
    long long v7 = 28537194573619560;
    int v6 = 7;
    char s[18] = "";
    for(i = 0; i < strlen(v8); ++i) 
    {
      s[i] = (char)(*((BYTE*)&v7 + i % v6)^v8[i]);
    }
      printf("%s\n", s);
      system("PAUSE");
      return 0 ;
  }
```
或者用python实现：

```python
v8=":\"AL_RT^L*.?+6/46"
v7="harambe"
v6=7

flag=''
 
for i in range(0,len(v8))
    flag += chr(ord(v8[i]) ^ ord(v7[i%v6]))
print flag
```

*注意*：v7 = 28537194573619560LL;的意思是long long v7=28537194573619560;

wp:第1条和
1、paython实现，由于程序是小段的存储方式，所以，ebmarah就得变成harambe

ord():是将字符串转换为ascii格式，为了方便运算

chr():是将ascii转换为字符串

## insanity

反汇编，查找字符串，找到flag；或用UE打开找到flag

反汇编找到puts((&strs)[4 * (v4 % 0xA)]);语句；strs即为所求的flag。

## python-trade
**题解**

[在线pyc反汇编网站](https://tool.lu/pyc/)反汇编得到源码：

```python
import base64

def encode(message):
    s = ''
    for i in message:
        x = ord(i) ^ 32
        x = x + 16
        s += chr(x)
    
    return base64.b64encode(s)

correct = 'XlNkVmtUI1MgXWBZXCFeKY+AaXNt'
flag = ''
print 'Input flag:'
flag = raw_input()
if encode(flag) == correct:
    print 'correct'
else:
    print 'wrong'
```

直接推导程序：
```python
import base64

correct = 'XlNkVmtUI1MgXWBZXCFeKY+AaXNt'
mid_flag = base64.b64decode(corrent)
print "the corrent message's frrst fflag is:"
print mid_flag

flag=' '
for i in mid_flag:
#x=ord(chr(i))-16
x=i-16
x=x^32
flag+=chr(x)
print flag
```

wp第六条

## no-strings-attached
x/6sw $eax

6：显示6行数据

s：字符串形式

w：word（4字节）形式

**题解**：4个函数的含义

发现在调用完decrypt函数之后，返回值eax即为flag，即0x8048725下断点

**值得注意的是**需要使用 x/6sw $eax命令进行查看

最后需要将这些转换为字符串的形式

```python
key="3934347b796f5f61725f616e696e74726e61696f6e6c5f6d737465797d"

flag=key.decode('hex')
print flag
```

## csaw2013reversing2
**题解**：使用动静结合的方式实现：

```c
  if ( sub_40102A() || IsDebuggerPresent() )
  {
    __debugbreak();
    sub_401000(v3 + 4);
    ExitProcess(0xFFFFFFFF);
  }
  ```
  使用OD在__debugbreak()下断点：0x401096。将0x40109A的汇编指令int 3改为nop。执行完解密函数sub_401000()后，在Hex Dump窗口按下Ctrl+G查看EDX地址(4C07E0)所指向的值，找到flag。或者将0x4010A3处的指令jmp short loc_4010CD改为jmp short 4010A5，可得到flag。或者在解密函数sub_401000()的retn语句下断点。

## maze
[迷宫问题](ttps://ctf-wiki.github.io/ctf-wiki/reverse/maze/maze/)：

该类问题使用光标选择.rodata部分中所有地图字符串，之后按shift+E提取所有地图数据。

迷宫问题特征：

1）在内存中放置“地图”

2）将用户输入限制为几个字符

3）通常只有一个迷宫入口和一个迷宫出口

该地图可以直接组成非常长的字符串，也可以一一排列。如果是逐行排列，由于迷宫一般较大，所以用于按线（注意，不按排列）按顺序排列，每行对应一个特定的行号，需要确定该行还原迷宫图的编号。安排迷宫的功能将重复很多次。
受限制的字符，例如作为组合w/s/a/d，h/j/k/l，l/r/u/d这样的类似组合。
通常，迷宫只有一个入口和一个出口，例如左上角(0, 0)位置的入口和右下角的出口(max_X, max_Y)。但是可能会有一个出口。在迷宫的中央，使用一个Y字符指示等。还要根据具体情况判断回答迷宫问题的条件。

**题解**

四个函数为：

```c
//v9的下一字节减1
bool __fastcall sub_400650(_DWORD *a1)
{
  int v1; // eax@1

  v1 = (*a1)--;
  return v1 > 0;
}
//v9的下一字节加1
bool __fastcall sub_400660(int *a1)
{
  int v1; // eax@1

  v1 = *a1 + 1;
  *a1 = v1;
  return v1 < 8;
}
//v9减1
bool __fastcall sub_400670(_DWORD *a1)
{
  int v1; // eax@1

  v1 = (*a1)--;
  return v1 > 0;
}
//v9加1
bool __fastcall sub_400680(int *a1)
{
  int v1; // eax@1

  v1 = *a1 + 1;
  *a1 = v1;
  return v1 < 8;
}
```

根据二维数组的性质，可以判断出

O对应左；
o对应右；
.对应上；
0对应下。
而这些函数传入的参数v9就是迷宫

跟到label15的位置，出现asc_601060字符串，查看字符串的值：

asc_601060      db '  *******   *  **** * ****  * ***  *#  *** *** ***     *********',0

8*8的迷宫：

走出迷宫就可以得到flag