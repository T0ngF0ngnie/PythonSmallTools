import requests
import os
import re
import threading
import queue as Queue
import logging
from optparse import OptionParser

def UrlDealProtocol(Xurl,Xnum):  #If there is no http or https, add http or https
    if re.match('^(http|https)',Xurl):
        return 1
    else:
        Hsurl  = 'https://'+Xurl
        FileList[Xnum] = 'http://'+Xurl
        FileList.append(Hsurl)
        return 0

def UrlDealPath(Xurl):           #Add path /actuator/env && /env Determine whether there is improper configuration(lol)
    PathEnv = Xurl + '/env'
    PathActuator = Xurl + '/actuator/env'
    UrlPath.append(PathEnv)
    UrlPath.append(PathActuator)

def ReadUrlFile(FileName):      #Read all urls from url file
    print("[*]Loading File {}".format(FileName))
    FileText = open(FileName,'r')
    FileList = [x.strip() for x in FileText.readlines()]
    FileText.close()
    return FileList

def WriteFile(FileName,Xurl):                #Write the result url to the file
    FileX = open(FileName,'a')
    FileX.write(Xurl+"\n")
    FileX.close()

def CheckProxy(Xproxy):             #Determine whether the proxy server can be used
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0)','X-Forwarded-For': '127.0.0.1'}
    url = "https://myip.ipip.net"
    flag = 1

    if Xproxy == None:
        try:
            rep = requests.get(url,headers=headers,verify=False,timeout=3)
            print("[*]{}".format(rep.text.strip()))
        except:
            print("",end="")
        finally:
            return flag
    else:
        try:
            proxies = {"https": Xproxy,"http": Xproxy,}
            rep = requests.get(url,headers=headers,verify=False,timeout=3,proxies=proxies)
            print("[*]Use Current Proxy:{}".format(Xproxy))
            print("[*]{}".format(rep.text.strip()))
        except:
            flag = 0
        finally:
            return flag


class Threads(threading.Thread):            #Custom thread class,Multi-threaded access url
    def __init__(self,url,queue,headers,Xproxy,OutFilePath):
        threading.Thread.__init__(self)
        self.url = url
        self.queue  = queue
        self.headers = headers
        self.Xproxy = Xproxy
        self.OutFilePath = OutFilePath
    
    def run(self):
        try:
            if self.Xproxy == None:
                rep = requests.get(self.url,headers=self.headers,verify=False,timeout=3)
            else:
                proxies = {"https": self.Xproxy,"http":self.Xproxy}
                rep = requests.get(self.url,headers=self.headers,verify=False,timeout=3,proxies=proxies)
            UrlCode = rep.status_code
            if UrlCode == 200:
                CanUseUrl.append(self.url)
                print('[+]{} can be access'.format(self.url))
                WriteFile(self.OutFilePath,self.url)
        except:
            print("",end="")
        finally:
            self.queue.get()
            self.queue.task_done()

def GetInfo(Xthread,Xproxy,OutFilePath):              #Access, determine whether there is a path
    global flag
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0)','X-Forwarded-For': '127.0.0.1'}
    q = Queue.Queue(Xthread)
    for iurl,s in zip(UrlPath,range(99999)):
        flag = 0
        q.put(s)
        t = Threads(iurl,q,headers,Xproxy,OutFilePath)
        t.start()
    q.join()
    

if __name__ == "__main__":
    UrlPath = []                               #Store the processed url
    CanUseUrl = []                              #Store URLs with configuration problems, the final processing results
    FileList = []                               #Store the url read from the file
    logging.captureWarnings(True)               #Turn off the certificate failure alert
    parser = OptionParser(usage="%prog",version="%prog% v1.1",description="o md fuck,The first and also final version,qiangqiang niubi")
    parser.add_option('-f',"--ReadFile",dest="ReadFile",help="Get Url File")
    parser.add_option('-o',"--OutFile",dest="OutFile",help="OutPut Can Use Url File",type='string',default="output.txt")
    parser.add_option('-t',"--Thread",dest="Thread",help="Set thread(default 10)",type='int',default=10)
    parser.add_option('-p',"--Proxy",dest="Proxy",help="Set Proxy(default None),example http://127.0.0.1:1080",type='string',default=None)

    (options, args) = parser.parse_args()
    ReadFileName = options.ReadFile
    if ReadFileName == None:
        print("Use python3 springtitle.py -h Get Help!!!")
        exit(0)
    OutFileName = options.OutFile
    SetThread = options.Thread
    GoProxy = options.Proxy
    OutFilePath  = os.getcwd()+'\\'+OutFileName
    ReadFilePath = os.getcwd()+'\\'+ReadFileName


    if CheckProxy(GoProxy) == 0 :
        print("There is a problem with the proxy server,Check your proxy server,Current proxy server:{}".format(GoProxy))
        exit(0)

    print("[*]FileName:{},\tFilePath:{},\tStart scanning".format(ReadFileName,ReadFilePath))

    if(os.path.exists(ReadFilePath)):
        FileList = ReadUrlFile(ReadFilePath)                          # read file get url
        for Xurl,Xnum in zip(FileList,range(0,9999999)):    #deal Protocol
            UrlDealProtocol(Xurl,Xnum)

        for Xurl in FileList:                               #add url Path
            UrlDealPath(Xurl)

        GetInfo(SetThread,GoProxy,OutFilePath)

        if CanUseUrl != None:
            #WriteFile(OutFilePath)
            print("[*]Scan Complete,{} url can use,OutFile:{}".format(len(CanUseUrl),OutFilePath))
        else:
            print("[*]Scan Complete 0 url can use")

    else:
        print("[-]error File {} not exists!!!".format(ReadFilePath))
        exit()
