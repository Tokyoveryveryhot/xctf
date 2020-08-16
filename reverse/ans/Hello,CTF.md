v10==v13
v10=v8=v4=v9[v3]
v9是输入，如果v9[i]为0，退出，否则v4=v9[i]
v13是a437261636b4d65

cin>>v9;
while(1)
{
    v4=v9[i];
    if(!v4)
        break;
    sprintf(v8,"%x",v4);
    strcat(v10,v8);
}
if(strcmp(v10,v13))
    printf("Success");

需要将437261636b4d654a757374466f7246756e转化为ASCII字符串

打开网站进行转换或使用Winhex查看或写程序查看：

#include<stdio.h>
int main(void)
{
    char table[]="437261636b4d654a757374466f7246756e";
    int ch;
    for(inti=0;i<18;i++)
    {
        sscanf(table+2*i,"%2x",&ch);
        putchar(ch);    
    }
    return0;
}