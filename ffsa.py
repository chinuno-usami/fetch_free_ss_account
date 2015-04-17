# -*- coding: UTF-8 -*-   
import urllib2
from sgmllib import SGMLParser
import urllib  
import httplib
import HTMLParser
import json
import logging

def initLogging(logFileName):
    logging.basicConfig(
        level = logging.DEBUG,
        format = 'LINE %(lineno)-4d %(levelname)-8s %(message)s',
        datefmt = '%m-%d %H:%M',
        filename = logFileName,
        filemode = 'w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)-s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def get_res(url):
    req = urllib2.Request(url)
    html_parser = HTMLParser.HTMLParser()
    res_data = urllib2.urlopen(req)
    res = res_data.read().decode('utf-8')
    res = html_parser.unescape(res).encode('utf-8')
    return res

class fylst(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_pre = ""
        self.name = []
    def start_pre(self, attrs):
        self.is_pre = 1
    def end_pre(self):
        self.is_pre = ""
    def handle_data(self, text):
        if self.is_pre == 1:
            self.name.append(text)

class gfwlst(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_td = ""
        self.name = []
    def start_td(self, attrs):
        self.is_td = 1
    def end_td(self):
        self.is_td = ""
    def handle_data(self, text):
        if self.is_td == 1:
            self.name.append(text)


if __name__ == '__main__':
    initLogging("get_ss.log")
    
    result = ""
    url_fy = "http://www.fyhqy.com/356/"
    url_gfw = "http://52-gfw.tk/ss.html"

    print " [+] Getting data from fyhqy...",
        
    try:
        res_fy = get_res(url_fy)
    except Exception, e:
        raise e

    print "\t[done]"

    print " [+] Getting data from 52-gfw...",
        
    # try:
    #     res_gfw = get_res(url_gfw)
    # except Exception, e:
    #     raise e
    res_gfw = get_res(url_gfw)
    print "\t[done]"

    #处理fyhqy的数据
    lst_fy = fylst()
    lst_fy.feed(res_fy)
    for js in lst_fy.name:
        result += js
    result = result.replace("美国节点地址1",'').replace("\r",'\n').lower()
    logging.debug('result:'+result)
    # 目前无法获取节点2
    # rst_list = result.split("节点地址2")

    jsdt_fix = result.replace('\"time',',\"time')#弃用rst_list[0]
    logging.debug('jsdt_fix:'+jsdt_fix)
    jsdt1 = json.loads(jsdt_fix)
    logging.debug('jsdt1:'+str(jsdt1))
    jsport1 = jsdt1[u'server_port']
    logging.debug('port:'+str(jsport1))
    jspw1 = jsdt1[u'password']
    logging.debug('passwd:'+jspw1)
    jssvr1 = jsdt1[u'server']
    logging.debug('server:'+jssvr1)
    jsmtd1 = jsdt1[u'method']
    logging.debug('methon:'+jsmtd1)

# 节点2
    # jsdt2 = json.loads(rst_list[1])
    # print jsdt2
    # jsport2 = jsdt2[u'server_port']
    # print "port:",jsport2
    # jspw2 = jsdt2[u'password']
    # print 'passwd:',jspw2
    # jssvr2 = jsdt2[u'server']
    # print "server:",jssvr2
    # jsmtd2 = jsdt2[u'method']
    # print 'methon:',jsmtd2


    #处理52-gfw的数据
    lst_gfw = gfwlst()
    lst_gfw.feed(res_gfw)
    list_gfw_write = []
    for dat in lst_gfw.name:
        list_gfw_write.append(dat)
        logging.debug('gfw list data:'+dat)

    print " [+] Getting config.json ...",
    fin = open('config.json','r')
    fin_text = fin.read()
    fin.close()
    print "\t[done]"
    logging.debug('fin_text:'+fin_text)

    jsin = json.loads(fin_text)

    #fhyqy节点1
    jsin[u'server_password'][0][0] = jssvr1 + ':' + str(jsport1)
    jsin[u'server_password'][0][1] = jspw1
    jsin[u'server_password'][0][2] = jsmtd1

# 节点2暂时不可用
#     jsin[u'server_password'][1][0] = jssvr2 + ':' + str(jsport2)
#     jsin[u'server_password'][1][1] = jspw2
#     jsin[u'server_password'][1][2] = jsmtd2

    #52-gfw设置
    print " [+] Setting 52-gwf config..."
    for x in xrange(4):
        jsin[u'server_password'][2+x][0] = list_gfw_write[4+x*4] + ':' + list_gfw_write[5+x*4]
        jsin[u'server_password'][2+x][1] = list_gfw_write[6+x*4]
        jsin[u'server_password'][2+x][2] = list_gfw_write[7+x*4]
        print '     -',x+1,"done"

    jswt = json.dumps(jsin)
    print " [+] Writting config.json...",
    fout = open('config.json','w')
    fout.write(jswt)
    fout.close()
    print "\t[done]"
