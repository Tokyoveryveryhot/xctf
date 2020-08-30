https://www.cnblogs.com/yhjoker/p/9831671.html
VScode配置C++环境编译和调试
进行编译和测试环境的配置(出问题，暂时没解决)

1、查看程序，发现三个参数，第一个参数为0xcafe，第二个参数为25，第三个参数为h4cky0u，然后计算  
  unsigned int hash = first * 31337 + (second % 17) * 11 + strlen(argv[3]) - 1615810207;

2、写个程序，输入正确的值即可

  
wp：
1、python实现：
first=int('cafe',16)
print(first)
second=25
argv3='h4cky0u'
hash=int(first*31337+(second%17)*11+len(argv3)-1615810207)
print(hex(hash))
