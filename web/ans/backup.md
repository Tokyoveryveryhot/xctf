常见的备份文件后缀名有: .git .svn .swp .svn .~ .bak .bash_history
以使用扫目录脚本/软件,扫一下,这里使用的是github上的脚本dirsearch,命令行下: py python3 dirsearch.py -u http://10.10.10.175:32770 -e *
看到存在备份文件index.php.bak访问 http://10.10.10.175:32770/index.php.bak


wp4使用御剑来进行处理。


https://blog.csdn.net/tianjin_ren/article/details/88773106
网站后台扫描工具