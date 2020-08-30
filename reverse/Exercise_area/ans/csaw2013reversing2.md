1、使用exeinfo PE查看文件的信息，发现程序是32位没有加壳
2、实际运行该程序，发现不能运行，出现中止，调试，忽略三个选项的对话框。
2、使用IDA加载exe，得到程序的大致流程，发现有判断语句if ( sub_40102A() || IsDebuggerPresent() )，其中IsDebuggerPresent() 函数读取当前进程的PEB里BeingDebugged的值用于判断自己是否处于调试状态。
说明调试与实际运行的流程会有偏差。
其中MessageBoxA(0, (LPCSTR)lpMem + 1, "Flag", 2u);就是三个选项的对话框
而且进入判断语句中，有防止调试的语句__debugbreak()
3、使用OD进行调试，进入该判断语句，使用空格或双击将0125109A的int 3改为nop，动态调试函数sub_401000，F7进行该函数内部，发现关键语句mov edx, [ebp+lpMem]

loc_40101F:
xor     [edx+ecx*4], esi
inc     ecx
cmp     ecx, eax
jb      short loc_40101F

PS：IDA给的语句貌似不是很准（在IDA的流程图状态下按下/就会在汇编语句中出现伪代码）

4、在Hex Dump窗口按下Ctrl+G查看EDX地址(4C07E0)所指向的值，找到flag


wp：
1、可以看到有个关键函数sub_401000， 意思是如果在动态调试器中就进入判断运行，如果没有直接弹窗，显示乱码的值，改掉int3，可以看出mov edx,[ebp+lpMem]对应的汇编指令地址,单步运行F8，执行了mov指令，接下来调用call，F8继续执行，执行完，edx存的就是flag的地址

wp的第一条
