burpsuite软件走的是代理服务器来抓包，相当于在中间加入了一个代理，截断中间的包。而不是网卡抓包。不能抓https的包
1、设置浏览器代理：
首选项->网络设置->设置->手动代理配置127.0.0.1，端口设置为999
2、打开burpsuite，设置代理：
Proxy->Options-> Proxy Listeners->Add，添加端口999
3、选择Intercept，选择Intercept is on，结果在HTTP history中显示
注：貌似不能抓https的包。
4、设置代理之后，浏览器不能访问网页

对于http的包：
打开Proxy->Intercept，选择Intercept is on，截断数据包，可以对数据包进行修改，修改后选择Intercept is off，可以发送数据包。


https://www.fujieace.com/kali-linux/beginner-tutorial/burpsuite-27.html
主要功能：
1、抓包，例view_source&cookie
2、爬虫
3、扫描漏洞
4、暴力破解，例weak_auth
5、发包改包，例get_post&xff_refer
6、sequencer
7、编码解码

之前不能抓https包可能是由于证书没有信任