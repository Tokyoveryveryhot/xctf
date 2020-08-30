## view source
1、点开场景后，使用F12或ctrl+u进行查看

2、burp抓包

## get_host

1、firefox下载MaxHacKBar插件

2、在url中附加写入/?a=1，就完成了以GET方式提交一个名为a，值为1的变量

3、回车执行，显示出请再以POST方式随便提交一个名为b，值为2的变量

4、点击Load URL，在Post Data下点勾，在Post data中输入b=2，点击Execution按键

5、显示flag


在客户机和服务器之间进行请求-响应时，两种最常被用到的方法是：GET和POST。
{GET-从指定的资源请求数据。POST-向指定的资源提交要被处理的数据}


利用hackbar进行POST传参：复制get的url，选择postdata，填入b=2，选择execute。即可发送POST请求。或使用burpsuite的Repeater进行实现。

## robets
Robots协议的定义。

robots.txt是一个文本文件，是一个协议，爬虫先检查是否参在robots.txt，之后根据文件内容确定访问范围

样例

配置项详解，其中Disallow是一种道德规范，而非必要手段。

Nikto扫描，dirsearch等后台扫描器的用法

## backup
常见备份文件后缀名

使用御剑或diesearch进行网站后台扫描，与上题方法雷同。

## cookie
cookie定义：简言之，加密存储的辨别用户身份的数据。

两个重要应用：登录及购物车

**题解**：通过F12开发者选项去做或使用burpsuite抓包进行实现。wp第7条写入爬虫进行实现

## disabled button
**题解**：点击F12，取消Disable选项。或审计表单代码，以post方式传递auth=flag。或使用burpsuite的Repeater发送修改后的包。

## weak_auth
**题解**:使用burpsuite实现字典遍历。[爆破字典库](https://github.com/rootphantomer/Blasting_dictionary)

wp第10条和第18条。

## command_execution
WAF（Web应用防护系统）的意义及功能（审计设备，访问控制设备，架构/网络设计工具，WEB应用加固工具）。

审计设备的记录信息（4条）

这题就是所谓的没有上waf，也就是可以篡改网站。

**题解**：命令拼接来实现：

127.0.0.1 | find / -name “*.txt”

127.0.0.1 | cat /home/flag.txt

wp第7条通过python脚本进行实现

## simple_php
php代码审计，本题是弱类型比较。

代码含义

**题解**：

1、php是弱类型语言：强类型的语言遇到函数引数类型和实际调用类型不匹配的情况经常会直接出错或者编译失败；
而弱类型的语言常常会实行隐式转换，或者产生难以意料的结果。

2、字符串和数字比较使用==时,字符串会先转换为数字类型再比较 php var_dump('a' == 0);//true，这里'a'会被转换数字0 var_dump('123a' == 123);//true，这里'123a'会被转换为123。$a==0 and $a，a=a即可，$b>1234且!is_numeric($b)，b=12345a（php是弱类型，所以输入'0'==0成立；b不能是数字但是要和数字比较，可以用数组b[]=5678）

3、在判断语句里，要求a==0，并且a不为0；看到两个等号，想到php弱等于，这里可以让a=admin，在“==”判断是，admin会被转换成“0”，a满足条件 然后是b，is_numeric这个函数要求b不能是数字，下面要求b大于1234，这里可以让b=2345%00，%00是空格的意思，这样b就不会被判断为数字，且大于1234，b满足条件。 构造url：http://111.198.29.45:40060/?a=admin&b=2345%00,即可得到flag。

[php弱类型初级入门介绍](https://www.secpulse.com/archives/69529.html)

[php弱类型安全问题总结](https://blog.spoock.com/2016/06/25/weakly-typed-security/)

[php弱类型总结](https://www.cnblogs.com/Mrsm1th/p/6745532.html)

## xff_referer
xff和referer的含义

简单地说，xff是告诉服务器当前请求者的最终ip的http请求头字段。通常可以直接通过修改http头中的X-Forwarded-For字段来仿造请求的最终ip

referer就是告诉服务器当前访问者是从哪个url地址跳转到自己的，跟xff一样，referer也可直接修改

**题解**：通过burpsite的Repeater来实现。

第11，14条

## webshell
**题解**：通过中国菜刀或[蚁剑](https://github.com/AntSwordProject/antSword/releases(https://github.com/AntSwordProject/antSword/releases))
进行实现。

wp第3条使用burpsuite的Repeater进行实现：直接在最下方写入shell=system("ls")
或shell=system("cat flag.txt")

# simple_js
js代码审计

**题解**