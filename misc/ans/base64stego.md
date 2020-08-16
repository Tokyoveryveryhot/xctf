1、.7zip解压base64stego.zip文件，得到stego.txt文件，使用UE打开
2、使用base64在线解密得到一段隐写术的介绍，怀疑使用了隐写术
3、查看writeup得知base64隐写的原理可得出结论：(1)base64加密后结尾无“=”号的无隐写位。(2)base64加密后结尾有1个“=”号的有2位隐写位。(3)base64加密后结尾有2个“=”号的有4位隐写位。首先判断每行数据的可隐写位数，然后将可隐写的每行最后一个字符根据base64码表，对应到相应的值，接着转为二进制，根据可隐写位数截取相应的位数，然后拼接这些隐写位，最后从左到右每8位一组截取二进制，分别将其转为十进制并对应ASCII码表，打印出相应的字符即可得到flag。
4、编写python脚本实现：
#coding=utf-8
def get_base64_diff_value(s1, s2):
    base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    res = 0
    for i in xrange(len(s2)):
        if s1[i] != s2[i]:
            return abs(base64chars.index(s1[i]) - base64chars.index(s2[i]))
    return res

def solve_stego():
    with open('1.txt', 'rb') as f:
        file_lines = f.readlines()
        bin_str = ''
        for line in file_lines:
            steg_line = line.replace('\n', '')
            norm_line = line.replace('\n', '').decode('base64').encode('base64').replace('\n', '')
            diff = get_base64_diff_value(steg_line, norm_line)
            print diff
            pads_num = steg_line.count('=')
            if diff:
                bin_str += bin(diff)[2:].zfill(pads_num * 2)
            else:
                bin_str += '0' * pads_num * 2
            print goflag(bin_str)

def goflag(bin_str):
    res_str = ''
    for i in xrange(0, len(bin_str), 8):
        res_str += chr(int(bin_str[i:i + 8], 2))
    return res_str

if __name__ == '__main__':
    solve_stego()
    ```


    wp的第八条，第二条，第十条，第十二条都很不错