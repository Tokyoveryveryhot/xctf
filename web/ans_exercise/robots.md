Robots协议（也称为爬虫协议、机器人协议等）的全称是“网络爬虫排除标准”（Robots Exclusion Protocol），网站通过Robots协议告诉搜索引擎哪些页面可以抓取，哪些页面不能抓取。

         robots.txt文件是一个文本文件, 是一个协议而不是一个命令.  当爬虫访问一个站点时， 它会首先检查该站点根目录下是否存在robots.txt，如果存在，爬虫就会按照该文件中的内容来确定访问的范围；如果该文件不存在，所有的爬虫将能够访问网站上所有没有被口令保护的页面。

robots.txt是搜索引擎中访问网站的时候要查看的第一个文件。当一个搜索蜘蛛访问一个站点时，它会首先检查该站点根目录下是否存在robots.txt，如果存在，搜索机器人就会按照该文件中的内容来确定访问的范围；如果该文件不存在，所有的搜索蜘蛛将能够访问网站上所有没有被口令保护的页面。

 样例:

       User-agent: *

       Disallow:  /

       Allow: /public/

 

    以上表明爬虫只充许爬取public目录，将上面的内容保存为robots.txt文件，放在网站的根目录下，和网站的入口文件(  index.html,index.htm等)在一起即可. 

 

    配置项详解:

        User-agent 指定爬虫名, *代表任何爬虫。 如有多条User-agent记录，则可以限制多个爬虫，但至少需要指定一条. 

        Disallow:不允许爬取的目录。 

       Allow:一般配合Disallow使用，用于排除限制。 

       本题中的flag_ls_h3re.php是disallow状态，但是这只是一种道德规范，而非必要手段。

       Nikto是一款开源的（GPL）网页服务器扫描器，它可以对网页服务器进行全面的多种扫描

       nikto -h 192.168.68.139