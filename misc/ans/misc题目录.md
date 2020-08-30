## this_is_flag
题目中直接给出

## pdf
pdf信息隐藏，**题解**:

1、使用chrome打开pdf，ctrl+F搜索flag，出现1处

2、ctrl+A选中，ctrl+C复制，ctrl+V粘贴到文本中

## give_you_flag
gif动图信息隐藏，**题解**：

1、下载附件，打开gif图会看到小龙人数完钞票会展示二维码，使用stegsolve等工具（需要安装Java，然后配环境变量才能使用）查看帧数得到二维码(点击Analyse - Frame Browser动图分解，发现二维码)

2、二维码缺少三个小方块，而这些小方块被称为定位图案，用于标记二维码矩形的大小，用三个定位图案可以标识并确定一个二维码矩形的位置和方向。

3、使用save保存图片，使用工具ps或画图将二维码修复完全便可获得完整二维码，使用SO JSON在线工具扫描获得flag。

**注意**：P了很多次，才成功的，要主要定位符和二维码直接要留白。

## 坚持60s
java反汇编，**题解**：

1、使用Java Decompiler GUI打开jar包，搜素flag，得到flag{RGFqaURhbGlfSmlud2FuQ2hpamk=}，提交发现不正确；看到=号想起base64解码，解码得到真正的flag

2、也可以直接解压jar包，挨个文件搜索flag，直到cn/bjsxt/plane目录下看到PlaneGameFrame.class中出现flag{RGFqaURhbGlfSmlud2FuQ2hpamk=},然后再提交base64解码，得到真正的flag

## gif
解压图片黑白联系二进制，**题解**:

打开文件出现多个黑白，让人联想到二进制，白色图片代表0，黑色图片代表1。

01100110前八位二进制换算后为 f 证明思路正确。

01100110011011000110000101100111011110110100011001110101010011100101111101100111011010010100011001111101

使用网页工具（在线转换二进制到字符串）二进制转字符串得到 flag

## 掀桌子
给组密码，**题解**

十六进制转为十进制，减去128，转为ASCII

方法一：
```python
string = "c8e9aca0c6f2e5f3e8c4efe7a1a0d4e8e5a0e6ece1e7a0e9f3baa0e8eafae3f9e4eafae2eae4e3eaebfaebe3f5e7e9f3e4e3e8eaf9eaf3e2e4e6f2"
flag = ''
for i in range(0,len(string), 2):
    s = "0x" + string[i] + string[i+1]
    flag += chr(int(s, 16) - 128)
print(flag)
```
方法二：
```python
import re
a=‘c8e9aca0c6f2e5f3e8c4efe7a1a0d4e8e5a0e6ece1e7a0e9f3baa0e8eafae3f9e4eafae2eae4e3eaebfaebe3f5e7e9f3e4e3e8eaf9eaf3e2e4e6f2’
b=re.findall(r'.{2}',a)
flag=' ' 
int i in b:
    flag+=chr(int(int(i,16)-128))
print(flag)
```

## 如来十三掌
给段密码，**题解**：

通过与佛论禅，rot-13，base64进行解码：

## stegano
pdf文档隐写，**题解**：

1、打开pdf文档，ctrl+a全选所有文字，ctrl+c复制全部文档

2、在记事本中ctrl+v粘贴所有文字

3、在第二行发现BABA BBB BA BBA ABA AB B AAB ABAA AB B AA BBB BA AAA BBAABB AABA ABAA AB BBA BBBAAA ABBBB BA AAAB ABBBB AAAAA ABBBB BAAA ABAA AAABB BB AAABB AAAAA AAAAA AAAAB BBA AAABB

4、看到AB想到培根密码，但培根密码5个一组，于是想到摩斯密码，将A替换为.，B替换为-，在线网站解密，得到flag

## simpleRAR
RAR文件隐写。[winRAR文件格式](https://blog.csdn.net/Claming_D/article/details/105899397)，**题解**：

使用WinRAR打开附件，发现secret.png的文件头损坏了，并且还有一个flag.txt。

flag.txt没有flag，使用winhex打开附件。

看到从here后面开始就应该是secret.png的部分了，百度了一下rar每个块的开头。

要的是文件块而不是子块，于是更改0x53位置的7A为74，成功解压，发现是一张空白的图片，继续用winhex打开
从here后面开始就应该是secret.png的部分了，

成功解压，发现是一张空白的图片，继续用winhex打开

发现是gif格式，将其重命名并用PhotoShop打开，发现有两个空白的图层

将两个图层分别提取出来，用StegSolve打开，不断点击箭头直到显示出图像

将两幅二维码拼接到一起并补全定位点，扫描二维码得到flag

具体参照https://blog.csdn.net/tqydyqt/article/details/101992518

## base64stego
zip文件隐写。**题解**：

1、.7zip解压base64stego.zip文件，得到stego.txt文件，使用UE打开

2、使用base64在线解密得到一段隐写术的介绍，怀疑使用了隐写术

3、查看writeup得知base64隐写的原理可得出结论：
        
        (1)base64加密后结尾无“=”号的无隐写位。
        (2)base64加密后结尾有1个“=”号的有2位隐写位。
        (3)base64加密后结尾有2个“=”号的有4位隐写位。

首先判断每行数据的可隐写位数，然后将可隐写的每行最后一个字符根据base64码表，对应到相应的值，接着转为二进制，根据可隐写位数截取相应的位数，然后拼接这些隐写位，最后从左到右每8位一组截取二进制，分别将其转为十进制并对应ASCII码表，打印出相应的字符即可得到flag。

4、编写python脚本实现：

思路是先循环解密base64字符串，提取出可以隐写的最后2-4位，再拼接最后转回ascii码flag就出来了

```python
#coding=utf-8
def get_base64_diff_value(s1, s2):
    base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    res = 0
    for i in xrange(len(s2)):
        if s1[i] != s2[i]:
            return abs(base64chars.index(s1[i]) - base64chars.index(s2[i]))
    return res

def solve_stego():
    with open('1.txt', 'rb') as f:
        file_lines = f.readlines()
        bin_str = ''
        for line in file_lines:
            steg_line = line.replace('\n', '')
            norm_line = line.replace('\n', '').decode('base64').encode('base64').replace('\n', '')
            diff = get_base64_diff_value(steg_line, norm_line)
            print diff
            pads_num = steg_line.count('=')
            if diff:
                bin_str += bin(diff)[2:].zfill(pads_num * 2)
            else:
                bin_str += '0' * pads_num * 2
            print goflag(bin_str)

def goflag(bin_str):
    res_str = ''
    for i in xrange(0, len(bin_str), 8):
        res_str += chr(int(bin_str[i:i + 8], 2))
    return res_str

if __name__ == '__main__':
    solve_stego()
```

wp的第八条，第二条，第十条，第十二条都很不错


## ext3

ext3文件隐写。**题解**：

1、将ext3文件用Winhex打开，搜索flag，得到路径~root/Desktop/file/O7avZhikgKgbF/flag.txt

2、使用.7zip解压工具解码ext3文件，按照上面的路径，找到flag.txt

3、base64解码得到flag{sajbcibzskjjcnbhsbvcjbjszcszbkzj}

wp：

1、记住了"flag"的base64编码的前几个字母是"ZmxhZ"，直接WinHex打开，搜"ZmxhZ"即搜到整个flag的base64编码。

2、首先在/mnt目录下新建一个文件夹，把该光盘挂载到/mnt目录新建的文件夹下： 

root@kali:/mnt# mkdir a 

root@kali:~# mount f1fc23f5c743425d9e0073887c846d23 /mnt/a 

接下来，查看光盘目录a下与flag有关的文件： 

root@kali:~# find /mnt/a -iname "*flag*"，结果为/mnt/a/07avZhikqKqbF/flag.txt 

查看flag.txt文件的内容： 

root@kali:~# cat /mnt/a/O7avZhikgKgbF/flag.txt，结果为ZmxhZ3tzYWpiY2lienNrampjbmJoc2J2Y2pianN6Y3N6Ymt6an0= 

最后使用base64解码： root@kali:~# base64 -d /mnt/a/O7avZhikgKgbF/flag.txt 结果为：flag{sajbcibzskjjcnbhsbvcjbjszcszbkzj} 

完整版:

root@ubuntu $:mkdir ~/ext3

root@ubuntu $:mount ext3 ~/ext3

root@ubuntu $:find . | -name flag.txt

root@ubuntu $:cd 07avZhikgKgbF/

root@ubuntu $:cat flag.txt

root@ubuntu $:base64 -d /mnt/a/O7avZhikgKgbF/flag.txt

## 功夫再高也怕菜刀
pcap文件隐写，**题解**：

1、使用sudo apt-get install foremost安装预装在kali中的foremost工具，使用foremost -h查看是否安装正确

2、进入目录，使用命令foremost -i 功夫再高也怕菜刀.pcapng，分离得到output文件夹。

3、使用chmod 777 output命令给文件夹提权

4、要么这题就是让你求压缩密码，flag就是文本（这种情况密码肯定没那么容易出来），要么就是压缩密码容易求，flag里面又有点东西。经过一番求（sou）索（suo），这一题是第一种情况。

5、在Wireshark中搜索flag，具体操作为点击搜索，选择分组字节流，字符串，添加flag.txt进行查找
一定要把搜索栏按照我标的调，尤其是第一个，它默认不是分组字节流，在这种情况下你搜索flag.txt，结果是搜索不到东西的。会有好几个符合条件的字节流，我看网上wp出奇的一致，都选在了1150这里，我都试了一下，发现结果都是正确的。

6、在1150处右键跟踪TCP流：

7、出现FFD8开始的流，一直到FFD9，选中该段区域，复制

8、在Winhex下新建6M的空文件，之后写入，其中粘贴板的格式为ASCII Hex，保存为.jpg图片

9、打开图片，即为RAR的密码

## base64÷4
base16解密，**题解**：

## Training-Stegano-1
图片隐写，**题解**：

使用Winhex打开图片，得到passward