1、将ext3文件用Winhex打开，搜索flag，得到路径~root/Desktop/file/O7avZhikgKgbF/flag.txt
2、使用.7zip解压工具解码ext3文件，按照上面的路径，找到flag.txt
3、base64解码得到flag{sajbcibzskjjcnbhsbvcjbjszcszbkzj}



wp：
1、记住了"flag"的base64编码的前几个字母是"ZmxhZ"，直接WinHex打开，搜"ZmxhZ"即搜到整个flag的base64编码。
2、首先在/mnt目录下新建一个文件夹，把该光盘挂载到/mnt目录新建的文件夹下： root@kali:/mnt# mkdir a root@kali:~# mount f1fc23f5c743425d9e0073887c846d23 /mnt/a 接下来，查看光盘目录a下与flag有关的文件： root@kali:~# find /mnt/a -iname "*flag*"，结果为/mnt/a/07avZhikqKqbF/flag.txt 查看flag.txt文件的内容： root@kali:~# cat /mnt/a/O7avZhikgKgbF/flag.txt，结果为ZmxhZ3tzYWpiY2lienNrampjbmJoc2J2Y2pianN6Y3N6Ymt6an0= 最后使用base64解码： root@kali:~# base64 -d /mnt/a/O7avZhikgKgbF/flag.txt 结果为：flag{sajbcibzskjjcnbhsbvcjbjszcszbkzj} 
root@ubuntu $:mkdir ~/ext3
root@ubuntu $:mount ext3 ~/ext3
root@ubuntu $:find . | -name flag.txt
root@ubuntu $:cd 07avZhikgKgbF/
root@ubuntu $:cat flag.txt