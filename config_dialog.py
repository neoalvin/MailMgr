# -*- coding: utf-8 -*-

"""
Module implementing config.
"""

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox

from Ui_config_dialog import Ui_Dialog

from mailre import getxml, setxml, getconfig, setconfig

class config(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(config, self).__init__(parent)
        self.setupUi(self)
        self.blackList.setColumnWidth(0, 270)
        self.whiteList.setColumnWidth(0, 270)
        self.addBtn1.clicked.connect(self.addblist)
        self.addBtn2.clicked.connect(self.addwlist)
        self.delBtn1.clicked.connect(self.delbmail)
        self.delBtn2.clicked.connect(self.delwmail)     
        self.saveBtn1.clicked.connect(self.saveblist)
        self.saveBtn2.clicked.connect(self.savewlist)
        self.showblist()
        self.showwlist()
        self.okBtn1.clicked.connect(self.saveconfig)
        self.okBtn2.clicked.connect(self.saveconfig)
        
    def saveconfig(self):
        """保存系统设置信息"""
        status1=["on", "off"]
        status2=["off", "on"]
        if self.checkBlack.isChecked() and not self.checkWhite.isChecked():
            setconfig(status1)
            QMessageBox.information(self, "提示", self.tr("黑名单设置生效！"))
        elif self.checkWhite.isChecked() and not self.checkBlack.isChecked():
            setconfig(status2)
            QMessageBox.information(self, "提示", self.tr("白名单设置生效！"))
        else:
            QMessageBox.information(self, "提示", self.tr("设置错误！"))
        
    def saveblist(self):
        """保存黑名单"""
        blist=[]
        rows=self.blackList.rowCount()
        for row in range(rows):
            content=self.blackList.item(row, 0).text()
            blist.append(content)
        setxml("./listxml/blacklist.xml",blist, "maillist", "mail")
        QMessageBox.information(self, "提示", self.tr("已保存至本地！"))
        
    def savewlist(self):
        """保存白名单"""
        wlist=[]
        rows=self.whiteList.rowCount()
        for row in range(rows):
            content=self.whiteList.item(row, 0).text()
            wlist.append(content)
        setxml("./listxml/whitelist.xml",wlist, "maillist", "mail")
        QMessageBox.information(self, "提示", self.tr("已保存至本地！"))
        
    def showblist(self):
        """导出黑名单""" 
        blist=getxml("./listxml/blacklist.xml", "mail")
        row=0
        for mail in blist:
            self.blackList.insertRow(row)
            newItem = QTableWidgetItem(mail)
            self.blackList.setItem(row, 0, newItem)
            row+=1
            
    def showwlist(self):
        """导出白名单""" 
        wlist=getxml("./listxml/whitelist.xml",  "mail")
        row=0
        for mail in wlist:
            self.whiteList.insertRow(row)
            newItem = QTableWidgetItem(mail)
            self.whiteList.setItem(row, 0, newItem)
            row+=1
            
    def addblist(self):
        """添加新邮箱到黑名单列表"""
        row = self.blackList.rowCount()
        self.blackList.insertRow(row)
        mail=self.mailno.text()+self.domain_1.currentText()
        newItem = QTableWidgetItem(mail)
        self.blackList.setItem(row, 0, newItem)
    
    def addwlist(self):
        """添加邮箱到白名单"""
        row = self.whiteList.rowCount()
        self.whiteList.insertRow(row)
        mail=self.mailok.text()+self.domain_2.currentText()
        newItem = QTableWidgetItem(mail)
        self.whiteList.setItem(row, 0, newItem)
        
    def delbmail(self):
        """删除黑名单中条目"""
        row=self.blackList.currentItem().row()
        self.blackList.removeRow(row)
    
    def delwmail(self):
        """删除黑名单中条目"""
        row=self.whiteList.currentItem().row()
        self.whiteList.removeRow(row)
if __name__ == '__main__':
 
    from PyQt5.QtWidgets import  QApplication
    import sys
    app = QApplication(sys.argv)
    window = config()
    window.show()
    sys.exit(app.exec_())
