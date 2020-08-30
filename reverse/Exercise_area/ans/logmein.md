IDA打开后F5查看，代码如下：
#include <iostream>
#include <string>
using namespace std;

#define _BYTE unsigned char

int main()
{
   string v8=":\"AL_RT^L*.?+6/46";
	char s[20];
	__int64_t v7=28537194573619560;//'ebmarah'小端序，需要逆过来
	int v6=7;
	cout<<v8.length();
	for ( int i = 0; i < v8.length(); ++i )
  {
    if ( i >= v8.length() )
      cout<<"out"<<endl;
    s[i] = (char)(*((_BYTE *)&v7+i%v6)^v8[i]); 
      cout<<s[i];
  }
   return 0;
}

值得注意的是 v7 = 28537194573619560LL;的意思是long long v7=28537194573619560;
放在代码中的意思是__int64_t v7=28537194573619560LL;

wp:第1条和
1、paython实现，由于程序是小段的存储方式，所以，ebmarah就得变成harambe

ord():是将字符串转换为ascii格式，为了方便运算

chr():是将ascii转换为字符串