#encoding=utf-8
import  xml.dom.minidom
import re

def getxml(filepath, item):
    """读取xml文件返回邮箱"""
    mail_list=[]
    #打开xml文档
    dom = xml.dom.minidom.parse(filepath)
    #得到文档元素对象
    root = dom.documentElement
    mails = root.getElementsByTagName(item)
    for mail in mails:
        mail_list.append(mail.firstChild.data)
    return mail_list
    
def setxml(filepath, mailbox_list, header,item):
    """将邮箱写入xml文件"""
    doc = xml.dom.minidom.Document()
    maillist = doc.createElement(header)
    doc.appendChild(maillist)
    for mailbox in mailbox_list:
        mail = doc.createElement(item)
        maillist.appendChild(mail)
        content = doc.createTextNode(mailbox)
        mail.appendChild(content)
    f =  open(filepath,  'w+')
    f.write(re.sub(r'(<[^/][^<>]*[^/]>)\s*([^<>]{,40}?)\s*(</[^<>]*>)', r'\1\2\3', doc.toprettyxml()))
    f.close()

def setconfig(status_list):
    """将设置信息写入xml"""
    doc = xml.dom.minidom.Document()
    header = doc.createElement("config")
    doc.appendChild(header)
    black = doc.createElement("useBlacklist")
    header.appendChild(black)
    content = doc.createTextNode(status_list[0])
    black.appendChild(content)
    white= doc.createElement("useWhitelist")
    header.appendChild(white)
    content = doc.createTextNode(status_list[1])
    white.appendChild(content)
    f =  open('config.xml',  'w+')
    f.write(re.sub(r'(<[^/][^<>]*[^/]>)\s*([^<>]{,40}?)\s*(</[^<>]*>)', r'\1\2\3', doc.toprettyxml()))
    f.close()
    
def getconfig():
    """读取系统设置信息"""
    """读取xml文件返回邮箱"""
    status_list=[]
    #打开xml文档
    dom = xml.dom.minidom.parse("config.xml")
    #得到文档元素对象
    root = dom.documentElement
    blacks = root.getElementsByTagName("useBlacklist")
    for black in blacks:
        status_list.append(black.firstChild.data)
    whites = root.getElementsByTagName("useWhitelist")
    for white in whites:
        status_list.append(white.firstChild.data)
    return status_list
    
def inblacklist(mailfrom):
    """判断是否在黑名单中"""
    flag=0
    blacklist=getxml("./listxml/blacklist.xml", "mail")
    for mail in blacklist:
        if mailfrom.find(mail)>0:
            flag=1
    return flag
    
def inwhitelist(mailfrom):
    """判断是否在白名单中"""
    flag=0
    blacklist=getxml("./listxml/whitelist.xml", "mail")
    for mail in blacklist:
        if mailfrom.find(mail)>0:
            flag=1
    return flag
    
def isblackre():
    """判断收信规则"""
    relist=getconfig()
    if relist[0]=="on":
        return 1
    else:
        return 0
