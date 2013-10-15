#!/usr/bin/python
#coding:utf-8
import wx
import wx.grid
import os
import sys
import daishumao


class MyFrame(wx.Frame):    # 主界面

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
        self.CreateStatusBar()
        filemenu = wx.Menu()
        menuClose = filemenu.Append(-1, "&Close", " Close the tab you are looking now")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(-1, "E&xit", " Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.SetMenuBar(menuBar)
        self.nb = wx.Notebook(self)
        self.filesize = os.path.getsize("data")
        alldata = open("data", "r")
        for i in alldata.readlines():
            sys.argv = i.encode("utf-8")[:-1].split(" ")
            temparg = daishumao.main()
            if_h, if_v = False, False
            if "\\h" in sys.argv:
                if_h = True
            if "\\v" in sys.argv:
                if_v = True
            self.nb.AddPage(cjlists(self.nb, temparg[0], temparg[1], temparg[2], if_h, if_v), "Table 1")
            daishumao.setglobalvar()
        alldata.close()

    def OnTimer(self, event):    # 计时器，定时检查data中是否有新内容，如果有就更新主界面
        tempsize = os.path.getsize("data")
        if tempsize != self.filesize:
            self.filesize = tempsize
            alldata = open("data", "r")
            count = 1
            lastselect = self.nb.GetSelection()
            self.nb.DeleteAllPages()
            for i in alldata.readlines():
                sys.argv = i.encode("utf-8")[:-1].split(" ")
                temparg = daishumao.main()
                if_h, if_v = False, False
                if "\\h" in sys.argv:
                    if_h = True
                if "\\v" in sys.argv:
                    if_v = True
                daishumao.setglobalvar()
                self.nb.AddPage(cjlists(self.nb, temparg[0], temparg[1], temparg[2], if_h, if_v), "Table %d" % (count))
                count += 1
            alldata.close()
            self.nb.SetSelection(lastselect)

    def OnClose(self, event):   # 关闭Tab
        deleteone = self.nb.GetSelection()
        self.nb.DeletePage(self.nb.GetSelection())
        alldata = open("data", "r")
        newfile = ''
        count = 0
        for i in alldata.readlines():
            if count != deleteone:
                newfile += i.encode("utf-8")
            count += 1
        alldata.close()
        output = open('data', 'w')
        output.writelines(newfile)
        output.close()

    def OnExit(self, event):
        self.Close(True)


class cjlists(wx.Panel):   # Tab类，按照参数生成矩阵

    def __init__(self, parent, maxnum, allnum, theanswer, if_h, if_v):
        wx.Panel.__init__(self, parent)
        self.grid = wx.grid.Grid(self)
        self.n = len(allnum)
        self.m = len(allnum[0])
        self.grid.CreateGrid(self.n, self.m, 10)
        for i in range(self.n):
            for j in range(self.m):
                self.grid.SetCellValue(i, j, str(allnum[i][j]))
        for i in theanswer:
            if theanswer[i]:
                self.grid.SetCellBackgroundColour(i[0] % self.n, i[1] % self.m, "Red")
        self.grid.AutoSize()
        boxsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        boxsizer2 = wx.BoxSizer(wx.VERTICAL)
        themax = wx.StaticText(self, label="%s" % maxnum)
        themax.SetForegroundColour((255, 0, 0))
        boxsizer1.Add(self.grid, 2, flag=wx.ALL, border=0)
        boxsizer1.Add(boxsizer2, 1, flag=wx.ALL, border=0)
        boxsizer2.Add(themax, 1, flag=wx.CENTER, border=0)
        if if_h:
            self.button1 = wx.Button(self, -1, "→")
            self.Bind(wx.EVT_BUTTON, self.OnClickRight, self.button1)
            boxsizer2.Add(self.button1, 1, flag=wx.CENTER, border=0)
            self.button2 = wx.Button(self, -1, "←")
            self.Bind(wx.EVT_BUTTON, self.OnClickLeft, self.button2)
            boxsizer2.Add(self.button2, 1, flag=wx.CENTER, border=0)
        if if_v:
            self.button3 = wx.Button(self, -1, "↑")
            self.Bind(wx.EVT_BUTTON, self.OnClickTop, self.button3)
            boxsizer2.Add(self.button3, 1, flag=wx.CENTER, border=0)
            self.button4 = wx.Button(self, -1, "↓")
            self.Bind(wx.EVT_BUTTON, self.OnClickBottom, self.button4)
            boxsizer2.Add(self.button4, 1, flag=wx.CENTER, border=0)
        self.SetSizer(boxsizer1)

    def OnClickRight(self, event):  # 矩阵向右移动
        num = []
        color = []
        for i in range(self.n):
            num.append([])
            color.append([])
            for j in range(self.m):
                num[i].append(self.grid.GetCellValue(i, j))
                color[i].append(self.grid.GetCellBackgroundColour(i, j))
        for i in range(self.n):
            for j in range(self.m):
                self.grid.SetCellValue(i, j, num[i][(j - 1) % self.m])
                self.grid.SetCellBackgroundColour(i, j, color[i][(j - 1) % self.m])

    def OnClickLeft(self, event):  # 向左移动
        num = []
        color = []
        for i in range(self.n):
            num.append([])
            color.append([])
            for j in range(self.m):
                num[i].append(self.grid.GetCellValue(i, j))
                color[i].append(self.grid.GetCellBackgroundColour(i, j))
        for i in range(self.n):
            for j in range(self.m):
                self.grid.SetCellValue(i, j, num[i][(j + 1) % self.m])
                self.grid.SetCellBackgroundColour(i, j, color[i][(j + 1) % self.m])

    def OnClickTop(self, event):  # 向上移动
        num = []
        color = []
        for i in range(self.n):
            num.append([])
            color.append([])
            for j in range(self.m):
                num[i].append(self.grid.GetCellValue(i, j))
                color[i].append(self.grid.GetCellBackgroundColour(i, j))
        for i in range(self.n):
            for j in range(self.m):
                self.grid.SetCellValue(i, j, num[(i + 1) % self.n][j])
                self.grid.SetCellBackgroundColour(i, j, color[(i + 1) % self.n][j])

    def OnClickBottom(self, event):  # 向下移动
        num = []
        color = []
        for i in range(self.n):
            num.append([])
            color.append([])
            for j in range(self.m):
                num[i].append(self.grid.GetCellValue(i, j))
                color[i].append(self.grid.GetCellBackgroundColour(i, j))
        for i in range(self.n):
            for j in range(self.m):
                self.grid.SetCellValue(i, j, num[(i - 1) % self.n][j])
                self.grid.SetCellBackgroundColour(i, j, color[(i - 1) % self.n][j])


if __name__ == '__main__':
    if len(os.popen("ps aux | grep python").readlines()) != 3:     # 如果窗口已经存在，就将命令存入data文件，然后退出。保证只有一个主窗口
        output = open('data', 'a')
        output.writelines(' '.join(sys.argv) + '\n')
        output.close()
        exit(0)
    output = open('data', 'w')
    output.writelines(' '.join(sys.argv) + '\n')
    output.close()
    app = wx.App(False)
    frame = MyFrame(None, title="Homework03")
    frame.Show()
    app.MainLoop()
