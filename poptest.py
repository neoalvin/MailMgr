#coding:utf-8
import poplib
import io
import email
import base64
#pop3 get email
M=poplib.POP3('pop3.163.com')
M.user('neoalvin@163.com')
M.pass_('bzgtxtodyghwsbdg')
#number of emails
numMessages=len(M.list()[1])
print('num of messages',numMessages)
for i in range(numMessages):
    m = M.retr(i+1)
    buf = io.StringIO()
    for j in m[1]:
        print(j.decode("ascii"), file=buf)
    buf.seek(0)
    #print(buf)
    msg = email.message_from_file(buf)
    print(msg)
    i=0
    for part in msg.walk():
        i+=1
        if i==1:
            #获取的邮件信息
            mailfrom=part.get("From")
            mailto=part.get("To")
            mailsub=part.get("Subject")
            print(mailfrom, mailto, mailsub)
        #获取邮件内容各部分的类型及文件名
        contenttype = part.get_content_type()
        filename = part.get_filename()
        print(contenttype, filename)
        #获取文本encode
        encode=part.get("Content-Transfer-Encoding")
        print(encode)
        #测试获取文本信息
        if contenttype=="text/plain":
            mailcontent=part.get_payload()
            if encode=="base64":
                mailcontent=base64.decodestring(bytes(mailcontent, 'utf-8'))
            print(mailcontent)
        #获取附件
        if filename:
            try:
                f = open("./mail/%s" % filename,'wb+')
                f.write(base64.decodestring(bytes(part.get_payload(), 'utf-8')))
                f.close()
                print("附件保存成功！")
            except:
                print("附件保存失败！")
input()
