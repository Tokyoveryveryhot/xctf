场景下应该是每个id对应一个数据界面，结果数据全被删了，黑客是在id=2333这个界面入侵，写入了什么webshell类似的，然后后台控制删了所有数据库，题目就是让我们找出入侵的地方

看到id=1先试试是不是注入，结果发现只要带字母或其他符号就会重定向，估计后台是做了判断只有数字类型才保留在原页面不进行重定向，不会是sql注入题，应该都没有用到数据库的。
题目里又说黑客加了点什么东西，根据这些条件综合判断id等于某个数字后会出现flag，burp数字爆破后得到flag







在所有能点击的位置点击，发现只有一个button可以进去，即报表中心。
看答案说要爆破ID

使用burp suite进行抓包，在Proxy->HTTP history中找到http://220.249.52.133:38087/index.php?id=1点击右键，选择Send to Intruder。

在Intruder中选择Position，

GET /index.php?id=§1§ HTTP/1.1
Host: 220.249.52.133:38087
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://220.249.52.133:38087/
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
选择参数id进行爆破。


在Intruder->Payloads->Payload Sets中，将Payload set选为1，Payload type选为Numbers。
在Intruder->Payloads->Payload Options[Numbers]中，将From选为1，To选为10000，Step选为1，点击Start Attack。

从结果上可以看出id为2333时的响应包比其他的包的长度都大一些，得到溢出的2333，加入url参数之中。


writeup1：
1.查看题目，发现id参数只能是数字
2.使用burp进行整数暴力破解，选择位置为id参数的值，有效载荷选择整数类型
3.攻击后查看响应包，发现id为2333时，响应包长度不同，可获取flag
