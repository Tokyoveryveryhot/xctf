1、手动脱壳，失败
wp的方法有以下两种：
1、UPX工具脱壳
1)用LoadPE（exeinfo pe）查看二进制文件，发现加了UPX的壳
2)在kali下使用upx -d  simple_unpack，脱壳
3)在IDA中查看strings，发现flag

2、取巧：
1)在UE中直接搜索flag
2)在shell中输入xxd simple_unpack | grep flag，得到flag字符串出现的位置0x000ca0a0，
再次输入命令xxd simple_unpack | grep 000ca0，得到flag
