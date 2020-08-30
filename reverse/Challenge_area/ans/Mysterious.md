1、exeinfo打开没有加壳，32位可执行程序
2、在main函数中：
      char v14,v15,v16;
      int v12 = atol(String[0]) + 1;
      if ( v12 == 123 && v14 == 120 && v16 == 122 && v15 == 121 )
      {
        strcpy(Text, "flag");
        memset(&v9, 0, 0xFCu);
        v10 = 0;
        v11 = 0;
        _itoa(v12, &v7, 10);
        strcat(Text, "{");
        strcat(Text, &v7);
        strcat(Text, "_");
        strcat(Text, "Buff3r_0v3rf|0w");
        strcat(Text, "}");
        MessageBoxA(0, Text, "well done", 0);
      }
注意此处v12为123,itoa转为字符串“123”，
注意v12在判断之前进行了+1，所以输入时应该是123-1，结合代码，得出
输入122xyz，可得到flag。
