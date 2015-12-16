# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QTableWidgetItem
import sys
from Ui_mainWin import Ui_MainWindow
from config_dialog import config
import smtplib, mimetypes 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage
import poplib
import io
import email
import base64
from mailre import inblacklist,  inwhitelist, isblackre

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.popList.setColumnWidth(0, 200)
        self.popList.setColumnWidth(1, 200)
        self.popList.setColumnWidth(2, 190)
        self.pushBtn.clicked.connect(self.smtpmail)
        self.testBtn.clicked.connect(self.smtptest)
        self.addBtn.clicked.connect(self.getFile)
        self.popTest.clicked.connect(self.poptest)
        self.pullBtn.clicked.connect(self.popmail)
        self.popList.clicked.connect(self.getcontent)
        self.extraBtn.clicked.connect(self.openextra)
        self.addmenu()
        self.content_list=[]
        
    def addmenu(self):
        """添加菜单项到窗口"""
        #文件菜单
        self.configobj=config()
        myAction = QAction('保存文件', self)
        myAction.setShortcut('Ctrl+S')
        myAction.triggered.connect(self.configobj.show)
        self.file_menu.addAction(myAction)
        myAction = QAction('另存为...', self)
        myAction.setShortcut('Ctrl+Shift+S')
        myAction.triggered.connect(self.configobj.show)
        self.file_menu.addAction(myAction)
        #设置菜单
        self.configobj=config()
        myAction = QAction('收信规则', self)
        myAction.setShortcut('Ctrl+T')
        myAction.triggered.connect(self.configobj.show)
        self.config.addAction(myAction)
        #退出菜单
        myAction = QAction('退出系统', self)
        myAction.setShortcut('Esc')
        myAction.triggered.connect(self.close)
        self.quit_menu.addAction(myAction)
        
            
    def smtptest(self):
        """填充smtp测试数据"""
        self.statusList.clear()
        self.filePath.setText("")
        self.smtpServer.setCurrentText("smtp.163.com")
        self.fromMail.setText("v_alvin")
        self.domain_1.setCurrentText("@163.com")
        self.sendPwd.setText("healer1227")
        self.toMail.setText("neoalvin@qq.com;nishealer@qq.com")
        #self.domain_2.setCurrentText("@qq.com")
        self.sender.setText("healer")
        self.receiver.setText("alvin")
        self.mailSub.setText("Introduction")
        self.mailContent.setText("just a test mail.")
        
    def poptest(self):
        """填充pop测试数据"""
        #清空邮件列表
        self.popList.setRowCount(0)
        self.popList.clearContents()
        #清空内容框
        self.popContent.setText("")
        #清空状态框
        self.popStatus.clear()
        self.popServer.setCurrentText("pop3.163.com")
        self.popMail.setText("neoalvin")
        self.domain_3.setCurrentText("@163.com")
        self.receivePwd.setText("bzgtxtodyghwsbdg")
        
    def smtpmail(self):
        """用smtp发送邮件"""
        host=self.smtpServer.currentText()
        mailto=self.toMail.text()+self.domain_2.currentText()
        mailto_list=[]
        self.statusList.clear()
        self.mailContent.setText("")
        self.statusList.clear()
        if mailto.find(';'):
            mailto_list=mailto.split(';')
        else:
            mailto_list.append(mailto)
        for mailfor in mailto_list:
            try:
                self.statusList.addItem("===发送给"+mailfor+"的邮件===")
                self.sendmail(host, mailfor)
            except Exception as e:
                self.statusList.addItem(str(e))
                
    def sendmail(self, host, mailto):
        """使用smtp发送单封邮件（带附件）"""
        mailfrom=self.fromMail.text()+self.domain_1.currentText()
        password=self.sendPwd.text()
        #sender=self.sender.text()
        #receiver=self.receiver.text()
        mailsub=self.mailSub.text()
        mailcontent=self.mailContent.toPlainText()
        filename=self.filePath.text()
        msg = MIMEMultipart() 
        msg['From'] = mailfrom
        msg['To'] = mailto
        msg['Subject'] = mailsub
        #邮件中的文本内容
        txt = MIMEText(mailcontent) 
        msg.attach(txt)
        if self.filePath.text()!='':
            ctype, encoding = mimetypes.guess_type(filename) 
            if ctype is None or encoding is not None: 
             ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1) 
            att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(filename, 'rb'))[0], _subtype = subtype) 
            att1.add_header('Content-Disposition', 'attachment', filename = filename) 
            msg.attach(att1) 
        #发送邮件 
        smtp = smtplib.SMTP() 
        smtp.connect(host, 25)
        self.statusList.addItem(str(smtp.docmd('helo', 'user'))) 
        #self.statusList.addItem(str(smtp.login(mailfrom,password)))
        self.statusList.addItem(str(smtp.sendmail(mailfrom, mailto, msg.as_string()))) 
        self.statusList.addItem(str(smtp.quit()))
        self.statusList.addItem("发送成功！")
        
        #测试窗口数据是否正确读取
        """
        self.statusList.addItem(host)
        self.statusList.addItem(mailfrom)
        self.statusList.addItem(password)
        self.statusList.addItem(mailto)
        self.statusList.addItem(mailsub)
        self.statusList.addItem(mailcontent)
        """
        #只发送纯文本邮件
        """
        try:
            smtp = smtplib.SMTP() 
            smtp.connect(host,25) 
            self.statusList.clear()
            self.statusList.addItem(str(smtp.docmd('helo', 'user'))) 
            #self.statusList.addItem(str(smtp.starttls()))
            self.statusList.addItem(str(smtp.login(mailfrom,password)))
            self.statusList.addItem(str(smtp.docmd('mail from:', '<%s>'%mailfrom)) )
            self.statusList.addItem(str(smtp.docmd('rcpt to:', '<%s>'%mailto)) )
            #data 指令表示邮件内容 
            self.statusList.addItem(str(smtp.docmd('data')))
            self.statusList.addItem(str(smtp.docmd('from:%s\nto:%s\nsubject:%s\r\n%s\r\n.\r\n'%(mailfrom,mailto,mailsub,mailcontent))))
            self.statusList.addItem(str(smtp.quit()))
        except Exception as e:
            QMessageBox.information(self,"Warning",self.tr(str(e)))"""
        
    def getFile(self):
        """获取附件路径"""
        fileName, type= QFileDialog.getOpenFileName(self,  "选取文件",  "", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔  
        self.filePath.setText(fileName)
        
    def openextra(self):
        """查看附件"""
        fileName, type= QFileDialog.getOpenFileName(self,  "查看附件",  "extrafile/", "All Files (*);;Text Files (*.txt)")  
        
    def popmail(self):
        """接收邮件"""
        popserver=self.popServer.currentText()
        user=self.popMail.text()+self.domain_3.currentText()
        pwd=self.receivePwd.text()
        #self.popStatus.addItem(user)
        M=poplib.POP3(popserver)
        M.user(user)
        M.pass_(pwd)
        #number of emails
        numMessages=len(M.list()[1])
        self.popStatus.addItem('邮件数量：'+str(numMessages))
        #清空邮件列表
        self.popList.setRowCount(0)
        self.popList.clearContents()
        #清空内容框
        self.popContent.setText("")
        #清空状态框
        self.popStatus.clear()
        row=-1
        for i in range(numMessages):
            self.popStatus.addItem('===第'+str(i+1)+'封邮件信息===')
            m = M.retr(i+1)
            buf = io.StringIO()
            for j in m[1]:
                print(j.decode("ascii"),file=buf)
            buf.seek(0)
            #原邮件信息
            msg = email.message_from_file(buf)
            #print(msg)
            #读取邮件头信息
            mailfrom=msg.get("From")
            isblack=isblackre()
            inblack=inblacklist(mailfrom)
            inwhite=inwhitelist(mailfrom)
            if isblack==1:
                self.popStatus.addItem("您启动了黑名单设置！")
                if inblack==0:
                    row+=1
                    mailsub=msg.get("Subject")
                    date=msg.get("Date")
                    #将邮件信息添加到列表
                    self.popList.insertRow(row)
                    item1 = QTableWidgetItem(date)
                    self.popList.setItem(row, 0, item1)
                    item2 = QTableWidgetItem(mailfrom)
                    self.popList.setItem(row, 1, item2)
                    item3 = QTableWidgetItem(mailsub)
                    self.popList.setItem(row, 2, item3)
                    self.popStatus.addItem("发件人："+str(mailfrom))
                    self.popStatus.addItem("主题："+str(mailsub))
                    self.popStatus.addItem("时间:"+str(date))
                    for part in msg.walk():
                        #获取邮件内容各部分的类型及文件名
                        contenttype = part.get_content_type()
                        filename = part.get_filename()
                        self.popStatus.addItem("文件类型："+str(contenttype))
                        self.popStatus.addItem("文件名："+str(filename))
                        #获取文本encode
                        encode=part.get("Content-Transfer-Encoding")
                        self.popStatus.addItem("文件编码："+str(encode))
                        #测试获取文本信息
                        if contenttype=="text/plain":
                            mailcontent=part.get_payload()
                            if encode=="base64":
                                mailcontent=base64.decodestring(bytes(mailcontent, "utf-8"))
                            if type(mailcontent)==type(b'a'):
                                mailcontent=mailcontent.decode("utf-8")
                            self.content_list.append(mailcontent)
                        #获取附件
                        if filename:
                            try:
                                f = open("./extrafile/%s" % filename,'wb+')
                                f.write(base64.decodestring(bytes(part.get_payload(), 'utf-8')))
                                f.close()
                                self.popStatus.addItem("附件保存成功！")
                            except:
                                self.popStatus.addItem("附件保存失败！")
                else:
                    self.popStatus.addItem("该发信人在您的黑名单中，请及时处理！")
            elif isblack==0:
                self.popStatus.addItem("您启动了白名单设置！")
                if inwhite==1:
                    row+=1
                    print(row)
                    mailsub=msg.get("Subject")
                    date=msg.get("Date")
                    #将邮件信息添加到列表
                    self.popList.insertRow(row)
                    item1 = QTableWidgetItem(date)
                    self.popList.setItem(row, 0, item1)
                    item2 = QTableWidgetItem(mailfrom)
                    self.popList.setItem(row, 1, item2)
                    item3 = QTableWidgetItem(mailsub)
                    self.popList.setItem(row, 2, item3)
                    self.popStatus.addItem("发件人："+str(mailfrom))
                    self.popStatus.addItem("主题："+str(mailsub))
                    self.popStatus.addItem("时间:"+str(date))
                    for part in msg.walk():
                        #获取邮件内容各部分的类型及文件名
                        contenttype = part.get_content_type()
                        filename = part.get_filename()
                        self.popStatus.addItem("文件类型："+str(contenttype))
                        self.popStatus.addItem("文件名："+str(filename))
                        #获取文本encode
                        encode=part.get("Content-Transfer-Encoding")
                        self.popStatus.addItem("文件编码："+str(encode))
                        #测试获取文本信息
                        if contenttype=="text/plain":
                            mailcontent=part.get_payload()
                            if encode=="base64":
                                mailcontent=base64.decodestring(bytes(mailcontent, "utf-8"))
                            if type(mailcontent)==type(b'a'):
                                mailcontent=mailcontent.decode("utf-8")
                            self.content_list.append(mailcontent)
                        #获取附件
                        if filename:
                            try:
                                f = open("./extrafile/%s" % filename,'wb+')
                                f.write(base64.decodestring(bytes(part.get_payload(), 'utf-8')))
                                f.close()
                                self.popStatus.addItem("附件保存成功！")
                            except:
                                self.popStatus.addItem("附件保存失败！")
                else:
                    self.popStatus.addItem("该发信人不在在您的白名单中，请及时处理！")
            else:
                    row+=1
                    mailsub=msg.get("Subject")
                    date=msg.get("Date")
                    #将邮件信息添加到列表
                    self.popList.insertRow(row)
                    item1 = QTableWidgetItem(date)
                    self.popList.setItem(row, 0, item1)
                    item2 = QTableWidgetItem(mailfrom)
                    self.popList.setItem(row, 1, item2)
                    item3 = QTableWidgetItem(mailsub)
                    self.popList.setItem(row, 2, item3)
                    self.popStatus.addItem("发件人："+str(mailfrom))
                    self.popStatus.addItem("主题："+str(mailsub))
                    self.popStatus.addItem("时间:"+str(date))
                    for part in msg.walk():
                        #获取邮件内容各部分的类型及文件名
                        contenttype = part.get_content_type()
                        filename = part.get_filename()
                        self.popStatus.addItem("文件类型："+str(contenttype))
                        self.popStatus.addItem("文件名："+str(filename))
                        #获取文本encode
                        encode=part.get("Content-Transfer-Encoding")
                        self.popStatus.addItem("文件编码："+str(encode))
                        #测试获取文本信息
                        if contenttype=="text/plain":
                            mailcontent=part.get_payload()
                            if encode=="base64":
                                mailcontent=base64.decodestring(bytes(mailcontent, "utf-8"))
                            if type(mailcontent)==type(b'a'):
                                mailcontent=mailcontent.decode("utf-8")
                            self.content_list.append(mailcontent)
                        #获取附件
                        if filename:
                            try:
                                f = open("./extrafile/%s" % filename,'wb+')
                                f.write(base64.decodestring(bytes(part.get_payload(), 'utf-8')))
                                f.close()
                                self.popStatus.addItem("附件保存成功！")
                            except:
                                self.popStatus.addItem("附件保存失败！")
    def getcontent(self):
        """查看邮件内容"""
        row=self.popList.currentItem().row()
        self.popContent.setText(self.content_list[row])
if __name__ == '__main__':
 
    from PyQt5.QtWidgets import  QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    
