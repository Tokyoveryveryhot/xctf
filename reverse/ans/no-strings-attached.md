1、如果动态调试时，断点断不了，可能是你设置的断点错了，可以尝试新的断点

2、x/6sw $eax
6：显示6行数据
s：字符串形式
w：word（4字节）形式

3、发现调试到0x8048742的时候出现no-strings-attached: malloc.c:2379: sysmalloc: Assertion `(old_top == initial_top (av) && old_size == 0) || ((unsigned long) (old_size) >= MINSIZE && prev_inuse (old_top) && ((unsigned long) old_end & (pagesize - 1)) == 0)' failed.
之后便调试不了了


1、首先使用exeinfo PE查看文件的信息发现为32位的程序，没有加壳，接着使用IDA打开本题，F5进行反汇编
2、发现main函数中共有4个函数：分别是
  setlocale(6, &locale)：调用setlocale函数来配置地域的信息，设置当前程序使用的本地化信息。
  banner()：设置随机数，打印Welcome to cyber malware control software和Current tracking '刚生成的随机数' bots woldwide
  prompt_authentication()：打印Please enter authentication details：
  authenticate()：具体flag生成的地方

  使用pwngdb调试该文件，断点下在authenticate()函数，即0x8048708位置，按下n步入函数
  发现在调用完decrypt函数之后，返回值eax即为flag
  值得注意的是需要使用 x/6sw $eax命令进行查看

