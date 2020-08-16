RAR文件格式分析：
https://blog.csdn.net/Claming_D/article/details/105899397

使用WinRAR打开附件，发现secret.png的文件头损坏了，并且还有一个flag.txt
flag.txt没有flag，使用winhex打开附件
看到从here后面开始就应该是secret.png的部分了，百度了一下rar每个块的开头
要的是文件块而不是子块，于是更改0x53位置的7A为74，成功解压，发现是一张空白的图片，继续用winhex打开
从here后面开始就应该是secret.png的部分了，百度了一下rar每个块的开头
我们要的是文件块而不是子块，于是更改7A为74，成功解压，发现是一张空白的图片，继续用winhex打开
发现是gif格式，将其重命名并用PhotoShop打开，发现有两个空白的图层
将两个图层分别提取出来，用StegSolve打开，不断点击箭头直到显示出图像
将两幅二维码拼接到一起并补全定位点，扫描二维码得到flag
具体参照https://blog.csdn.net/tqydyqt/article/details/101992518
