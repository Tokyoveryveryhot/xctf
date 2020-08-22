0、打开题目，点开链接
1、设置浏览器代理127.0.0.1:8080
2、设置burp代理(一般默认，不用管)
3、监听(Proxy->Intercept->Intercept is on)
具体可参照web应用代理工具burpsuite.md
4、输入username（123），password（123），点击login，页面会被burp截住
5、在Proxy->HTTP history中，点击刚才接收到的请求包，右键选择Send to Intruder
6、在Intruder->Position中§§符号夹住的是要选择的参数，本题中为username=§123§&password=§123§
7、在Intruder->Payloads中Payloads set设为1，Payload type设为Simple list，在Payload Options中选择Load，载入字典，选择右上角的Start attack。
8、查看收到的包，长度都是一样的，随便点开一个，发现Response中显示'please login as admin'
9、关闭Intruder attack窗口，在Payload Options中写入admin，点击Add，再次测试，发现admin的包长度与其他包不同，点开发现Response包显示‘password error’，说明用户名即为admin。
10、关闭Instruder attack窗口，在Instrder->Positions中，将username改为admin，如下：
username=admin&password=§123§
11、在Instruder->Paylaod中，重复上面的第7步
12、发现123456的长度为437，Response包返回flag的值

wp的第十条和第十八条，选择python脚本遍历的密码