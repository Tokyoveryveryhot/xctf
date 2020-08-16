1、准备工作
（1）chmod 777 forget
（2）file forget
显示：
1、准备工作
（1）chmod 777 forget
（2）file forget
显示：
forget: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=35930a2d9b048236694e9611073b759e1c88b8c4, stripped
（3）./forget
显示：
Welcome, let me know your name: yang
Hi, yang. Let's play a game.
Game 1/50
Give me the point(1~6): 1
You lost.
Bye bye!
（4）脚本checksec：
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
2、思路
本题中出现输入函数：v6 = read(0, buf, 0x50uLL);但buf的长度等于0x50，不存在溢出
随后出现srand(seed[0]);
查看缓存区：
-0000000000000050 buf             db 55 dup(?)
-0000000000000019 var_19          db ?
-0000000000000018 var_18          dq ?
-0000000000000010 seed            dd 2 dup(?)
可以通过溢出覆盖seed[0]的值
与guess_num的题目相同：
payload='a'*(0x50-0x40)+p64(0)
main函数循环中sub_A20()函数是输入v1，当v1==rand()%6+1时，输出WIN，否则跳出循环。
而v8==50时才跳出循环，调用sub_B28()函数，打开flag文件，输出“Congratulations”和flag的值




