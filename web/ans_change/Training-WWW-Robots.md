1、使用dirsearch工具得到网站的目录：

dudu@kali:~/dirsearch$ python3 dirsearch.py -u http://220.249.52.133:36698/  -e *

[15:48:31] Starting:                                                                                                                                                                                                                       
[15:48:32] 403 -  297B  - /.htaccess-dev                                                                                                                                                                                                   
[15:48:32] 403 -  299B  - /.htaccess-local                                                                                                                                                                                                 
[15:48:32] 403 -  299B  - /.htaccess-marco                                                                                                                                                                                                 
[15:48:32] 403 -  298B  - /.htaccess.bak1                                                                                                                                                                                                  
[15:48:32] 403 -  297B  - /.htaccess.old                                                                                                                                                                                                   
[15:48:32] 403 -  298B  - /.htaccess.orig                                                                                                                                                                                                  
[15:48:32] 403 -  297B  - /.htaccess.txt                                                                                                                                                                                                   
[15:48:32] 403 -  298B  - /.htaccess.save                                                                                                                                                                                                  
[15:48:32] 403 -  300B  - /.htaccess.sample                                                                                                                                                                                                
[15:48:32] 403 -  296B  - /.htaccessBAK                                                                                                                                                                                                    
[15:48:32] 403 -  296B  - /.htaccessOLD                                                                                                                                                                                                    
[15:48:32] 403 -  297B  - /.htaccessOLD2                                                                                                                                                                                                   
[15:48:32] 403 -  297B  - /.htpasswd-old                                                                                                                                                                                                   
[15:48:32] 403 -  295B  - /.httr-oauth                                                                                                                                                                                                     
[15:48:32] 403 -  288B  - /.php                                                                                                                                                                                                            
[15:48:36] 200 -  523B  - /index.php                                                                                                                                                                                                       
[15:48:36] 200 -  523B  - /index.php/login/
[15:48:38] 200 -   71B  - /robots.txt                                                                   
[15:48:38] 403 -  297B  - /server-status                                                                
[15:48:38] 403 -  298B  - /server-status/
                                                                                                                  
Task Completed  

2、访问http://220.249.52.133:36698/robots.txt
User-agent: *
Disallow: /fl0g.php


User-agent: Yandex
Disallow: *

3、访问http://220.249.52.133:36698/fl0g.php
得到flag：cyberpeace{4d42e2b0b0cd3323a27ac33ad69ef72a}

附录：
robots.txt是一个协议，而不是一个命令。robots.txt是搜索引擎中访问网站的时候要查看的第一个文件。robots.txt文件告诉蜘蛛程序在服务器上什么文件是可以被查看的。

当一个搜索蜘蛛访问一个站点时，它会首先检查该站点根目录下是否存在robots.txt，如果存在，搜索机器人就会按照该文件中的内容来确定访问的范围；如果该文件不存在，所有的搜索蜘蛛将能够访问网站上所有没有被口令保护的页面。百度官方建议，仅当您的网站包含不希望被搜索引擎收录的内容时，才需要使用robots.txt文件。如果您希望搜索引擎收录网站上所有内容，请勿建立robots.txt文件。

如果将网站视为酒店里的一个房间，robots.txt就是主人在房间门口悬挂的“请勿打扰”或“欢迎打扫”的提示牌。这个文件告诉来访的搜索引擎哪些房间可以进入和参观，哪些房间因为存放贵重物品，或可能涉及住户及访客的隐私而不对搜索引擎开放。但robots.txt不是命令，也不是防火墙，如同守门人无法阻止窃贼等恶意闯入者。

Robots协议用来告知搜索引擎哪些页面能被抓取，哪些页面不能被抓取；可以屏蔽一些网站中比较大的文件，如：图片，音乐，视频等，节省服务器带宽；可以屏蔽站点的一些死链接。方便搜索引擎抓取网站内容；设置网站地图连接，方便引导蜘蛛爬取页面。
