0、把AscII字符转换为十六进制   
  char   *sss   =   "12AB";   
  int   a;   
  sscanf(sss,   "%X",   &a);   
    
  把十六进制转换位AscII字符   
  char   buf[100];   
  int   a   =   0x1234;   
  sprintf(buf,   "%X",   a);  google的实现

1、利用hash表实现：
#include <string>
#include <map>
#include <iostream>
using namespace std;
string getValue(string temp);
map<char,int> hexMap;
 
int main()
{
    hexMap['0']=0;hexMap['1']=1;hexMap['2']=2;hexMap['3']=3;hexMap['4']=4;hexMap['5']=5;
    hexMap['6']=6;hexMap['C']=12;hexMap['7']=7;hexMap['8']=8;hexMap['9']=9;hexMap['A']=10;
    hexMap['B']=11;hexMap['D']=13;hexMap['E']=14;hexMap['F']=15;hexMap['c']=12;
    hexMap['a']=10;hexMap['b']=11;hexMap['d']=13;hexMap['e']=14;hexMap['f']=15;
    string temp="4a"; //十六进制
    cout<<getValue(temp)<<endl;
    return 0;
}
string getValue(string temp)
{
    int i=0;
    char s[2] ;
    s[0] = hexMap[temp[i]]*16+hexMap[temp[i+1]];
    s[1]='\0';
    string  ASCII= s;
    return ASCII;
}

2、利用sscanf函数进行实现
#include<stdio.h>
#include<string.h>
int main()
{
    char table[]="437261636b4d654a757374466f7246756e";
    int TABLE_SIZE=strlen(table)+1;
    int ch;
    char szBuffer[TABLE_SIZE];
    for (i=0;i<strlen(table);i++)
    {
        sscanf_s((tabke+i*2),"%02X",(szBuffer+i));
        sscanf(table+i*2,"%2x",&ch);
        putchar(ch)
    }
    printf("%s",szBuffer);
    return 0;
}


3、利用ASCII码表的值进行转换
#include <iostream>
 
//每2位16进制转换一个字符，p指针指向的字符串在ToChar函数中只处理2位，循环处理即可
char ToChar(const char * p)
{
    unsigned char * cursor=(unsigned char *)p;
    char c;
    if(*cursor>='0'&&*cursor<='9')
        c=(*cursor-'0')<<4;
    else if(*cursor>='A'&&*cursor<='Z')
        c=(*cursor-'A'+10)<<4;
    else if(*cursor>='a'&&*cursor<='z')
        c=(*cursor-'a'+10)<<4;
    else
        return char(-1);
    if(*(cursor+1)>='0'&&*(cursor+1)<='9')
        c=(*(cursor+1)-'0');
    else if(*(cursor+1)>='A'&&*(cursor+1)<='Z')
        c=(*(cursor+1)-'A'+10);
    else if(*(cursor+1)>='a'&&*(cursor+1)<='z')
        c=(*(cursor+1)-'a'+10);
    else
        return char(-1);
     
    return (char)c;
}
int  main(int argc, char * argv[])
{
    char buff[]="1b40";
    char array[3]="";
    array[0]=ToChar(buff);
    array[1]=ToChar(buff+2);
    printf("%s\n",array);
    return 0;
}

4、利用python进行实现
key="3934347b796f5f61725f616e696e74726e61696f6e6c5f6d737465797d"

flag=key.decode('hex')
print flag

