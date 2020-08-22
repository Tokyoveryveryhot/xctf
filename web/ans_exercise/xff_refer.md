xff

维基百科：

    X-Forwarded-For（XFF）是用来识别通过HTTP代理或负载均衡方式连接到Web服务器的客户端最原始的IP地址的HTTP请求头字段。

简单地说，xff是告诉服务器当前请求者的最终ip的http请求头字段
通常可以直接通过修改http头中的X-Forwarded-For字段来仿造请求的最终ip


Referer

维基百科：

    HTTP来源地址（referer，或HTTPreferer）
    是HTTP表头的一个字段，用来表示从哪儿链接到当前的网页，采用的格式是URL。换句话说，借着HTTP来源地址，当前的网页可以检查访客从哪里而来，这也常被用来对付伪造的跨网站请求。

简单的讲，referer就是告诉服务器当前访问者是从哪个url地址跳转到自己的，跟xff一样，referer也可直接修改

X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项

HTTP Referer是header的一部分，当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器我是从哪个页面链接过来的

1、将Firefox的插件FoxProxy设置为127.0.0.1:8080(对全部URLs使用)
2、打开burpsuite，Proxy->Intercept is on
3、点击题目场景的http地址，在Proxy下收到请求包，右键Send to Repeater
4、在Repeater中的Request中Raw窗口添加X-Forwarded-For: 123.123.123.123，点击左上角的Send，出现：
<script>
document.getElementById("demo").innerHTML="必须来自https://www.google.com";
</script>
5、在Repeater中的Request中Raw窗口添加Referer: https://www.google.com，点击左上角的Send，出现：
<script>
document.getElementById("demo").innerHTML="cyberpeace{fd25213d0495c846a4c73e2026107653}";
</script>


wp第11条，第14条
1、使用火狐Modify  Header  Value插件，URL一栏填的是目标网站，在本题环境中填的就是题目的URL。HeaderName那一栏填的是你请求头里面要加的东西，比如现在我加上了Referer。HeaderValue那一栏填的是你加的头部字段的值，在本题中Referer是google、XFF是123.123.123.123
