一个判断spring框架是否存在actuator信息泄露的小工具

使用方法：

1、fofa批量搜索spring框架的url

2、url导入到文本

3、python3 GetSpringEnv.py -h
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f READFILE, --ReadFile=READFILE
                        Get Url File
  -o OUTFILE, --OutFile=OUTFILE
                        OutPut Can Use Url File
  -t THREAD, --Thread=THREAD
                        Set thread(default 10)
  -p PROXY, --Proxy=PROXY
                        Set Proxy(default None),example http://127.0.0.1:1080
                        
                        
ps：代码中的英文注释，直接忽略。用来调侃强强
