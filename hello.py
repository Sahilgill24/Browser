import os
import sys
import socket


class URL:
    def __init__(self,url):
        #make a constructor that will always parse our url 
        self.scheme,url=url.split("://",1) #iska mtlb hai kii url ko split krdena and max split 1 hii hona chahiye 
        assert self.scheme == "http" , "unknown scheme {}".format(self.scheme) # ab iska mtlb hai kii agr scheme hmari http nhi 
        # to print krdena unknown scheme and usme {} jo ye hein inme wo scheme apne aap input hojegi
        if "/" not in url:
            url=url + '/' 
        self.host,url=url.split('/',1)
        self.path = '/' + url

    def request(self):
        s=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM,proto=socket.IPPROTO_TCP)
        s.connect((self.host,80))
        s.send(("GET {} HTTP/1.0\r\n".format(self.path) + \
                "Host: {}\r\n\r\n".format(self.host)) \
               .encode("utf8"))
        response=s.makefile("r",encoding="utf-8",newline='\r\n')
        #instead of using the while loop , we here use make file function that returns a file type object conating every byte we recieved
        statusline =response.readline() # reads the first line 
        version ,status,explanation=statusline.split(" ",2)
        assert status =="200" ,"{} : {}".format(status,explanation)
        # we might want to chekc that what http verison we are getting as a response , but there are many misconfigured codes here
        headers = {}
        while True:
            line =response.readline()
            if line == '\r\n':
                break
            header,value =line.split(":",1)
            headers[header.lower()]=value.strip()
        assert "transfer-encoding" not in headers
        assert "content-encoding" not in headers
        body=response.read()
        s.close()
        return headers,body

def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")
            #agr wo angular brackets ke beech mei hai then do nothign but agr normal text then usko print krdo 

def load(url):
    headers,body=URL.request(url)
    show(body)

if __name__=="__main__":
    load(URL(sys.argv[1]))
   
    


            

        


            