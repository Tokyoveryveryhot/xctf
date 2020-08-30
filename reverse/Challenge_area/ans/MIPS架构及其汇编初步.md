# [MIPS编程入门](https://www.cnblogs.com/thoupin/p/4018455.htm)

## 数据类型
所有MIPS指令都是32位长的

各单位：1字节=8位，半字长=2个字节，1字长=4个字节

一个字符空间=1个字节

一个整型=一个字长=4个字节

单个字符用单引号，例如：'b'

字符串用双引号，例如："A string"

## 寄存器
MIPS下一共有32个通用寄存器

在汇编中，寄存器标志由$符开头

寄存器表示可以有两种方式：

1、直接使用该寄存器对应的编号，例如：从$0到$31

2、使用对应的寄存器名称，例如：$t1, $sp(详细含义，下文有表格

对于乘法和除法分别有对应的两个寄存器$lo, $hi，不存在直接寻址；必须要通过mfhi("move from hi")以及mflo("move from lo")分别来进行访问对应的内容

栈的走向是从高地址到低地址



## 程序结构：
程序结构为数据声明+普通文本+程序编码

数据声明在代码段后

### 数据声明
数据段以 .data为开始标志
声明变量后，即在主存中分配空间。
```
Note: labels always followed by colon ( : )

example
	
var1:		.word	3	# create a single integer variable with initial value 3
　　　　　　　　　　　　　　　　　　 # 声明一个 word 类型的变量 var1, 同时给其赋值为 3
array1:		.byte	'a','b'	# create a 2-element character array with elements initialized
				#   to  a  and  b
　　　　　　　　　　　　　　　　　　 # 声明一个存储2个字符的数组 array1，并赋值 'a', 'b'
array2:		.space	40	# allocate 40 consecutive bytes, with storage uninitialized
				#   could be used as a 40-element character array, or a
				#   10-element integer array; a comment should indicate which!	
　　　　　　　　　　　　　　　　　　 # 为变量 array2 分配 40字节（bytes)未使用的连续空间，当然，对于这个变量
　　　　　　　　　　　　　　　　　　 # 到底要存放什么类型的值， 最好事先声明注释下！
```

### 代码
代码段以 .text为开始标志
其实就是各项指令操作
程序入口为main：标志（这个都一样啦）
程序结束标志（详见下文）

### 注释
同C系语言

## 程序
MIPS程序的基本模板如下：
```
#Comment giving name of program and description of function
#说明下程序的目的和作用（其实和高级语言都差不多了）
#Template.s
#Bare-bones outline of MIPS assembly language program


           .data       # variable declarations follow this line
　　　　                # 数据变量声明
			name:	                storage_type	value(s)	
			变量名：（冒号别少了）     	数据类型          变量值   
                       # ...
														
           .text       # instructions follow this line	
		       # 代码段部分															
main:                  # indicates start of code (first instruction to execute)
                       # 主程序
                       # ...

加载/保存(也许这里写成读取/写入 可能更易理解一点) 指令集
如果要访问内存，不好意思，你只能用 load 或者 store 指令
其他的只能都一律是寄存器操作
									
# End of program, leave a blank line afterwards to make SPIM happy
# 必须多给你一行，你才欢？
```

### 加载/保存(读取/写入) 指令集
**访问内存只能用load或store**

lw	register_destination, RAM_source：从内存中复制 RAM_source 的内容到 对应的寄存器中

lb	register_destination, RAM_source：lb 意为 load byte

sw	register_source, RAM_destination：将指定寄存器中的数据 写入 到指定的内存中

sb	register_source, RAM_destination：sb 意为 store byte

li	register_destination, value：li 意为 load immediate

```
example:
	.data
var1:	.word	23		# declare storage for var1; initial value is 23
　　　　　　　　　　　　　　　　　　 # 先声明一个 word 型的变量 var1 = 3;
	.text
__start:
	lw	$t0, var1	# load contents of RAM location into register $t0:  $t0 = var1
　　　　　　　　　　　　　　　　　　 # 令寄存器 $t0 = var1 = 3;
	li	$t1, 5		# $t1 = 5   ("load immediate")
　　　　　　　　　　　　　　　　　　 # 令寄存器 $t1 = 5;
	sw	$t1, var1	# store contents of register $t1 into RAM:  var1 = $t1
　　　　　　　　　　　　　　　　　　 # 将var1的值修改为$t1中的值： var1 = $t1 = 5;
	done
```

### 立即与间接寻址
直接给地址

	la	$t0, var1

地址是寄存器的内容（可以理解为指针）

	lw	$t2, ($t0)
load word at RAM address contained in $t0 into $t2

	sw	$t2, ($t0)
store word in register $t2 into RAM at address contained in $t0

+偏移量

	lw	$t2, 4($t0)
load word at RAM address ($t0+4) into register $t2

"4" gives offset from address in register $t0

	sw	$t2, -12($t0)
store word in register $t2 into RAM at address ($t0 - 12)
negative offsets are fine

```
example：
栗子：

		.data
array1:		.space	12		#  declare 12 bytes of storage to hold array of 3 integers
　　　　　　　　　　　　　　　　　　　　　　　 #  定义一个 12字节 长度的数组 array1, 容纳 3个整型
		.text
__start:	la	$t0, array1	#  load base address of array into register $t0
　　　　　　　　　　　　　　　　　　　　　　　 #  让 $t0 = 数组首地址
		li	$t1, 5		#  $t1 = 5   ("load immediate")
		sw $t1, ($t0)		#  first array element set to 5; indirect addressing
　　　　　　　　　　　　　　　　　　　　　　　　# 对于 数组第一个元素赋值 array[0] = $1 = 5
		li $t1, 13		#   $t1 = 13
		sw $t1, 4($t0)		#  second array element set to 13
　　　　　　　　　　　　　　　　　　　　　　　　# 对于 数组第二个元素赋值 array[1] = $1 = 13 
　　　　　　　　　　　　　　　　　　　　　　　　# (该数组中每个元素地址相距长度就是自身数据类型长度，即4字节， 所以对于array+4就是array[1])
		li $t1, -7		#   $t1 = -7
		sw $t1, 8($t0)		#  third array element set to -7
　　　　　　　　　　　　　　　　　　　　　　　　# 同上， array+8 = （address[array[0])+4）+ 4 = address(array[1]) + 4 = address(array[2])
		done
```

### 算术指令集
最多3个操作数

再说一遍，在这里，操作数只能是寄存器，绝对不允许出现地址

所有指令统一是32位 = 4 * 8 bit = 4bytes = 1 word

  add $t0,$t1,$t2 # $t0 = $t1 + $t2; add as signed (2's complement) integers

		sub	    $t2,$t3,$t4	#  $t2 = $t3 Ð $t4
		addi	$t2,$t3, 5	#  $t2 = $t3 + 5;   "add immediate" (no sub immediate)
		addu	$t1,$t6,$t7	#  $t1 = $t6 + $t7;   add as unsigned integers
		subu	$t1,$t6,$t7	#  $t1 = $t6 + $t7;   subtract as unsigned integers

		mult	$t3,$t4		#  multiply 32-bit quantities in $t3 and $t4, and store 64-bit
					#  result in special registers Lo and Hi:  (Hi,Lo) = $t3 * $t4
　　　　　　　　　　　　　　　　　　　　　　　　　运算结果存储在hi,lo（hi高位数据， lo地位数据）
		div	$t5,$t6		#  Lo = $t5 / $t6   (integer quotient)
					#  Hi = $t5 mod $t6   (remainder)
　　　　　　　　　　　　　　　　　　　　　　　　　商数存放在 lo, 余数存放在 hi
		mfhi	$t0		#  move quantity in special register Hi to $t0:   $t0 = Hi
　　　　　　　　　　　　　　　　　　　　　　　　  不能直接获取 hi 或 lo中的值， 需要mfhi, mflo指令传值给寄存器
		mflo	$t1		#  move quantity in special register Lo to $t1:   $t1 = Lo
					#  used to get at result of product or quotient

		move	$t2,$t3	#  $t2 = $t3

### 控制流

#### 分支（if else系列）

		b	            target		#  unconditional branch to program label target
		beq 	        $t0,$t1,target	#  branch to target if  $t0 = $t1
		blt	            $t0,$t1,target	#  branch to target if  $t0 < $t1
		ble	            $t0,$t1,target	#  branch to target if  $t0 <= $t1
		bgt	            $t0,$t1,target	#  branch to target if  $t0 > $t1
		bge         	$t0,$t1,target	#  branch to target if  $t0 >= $t1
		bne	            $t0,$t1,target	#  branch to target if  $t0 <> $t1


#### 跳转（while, for, goto系列）

		j	target	　　　　 #  unconditional jump to program label target
　　　　　　　　　　　　　　　　　　　　　　　    
看到就跳， 不用考虑任何条件

		jr	$t3		#  jump to address contained in $t3 ("jump register")
　　　　　　　　　　　　　　　　　　　　　　　　　
 类似相对寻址，跳到该寄存器给出的地址处

#### 子程序调用

subroutine call: "jump and link" instruction

	jal	sub_label	#  "jump and link"
copy program counter (return address) to register $ra (return address register)

将当前的程序计数器保存到 $ra 中

jump to program statement at sub_label
subroutine return: "jump register" instruction

	jr	$ra	#  "jump register"
jump to return address in $ra (stored by jal instruction)

通过上面保存在  $ra 中的计数器返回调用前

Note: return address stored in register $ra; if subroutine will call other subroutines, or is recursive, return address should be copied from $ra onto stack to preserve it, since jal always places return address in this register and hence will overwrite previous value