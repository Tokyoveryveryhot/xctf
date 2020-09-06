#codeing = UTF-8
from pwn import *

context(arch='i386',os='linux',log_level='debug')
elf = ELF('./supermarket')
