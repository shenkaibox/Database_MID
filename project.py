import yfinance as yf
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
from datetime import datetime
import wx

conn = sqlite3.connect('project.db')
print("Database Connected")


class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        font = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        # all static text
        StockText = wx.StaticText(self, -1, "Here are my stocks : ", pos=(20,10))
        StockText.SetFont(font)
        
        # button
        self.showButton = wx.Button(self, wx.ID_ANY, 'Display', pos=(200, 10))
        self.showButton.Bind(wx.EVT_BUTTON, self.OnButton)
        self.financeButton = wx.Button(self, wx.ID_ANY, 'Finance State', pos=(300, 10))
        self.financeButton.Bind(wx.EVT_BUTTON, self.OnButton2)
        self.growthButton = wx.Button(self, wx.ID_ANY, 'Growth', pos=(400, 10))
        self.growthButton.Bind(wx.EVT_BUTTON, self.OnButton3)
        self.updateButton = wx.Button(self, wx.ID_ANY, 'Update', pos=(500,10))
        self.updateButton.Bind(wx.EVT_BUTTON, self.OnButton4)
        
    #顯示目前所擁有的股票資訊    
    def OnButton(self, event):
        print("Button Clicked")
        cur = conn.cursor()
        cur.execute("SELECT * from OwnStock")
        CategoryText = wx.StaticText(self, -1, "[Name, Num(shares), Current Price, Beginning Value, Current Value]", pos=(20,60))
        rows = cur.fetchall()
        blank = 0
        for i in range(len(rows)):
            temp = ""
            for element in range(len(rows[i])):
                # print(element + " ", end='')
                temp+=rows[i][element] + "        "
                showStock = wx.StaticText(self, -1, temp, pos = (20, 100+blank*50))
            blank+=1

    #目前所有擁有的股票狀態圓餅圖
    def OnButton2(self, event):
        cur = conn.cursor()
        cur = conn.execute("SELECT * from OwnStock")
        rows = cur.fetchall()
        list_stock = []
        list_CurrentP = []
        # print(len(rows))
        # print(rows[1][1])
        for row in range(len(rows)):
            list_stock.append(rows[row][0])
            list_CurrentP.append(float(rows[row][4]))  
        # print(list_stock)
        # print(list_CurrentP)
        plt.pie(list_CurrentP, labels=list_stock, autopct='%.1f%%',radius=1)
        plt.title("All Finance State", {"fontsize" : 18})
        plt.show()
        
    #目前所擁有的股票成長率長條圖
    def OnButton3(self, event):
        cur = conn.cursor()
        cur = conn.execute("SELECT * from OwnStock")
        rows = cur.fetchall()
        list_stock = []
        list_value = []
        for row in range(len(rows)):
            list_value.append(((float(rows[row][4])-float(rows[row][3]))/float(rows[row][3]))*100)
            list_stock.append(rows[row][1])

        plt.bar(np.arange(len(list_stock)), list_value)
        plt.xticks(np.arange(len(list_stock)),list_stock)
        plt.xlabel('Stock Name')
        plt.ylabel('Current growth in percentage')
        plt.title('growth of all stocks')
        for x,y in enumerate(list_value):
            plt.text(x,y,'%s'%round(y,1)+'%', ha='center')
        plt.show()
    
    #更新最新的股價(CurrentP)    
    def OnButton4(self, event):
        cur = conn.cursor()
        cur = conn.execute("SELECT * from OwnStock")
        rows = cur.fetchall()
        for row in range(len(rows)):
            currentv = 0
            stockid = str(rows[row][0]) + '.tw'
            stock = yf.Ticker(stockid)
            data = stock.history()
            data = data.reset_index()
            closeP = data['Close']
            # print(closeP.iloc[-1]) //latest price
            curu = conn.execute("Update OwnStock set CurrentP=? where Name=?", (closeP.iloc[-1], str(rows[row][0])))
            currentv = float(rows[row][2]) * float(rows[row][1])
            curu = conn.execute("Update OwnStock set CurrentV=? where Name=?", (currentv, str(rows[row][0])))
            print("finish")
            conn.commit()
    
class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # static text
        font = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        searchText = wx.StaticText(self, -1, "股票代碼", pos=(20,10))
        searchText.SetFont(font)
        CategoryText = wx.StaticText(self, -1, "[Name, Date, Num(shares), Current Price, Beginning Value]", pos=(20,60))
        
        # textCtrl
        self.codeText = wx.TextCtrl(self, pos=(125,10))
        # self.codeText.Bind(wx.EVT_TEXT, self.OnKeyTyped)
        
        
        # Button
        self.showButton = wx.Button(self, wx.ID_ANY, 'Show', pos=(250, 10))
        self.showButton.Bind(wx.EVT_BUTTON, self.OnButton)
        self.clearButton = wx.Button(self, wx.ID_ANY, 'Clear', pos=(400, 10))
        self.clearButton.Bind(wx.EVT_BUTTON, self.OnButton2)
    
    #歷史購買資訊顯示    
    def OnButton(self, event):
        print("Button clicked")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Record WHERE NAME='{n}'".format(n=self.codeText.GetValue()))
        # cur.execute("select * from Record")
        CategoryText = wx.StaticText(self, -1, "[Name, Date, Num(shares), Current Price, Beginning Value]", pos=(20,60))
        rows = cur.fetchall()
        blank = 0
        for i in range(len(rows)):
            temp = ""
            for element in range(len(rows[i])):
                # print(element + " ", end='')
                temp+=rows[i][element] + "        "
                # showStock = wx.StaticText(self, -1, "                                                                                         "
                #                      , pos= (20, 100 + blank * 50))
                showStock = wx.StaticText(self, -1, temp, pos = (20, 100+blank*50))
            blank+=1
        cur.close()
    
    def OnButton2(self, event):
        cur = conn.cursor()
        cur.execute("SELECT * FROM Record WHERE NAME='{n}'".format(n=self.codeText.GetValue()))
        rows = cur.fetchall()
        for i in range(len(rows)):
            data = wx.StaticText(self, -1, "                                                                                                            "
                                , pos= (20, 100 + i * 50))
        
class TabThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # static Text
        font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.LIGHT)
        searchText = wx.StaticText(self, -1, "查詢的股票", pos=(20,10))
        searchText.SetFont(font)
        timeText = wx.StaticText(self, -1, "Enter the Start Time : ", pos=(20,40))
        timeText.SetFont(wx.Font(15, wx.ROMAN, wx.NORMAL, wx.LIGHT))
        yearText = wx.StaticText(self, -1, "Enter the Year", pos=(20,70))
        yearText.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT))
        monthText = wx.StaticText(self, -1, "Enter the Month", pos=(20,100))
        monthText.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT))
        dateText = wx.StaticText(self, -1, "Enter the Date", pos=(20,130))
        dateText.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT))
        
        # four textCtrl
        self.stockText = wx.TextCtrl(self, pos=(200,10))
        self.yText = wx.TextCtrl(self, pos=(200,70))
        self.mText = wx.TextCtrl(self, pos=(200,100))
        self.dText = wx.TextCtrl(self, pos=(200,130))
        
        # search button
        self.showButton = wx.Button(self, wx.ID_ANY, 'Search', pos=(400, 130))
        self.showButton.Bind(wx.EVT_BUTTON, self.OnButton)
    
    #最新股價查詢
    def OnButton(self, event):
        stockid = self.stockText.GetValue() + '.tw'
        data = yf.download('{n}'.format(n=stockid), start = '{y}-{m}-{d}'.format(y=self.yText.GetValue(), m=self.mText.GetValue(), d=self.dText.GetValue()), period = 'max', interval='1d')
        mpf.plot(data,type='candle', style='yahoo',title='{name}'.format(name=self.stockText.GetValue()),volume=True)
        
class TabFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # static text
        font = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        codeidText = wx.StaticText(self, -1, "股票代碼", pos=(20,10))
        codeidText.SetFont(font)
        numText = wx.StaticText(self, -1, "購買股數", pos=(20,40))
        numText.SetFont(font)
        
        # two textCtrl
        self.stockidText = wx.TextCtrl(self, pos=(200,10))
        self.numberText = wx.TextCtrl(self, pos=(200,40))
        
        # Button
        self.buyButton = wx.Button(self, wx.ID_ANY, 'Buy', pos=(400,40))
        self.buyButton.Bind(wx.EVT_BUTTON, self.OnButton)
        # self.testButton = wx.Button(self, wx.ID_ANY, 'test', pos=(400,100))
        # self.testButton.Bind(wx.EVT_BUTTON, self.OnButton2)
        
    def OnButton(self, event):
        temp = ""
        stockid = self.stockidText.GetValue()
        fullstockid = stockid+'.tw' #股票的full id
        stocknum = self.numberText.GetValue()
        stock = yf.Ticker(fullstockid)
        data = stock.history()
        data = data.reset_index()
        finalPrice = (data['Close'].iloc[-1])   #股票價格
        BeginningValue = float(stocknum)*finalPrice
        now = datetime.now()
        s = datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
        
        cur = conn.cursor()
        cur.execute("Insert into Record Values(?,?,?,?,?)", (stockid, s, stocknum, finalPrice, str(BeginningValue)))
        conn.commit()
        finish = wx.StaticText(self, -1, temp+"Complete trading", pos = (20,80))
        finish.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT))
        cur.execute("select * from OwnStock where name=?", (stockid,))
        if not cur.fetchone():
            valid = False #找不到
            cur.execute("Insert INTO OwnStock VALUES(?, ?, ?, ?, ?)", (stockid, stocknum, finalPrice, str(float(stocknum)*float(finalPrice)), str(float(stocknum)*float(finalPrice))))
            conn.commit()
        else:
            valid = True #有這支股票
            cur.execute("select * from OwnStock where Name=?", (stockid,))
            rows = cur.fetchall()
            ori_num=0
            ori_beginv=0
            ori_currentv=0
            for row in range(len(rows)):
                ori_num+=int(rows[row][1])
                ori_beginv+=float(rows[row][3])
                ori_currentv+=float(rows[row][4])
            cur.execute("Update OwnStock set Num=?, BeginV=? where Name=?", (str(ori_num+int(stocknum)), str(ori_beginv+BeginningValue), stockid))
            conn.commit()
            cur.execute("Update OwnStock set currentV=? where Name=?", (str(ori_currentv+BeginningValue), stockid))
            conn.commit()
        
        
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Project", size=(600,600))
         
        # Creating the Tab holders: Panel and Notebook
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        
        #Creating the Tab windows
        tab1 = TabOne(nb)
        tab2 = TabTwo(nb)
        tab3 = TabThree(nb)
        tab4 = TabFour(nb)
        
        

        # add Tabs to Notebook and give a name to the Tabs
        nb.AddPage(tab1, "MyStock")
        nb.AddPage(tab2, "BuyingRecord")
        nb.AddPage(tab3, "Share Price")
        nb.AddPage(tab4, "BuyingStock")
        
        

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

app = wx.App()
MainFrame().Show()
app.MainLoop()