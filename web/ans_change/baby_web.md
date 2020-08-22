1、使用dirsearch工具得到网站的目录：

dudu@kali:~/dirsearch$ python3 dirsearch.py -u http://220.249.52.133:34382/  -e *
[15:25:40] Starting: 
[15:25:41] 403 -  305B  - /.htaccess-dev                              
[15:25:41] 403 -  307B  - /.htaccess-local
[15:25:41] 403 -  307B  - /.htaccess-marco
[15:25:41] 403 -  306B  - /.htaccess.bak1
[15:25:41] 403 -  305B  - /.htaccess.old
[15:25:41] 403 -  308B  - /.htaccess.sample
[15:25:41] 403 -  305B  - /.htaccess.txt
[15:25:41] 403 -  306B  - /.htaccess.save
[15:25:41] 403 -  304B  - /.htaccessBAK
[15:25:41] 403 -  306B  - /.htaccess.orig
[15:25:41] 403 -  304B  - /.htaccessOLD
[15:25:41] 403 -  305B  - /.htaccessOLD2
[15:25:41] 403 -  305B  - /.htpasswd-old
[15:25:41] 403 -  303B  - /.httr-oauth
[15:25:42] 200 -   11B  - /1.php                                                  
[15:25:46] 302 -   17B  - /index.php  ->  1.php                                                                   
[15:25:46] 302 -   17B  - /index.php/login/  ->  1.php
[15:25:47] 403 -  305B  - /server-status                                                                
[15:25:47] 403 -  306B  - /server-status/ 
                                                                                                                  
Task Completed
2、使用burpsuite抓index.php的包
开始是 http://220.249.52.133:34382/1.php
抓http://220.249.52.133:34382/index.php的包

其中Request的信息为：
GET /index.php HTTP/1.1
Host: 220.249.52.133:34382
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

Response的信息为：
HTTP/1.1 302 Found
Date: Wed, 19 Aug 2020 07:38:59 GMT
Server: Apache/2.4.38 (Debian)
X-Powered-By: PHP/7.2.21
FLAG: flag{very_baby_web}
Location: 1.php
Content-Length: 17
Connection: close
Content-Type: text/html; charset=UTF-8

Flag is hidden!
