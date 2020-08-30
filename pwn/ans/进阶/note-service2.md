   开启的保护：

    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX disabled
    PIE:      PIE enabled
    RWX:      Has RWX segments
出问题的源码，不知为什么我的伪代码跟答案不一致：
```c
void sub_E30()
{
  __int64 savedregs; // [rsp+10h] [rbp+0h]

  while ( 1 )
  {
    sub_C56();
    printf("your choice>> ");
    sub_B91();
    switch((unsigned int)&savedregs)
    {
      case 1u:
          sub_CA5();
          break;
      case 2u:
          sub_DC1();
          break;
      case 3u:
          sub_DD4();
          break;
       case  4u:
          sub_DE7();
          break;
        case 5u:
            exit(0);
            return ;
        default:
            puts("invalid choice");
            break;
    }
}
```

在sub_CA5()函数中，存在：

printf("index:");
      v1 = sub_B91();           //输入，可理解为scanf
      printf("size:");
      result = sub_B91();      //输入，可理解为scanf
      v2 = result;
      if ( result >= 0 && result <= 8 )
      {
        qword_2020A0[v1] = malloc(result);  //result最高为8，但是v1的范围没有限制
        if ( !qword_2020A0[v1] )
        {
          puts("malloc error");
          exit(0);
        }

1、创建的堆空间大小最多为7字节
2、保存堆指针的数组下标可以越界

 
数组下标可以越界，可以把任意的地方的8字节数据写成新建的堆的地址指针，
那么，通过数组越界，我们可以把一些函数的GOT表内容修改为堆指针，由于程序NX保护是关闭的，那么堆栈里的数据也可以当成指令执行。那么我们在堆里布置shellcode即可。

但是堆的大小最大为7个字节，我们的shellcode最少也要十几字节，因此，我们把shellcode分开，存储到多个堆里，然后在每个堆的最后2字节空间，填上jmp short xxxx指令，让它跳转到下一个堆里去执行代码。Jmpshort xxxx指令占用2字节，并且，这条指令使用的是相对当前代码位置寻址，为了发现规律，我们找几个现成的指令看看

.text:0000000000000E8A ; ---------------------------------------------------------------------------
.text:0000000000000E8A                 mov     eax, 0
.text:0000000000000E8F                 call    sub_CA5
.text:0000000000000E94                 jmp     short loc_ED1                                            //查看jmp short的跳转规律
.text:0000000000000E96 ; ---------------------------------------------------------------------------
.text:0000000000000E96                 mov     eax, 0
.text:0000000000000E9B                 call    sub_DC1
.text:0000000000000EA0                 jmp     short loc_ED1                                          //查看jmp short的跳转规律
.text:0000000000000EA2 ; ---------------------------------------------------------------------------
.text:0000000000000EA2                 mov     eax, 0
.text:0000000000000EA7                 call    sub_DD4
.text:0000000000000EAC                 jmp     short loc_ED1                                         //查看jmp short的跳转规律
.text:0000000000000EAE ; ---------------------------------------------------------------------------

Hex-View区：
0000000000000E94  EB 3B             jmp short loc_ED1

0000000000000EA0  EB 2F             jmp short loc_ED1

0000000000000EAC  EB 23             jmp short loc_ED1

计算：
94+3B = CF  //跳转的地址是ECF，而非ED1

A0+2F = CF  //跳转的地址是ECF，而非ED1

AC+23 = CF //跳转的地址是ECF，而非ED1

但是我们发现ED1-2=ECF，因此得出规律：jmp short xxx中的xxx计算公式为xxx = 目标地址-当前地址-2。


堆的数据结构：

/*
  This struct declaration is misleading (but accurate and necessary).
  It declares a "view" into memory allowing access to necessary
  fields at known offsets from a given base. See explanation below.
*/
struct malloc_chunk {
//INTERNAL_SIZE_T被定义为size_t,在32位系统上是32位无符号整数(4bytes)，在64位系统上是64位无符号整数(8bytes)
  INTERNAL_SIZE_T      prev_size;  /*  前一个chunk空闲则记录了前一个chunk的大小，如果前一个chunk不空闲，那么这里存储的就是前一个chunk最后的数据. */
  INTERNAL_SIZE_T      size;       /* 当前chunk的大小，chunk的大小必须是2*SIZE_SZ的整数倍。32位系统下最小的chunk是16个字节大小，64位系统下最小的chunk是24个字节或32个字节大小。 */

  struct malloc_chunk* fd;         /* chunk被分配后从fd开始是用户的数据*/
  struct malloc_chunk* bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /*只有在chunk空闲时才是用，只用于large chunk */
  struct malloc_chunk* bk_nextsize;
};


paylaod中chunk示意图：

![avatar](/home/dudu/图片/chunk_payload.PNG)

Jmp short后面的next值的计算:

next = (8 + 8 + 8 + 1 + 2 - 2) = 0x19

构造shellcode:



    ;64位系统调用  
    mov rdi,xxxx;/bin/sh字符串的地址  
    mov rax,59;execve的系统调用号  
    mov rsi,0;  
    mov rdx,0  
    syscall  

