一个判断spring框架是否存在actuator信息泄露的小工具

思路：通过将url 拼接 /env和/actuator/env 来判断，是否存在。

使用方法：

1、fofa批量搜索spring框架的url

2、url导入到文本

3、python3 GetSpringEnv.py -h

Options:

  --version             show program's version number and exit
  
  
  -h, --help            show this help message and exit
  
  
  -f READFILE, --ReadFile=READFILE
  
                        读取url文本，进行扫描判断
                        
  -o OUTFILE, --OutFile=OUTFILE
  
                        输出文本，将扫描结果写入文本。默认为当前脚本路径下的output.txt
                        
                        
  -t THREAD, --Thread=THREAD
  
                        设置扫描线程。默认为10线程
                        
                        
  -p PROXY, --Proxy=PROXY
  
                        设置代理。默认无代理。使用方法 -p http://127.0.0.1:1080
                        
                        
ps：代码中的英文注释，直接忽略。用来调侃强强
