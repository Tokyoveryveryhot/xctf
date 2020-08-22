知识点1:
在linuxshell中，假如有如下语句,这就是shell注入方面echo ‘’;ls;cat 1.txt;/bin/sh;’’则ls、cat 1.txt、/bin/sh这三个命令会依次执行，这也就是本题突破的关键
知识点2:
C语言或C++申请内存后，用free或delete释放堆后，指针的值还在，如果不手动设置为NULL，就可以被我们利用。

当前一个堆释放后，新创建的堆的地址就是前一个堆的地址，指针仍然指向原来的堆地址。

选项5退出时，释放了堆内存，但是并没有将指针设置为NULL，因此指针仍然指向原来的那个地址。

选项4，有system，这里判断ptr的内容是否为空，于是我们在退出时，选择不退出，这样我们释放了第一个堆，
然后我们在选项3中输入注入语句，创建的堆的地址就是第一个堆的地址，也就是ptr指向的内容，最后再选择4，执行getshell。
这就是UAF(use After Free)漏洞，通过UAF使得set_time_zone分配得到的是set_format释放掉的内存。


在函数400F8F中，先释放ptr指针，再询问是否退出，若不退出，则原来指针有被利用的风险


利用方法：uaf

先malloc一个format字符串，随便填几个字符
然后free它，（ 这里并没有malloc timezone，不过经过百度，free()一个空指针是没事的）
（此时fastbin里面存上了format的chunk，但是指针还有），然后选项3，malloc 那个timezone，这样写入timezone就是写入format了
别忘了要选项3设置一个时间，要不程序进行不下去
最后在选项4 print


利用use after free

选择1设置 格式化字符串 （malloc(n)）
选择3设置时区 (malloc(n))，传入参数/bin/sh，利用’’\将参数括起来，‘；’用来传参
选择5 退出 (选择否 ， 目的是 free上面的两个块)
选择3设置时区(消耗时区 free的块)
选择4设置时区 （使用格式化字符串free的块）



1、int snprintf ( char * str, size_t size, const char * format, ... );
参数str -- 目标字符串。
size -- 拷贝字节数(Bytes)。
format -- 格式化成字符串。
... -- 可变参数
我的IDA出现问题，反汇编的结果为__snprintf_chk(&command,2048LL,1LL,2048LL,"/bin/date -d @%d +'%s'",(unsigned int)dword_602120);
而实际上的反汇编为__snprintf_chk(&command,2048LL,1LL,2048LL,"/bin/data -d @%d + '%s'",(unsigned int)dword_602120,ptr,a3);
system(&command)
如果我们可以控制command就可以getshell了，但是command由ptr，也就是我们输入的format控制

按下1，
fgets(s,1024,stdin)
v0=strdup(s)//malloc+strcpy
qword_602118=v0
按下3，
fgets(s,1024,stdin)
value=strdup(s)
按下4，
__snprintf_chk(&command,2048LL,1LL,2048LL,"/bin/data -d @%d + '%s'",(unsigned int)dword_602120,qword_602118,a3);
system(&command)
按下5，
free(qword_602118)->format
free(value)->time zone


