本题是关于PHP代码审计的：
<?php
show_source(__FILE__);
include("config.php");
$a=@$_GET['a'];
$b=@$_GET['b'];
if($a==0 and $a){
    echo $flag1;
}
if(is_numeric($b)){
    exit();
}
if($b>1234){
    echo $flag2;
}
?> 

这段php代码的意思是，通过get方法得到a和b的值，然后如果满足a==0 并且a为真，得到flag1，如果b不是数字且b>1234就得到flag2.

php是弱类型语言。如果遇到参数类型不一样的情况会实现隐式转换，在本题中我们设置a=0a，在"=="判断时，会被系统转换为0，且本身不为false，满足条件；设置b=12345a，这样b不会被判为数字，且b大于1234

1、php是弱类型语言：强类型的语言遇到函数引数类型和实际调用类型不匹配的情况经常会直接出错或者编译失败；
而弱类型的语言常常会实行隐式转换，或者产生难以意料的结果。

2、字符串和数字比较使用==时,字符串会先转换为数字类型再比较 php var_dump('a' == 0);//true，这里'a'会被转换数字0 var_dump('123a' == 123);//true，这里'123a'会被转换为123。$a==0 and $a，a=a即可，$b>1234且!is_numeric($b)，b=12345a（php是弱类型，所以输入'0'==0成立；b不能是数字但是要和数字比较，可以用数组b[]=5678）

3、在判断语句里，要求a==0，并且a不为0；看到两个等号，想到php弱等于，这里可以让a=admin，在“==”判断是，admin会被转换成“0”，a满足条件 然后是b，is_numeric这个函数要求b不能是数字，下面要求b大于1234，这里可以让b=2345%00，%00是空格的意思，这样b就不会被判断为数字，且大于1234，b满足条件。 构造url：http://111.198.29.45:40060/?a=admin&b=2345%00,即可得到flag。

wp第2条，第8条

1、通过阅读代码发现需要同时满足a==0且if a为真，b不是数字且b>1234才会返回flag
$a==$b                       等于                                               TRUE，如果类型转换后$a等于$b
$a===$b                     全等                                                TRUE，如果$a等于$b，且他们的类型也相同

“0”为true，可以把参数a构造为'0'或者'abc'这种在'=='判断中转换后为0且本身不为false；数字和字符混合的字符串转换为整数后只保留数字。

2、当一个字符串当作一个数值来取值，其结果和类型如下:如果该字符串没有包含’.’,’e’,’E’并且其数值值在整形的范围之内,该字符串被当作int来取值，其他所有情况下都被作为float来
取值，该字符串的开始部分决定了它的值，如果该字符串以合法的数值开始，则使用该数值，否则其值为0如："0e11"=="0e22"比较的时候，会将这类字符串识别为科学技术法的数字，所以0的多少次方都是零。
"A"==0比较的时候，会将A转化成数值，强制转化,由于A是字符串，转化的结果是0自然和0相等。
"1A"==1比较的时候会将1A转化成为数值1；但“A1“==1结果却为false，也就是"A1"转化成了0。








a=[0]&b[]=5555555 这个也是可以过地，大部分这种问题都可以使用数组然绕过

https://www.secpulse.com/archives/69529.html

<?php
var_dump("admin"==0); //true
var_dump("1admin"==1); //true
var_dump("admin1"==1) //false
var_dump("admin1"==0) //true
var_dump("0e123456"=="0e4456789"); //true
?> 


https://blog.spoock.com/2016/06/25/weakly-typed-security/
几个问题：
类型转换：
0=='0'		//true
0 == 'abcdefg'	//true
0 === 'abcdefg'	//false
1 == '1abcdef'	//true
Hash比较：
"0e132456789"=="0e7124511451155" //true
有问题："0e123456abc"=="0e1dddada"	//false
"0e1abc"=="0"     //true
十六进制转换：
有问题"0x1e240"=="123456"		//true
"0x1e240"==123456		//true
"0x1e240"=="1e240"		//false
类型转换：
int->string
$var = 5;
方式1：$item = (string)$var;
方式2：$item = strval($var);

var_dump(intval('2'))	//2
var_dump(intval('3abcd'))	//3
var_dump(intval('abcd'))	//0

内置函数的参数的松散性：
1、md5()函数
$array1[] = array(
    "foo" => "bar",
    "bar" => "foo",
);
$array2 = array("foo", "bar", "hello", "world");
var_dump(md5($array1)==var_dump($array2));	//true
PHP手册中的md5()函数的描述是string md5 ( string $str [, bool $raw_output = false ] )，md5()中的需要是一个string类型的参数。但是当你传递一个array时，md5()不会报错，知识会无法正确地求出array的md5值，这样就会导致任意2个array的md5值都会相等。这个md5()的特性在攻防平台中的bypass again同样有考到。

2、strcmp()函数
strcmp()函数在PHP官方手册中的描述是int strcmp ( string $str1 , string $str2 ),需要给strcmp()传递2个string类型的参数。如果str1小于str2,返回-1，相等返回0，否则返回1。strcmp函数比较字符串的本质是将两个变量转换为ascii，然后进行减法运算，然后根据运算结果来决定返回值。
如果传入给出strcmp()的参数是数字呢？

$array=[1,2,3];
var_dump(strcmp($array,'123')); //null,在某种意义上null也就是相当于false。
strcmp这种特性在攻防平台中的pass check有考到。

3、switch()函数
如果switch是数字类型的case的判断时，switch会将其中的参数转换为int类型。如下：

$i ="2abc";
switch ($i) {
case 0:
case 1:
case 2:
    echo "i is less than 3 but not negative";
    break;
case 3:
    echo "i is 3";
}
这个时候程序输出的是i is less than 3 but not negative，是由于switch()函数将$i进行了类型转换，转换结果为2。

4、in_array()函数
在PHP手册中，in_array()函数的解释是bool in_array ( mixed $needle , array $haystack [, bool $strict = FALSE ] ),如果strict参数没有提供，那么in_array就会使用松散比较来判断$needle是否在$haystack中。当strince的值为true时，in_array()会比较needls的类型和haystack中的类型是否相同。

$array=[0,1,2,'3'];
var_dump(in_array('abc', $array));  //true
var_dump(in_array('1bc', $array));	//true
可以看到上面的情况返回的都是true,因为’abc’会转换为0，’1bc’转换为1。
array_search()与in_array()也是一样的问题

https://www.cnblogs.com/Mrsm1th/p/6745532.html
=== 在进行比较的时候，会先判断两种字符串的类型是否相等，再比较
== 在进行比较的时候，会先将字符串类型转化成相同，再比较

php手册：
当一个字符串当作一个数值来取值，其结果和类型如下:如果该字符串没有包含'.','e','E'并且其数值值在整形的范围之内
该字符串被当作int来取值，其他所有情况下都被作为float来取值，该字符串的开始部分决定了它的值，如果该字符串以合法的数值开始，则使用该数值，否则其值为0。
1 <?php
2 $test=1 + "10.5"; // $test=11.5(float)
3 $test=1+"-1.3e3"; //$test=-1299(float)
4 $test=1+"bob-1.3e3";//$test=1(int)
5 $test=1+"2admin";//$test=3(int)
6 $test=1+"admin2";//$test=1(int)
7 ?>

1、md5绕过(Hash比较缺陷)
<?php
if (isset($_GET['Username']) && isset($_GET['password'])) {
    $logined = true;
    $Username = $_GET['Username'];
    $password = $_GET['password'];

     if (!ctype_alpha($Username)) {$logined = false;}
     if (!is_numeric($password) ) {$logined = false;}
     if (md5($Username) != md5($password)) {$logined = false;}
     if ($logined){
    echo "successful";
      }else{
           echo "login failed!";
        }
    }
?>
md5开头是0e的字符串 上文提到过，0e在比较的时候会将其视作为科学计数法，所以无论0e后面是什么，0的多少次方还是0。md5('240610708') == md5('QNKCDZO')成功绕过!


2、json绕过
<?php
if (isset($_POST['message'])) {
    $message = json_decode($_POST['message']);
    $key ="*********";
    if ($message->key == $key) {
        echo "flag";
    } 
    else {
        echo "fail";
    }
 }
 else{
     echo "~~~~";
 }
?>
但是可以利用0=="admin"这种形式绕过，最终payload message={"key":0}


3、array_search&is_array绕过
<?php
if(!is_array($_GET['test'])){exit();}
$test=$_GET['test'];
for($i=0;$i<count($test);$i++){
    if($test[$i]==="admin"){
        echo "error";
        exit();
    }
    $test[$i]=intval($test[$i]);
}
if(array_search("admin",$test)===0){
    echo "flag";
}
else{
    echo "false";
}
?>
payload test[]=0可以绕过

1 <?php
2 $a=array(0,1);
3 var_dump(array_search("admin",$a)); // int(0) => 返回键值0
4 var_dump(array_seach("1admin",$a));  // int(1) ==>返回键值1
5 ?>
array_search函数 类似于== 也就是$a=="admin" 当然是$a=0  当然如果第三个参数为true则就不能绕过


4、strcmp漏洞绕过 php -v <5.3
<?php
    $password="***************"
     if(isset($_POST['password'])){

        if (strcmp($_POST['password'], $password) == 0) {
            echo "Right!!!login success";n
            exit();
        } else {
            echo "Wrong password..";
        }
?>
我们传入 password[]=xxx 可以绕过 是因为函数接受到了不符合的类型，将发生错误，但是还是判断其相等
payload: password[]=xxx

5、switch绕过
<?php
$a="4admin";
switch ($a) {
    case 1:
        echo "fail1";
        break;
    case 2:
        echo "fail2";
        break;
    case 3:
        echo "fail3";
        break;
    case 4:
        echo "sucess";  //结果输出success;
        break;
    default:
        echo "failall";
        break;
}
?>

https://www.php.net/manual/zh/types.comparisons.php
PHP类型比较表
Note:
HTML 表单并不传递整数、浮点数或者布尔值，它们只传递字符串。要想检测一个字符串是不是数字，可以使用 is_numeric() 函数。
Note:
在没有定义变量 $x 的时候，诸如 if ($x) 的用法会导致一个 E_NOTICE 级别的错误。所以，可以考虑用 empty() 或者 isset() 函数来初始化变量。
松散比较表
太长不看