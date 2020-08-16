0、套路：使用checksec查看开了哪些保护
                 使用file查看文件类型
                 运行查看功能
1、checksec工具不可用问题：可以在脚本中写入elf = ELF('./CGFfsb')，其中CGFfsb文件需要在shell所在路径下。每次遇到一道题，都需要先执行一下。
2、pwndbg本地调试的使用方法：下载后使用mv 原名称 目的名称更改名字，之后使用chmod 777 目的名称提权，随后在该目录下shell输入dbg，产生pwndbg的命令，使用b * 0x地址下断点，输入start运行。


pwndbg本地调试的使用方法：
下断后请加
debug()
r.send(payload)
r.interactive()

例子：
def debug(addr = '0x080485B8'):
    raw_input('debug:')
    gdb.attach(r, "b *" + addr)
debug()

r.send(payload)

r.interactive() 

必须加 r.interactive()
或者在r.send前加pause也ok
应该是要维持进程吧

好坑啊

下断后 在弹出gdb窗口按c 来到断点处

注意最好在r.send前下断如果要观察payload对栈的影响


3、tips:做pwn题的一些调试技巧

当你觉得你的脚本没有问题，但是却又怎么也出你想要的结果时，你就需要用到调试了

1、一个是设置context.log_level="debug"
2、脚本在执行时就会输出debug的信息，你可以通过观察这些信息查找哪步出错了
3、用gdb.attach(p)
4、在发送payload前加入这条语句，同时加上pause() 时脚本暂停
5、然后就会弹出来一个开启gdb的终端，先在这个终端下好断点，然后回运行着脚本的那个终端按一下回车继续运行脚本，程序就会运行到断点，就可以调试了

from pwn import*  
p = process('./xxxx')  
payload = .....  
gdb.attach(p)  
pause()  
p.sendline(payload)  
p.interactive()  

b  * 0xAAAAAAAA为下断点
start为运行
step为单步步入
next为单步执行

6、如果遇到libc里的read函数，需要sleep一下


x/10gx   $sp查看栈顶元素6
