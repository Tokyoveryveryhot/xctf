1、IDA拖入文件，发现是32位程序
2、跟进main函数，发现就是输出随机数计算的题目，找到关键变量strs
3、点击strs，发现strs即为9447{This_is_a_flag}

wp:
1、使用exeinfo pe查看壳和程序的相关信息
2、运行fule insanty查看程序详细信息
3、放入IDA，发现关键字符串&strs，跟进strs


1、strings insantity查看字符串