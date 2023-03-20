import datetime
import uiautomation as auto
import uiautomation as ui

auto.uiautomation.SetGlobalSearchTimeout(5)  # 设置全局搜索超时 5

class WxUtil:
    # def __init__(self) -> None:
        # self.WeChatMainWndForPC = auto.WindowControl(searchDepth=1, Name="微信", ClassName='WeChatMainWndForPC')
        # self.NewContactProfileWnd = auto.PaneControl(searchDepth=1, Name="微信", ClassName='NewContactProfileWnd')
        # self.WeUIDialog = auto.WindowControl(searchDepth=2, Name="添加朋友请求", ClassName='WeUIDialog')

    def getWeChatMainWndForPC(self):
        self.WeChatMainWndForPC = auto.WindowControl(searchDepth=1, Name="微信", ClassName='WeChatMainWndForPC')
        return self.WeChatMainWndForPC
    
    def getNewContactProfileWnd(self):
        self.NewContactProfileWnd = auto.PaneControl(searchDepth=1, Name="微信", ClassName='NewContactProfileWnd')
        return self.NewContactProfileWnd
    
    def getWeUIDialog(self):
        self.WeUIDialog = auto.WindowControl(searchDepth=2, Name="添加朋友请求", ClassName='WeUIDialog')
        return self.WeUIDialog

    def goBackHome(self):
        # 不管什么情况，都先回到主界面
        WeChatMainWndForPC = self.getWeChatMainWndForPC()
        NewContactProfileWnd = self.getNewContactProfileWnd()
        WeUIDialog = self.getWeUIDialog()
        if WeUIDialog.Exists(1, 1):
            print("存在添加朋友请求,点击取消，回到主界面")
            WeUIDialog.ButtonControl(Name="取消").Click()
            WeChatMainWndForPC.ButtonControl(Name="聊天").Click()
            return
        if NewContactProfileWnd.Exists(1, 1):
            print("存在添加到通讯录弹窗，直接回主页面")
            WeChatMainWndForPC.ButtonControl(Name="聊天").Click()
            return
        if WeChatMainWndForPC.Exists(1, 1):
            print("已经在主界面")
            WeChatMainWndForPC.ButtonControl(Name="聊天").Click()
            return
        # 抛出异常
        raise Exception("未知异常，可能并没有运行微信")
    
    def addFriend(self, friendid,msg):
        self.goBackHome()
        WeChatMainWndForPC = self.getWeChatMainWndForPC()
        WeChatMainWndForPC.ButtonControl(Name="聊天").Click()
        txl=WeChatMainWndForPC.ButtonControl(Name="通讯录")
        # 转换为坐标点击
        x = txl.BoundingRectangle.xcenter()
        y = txl.BoundingRectangle.ycenter()
        ui.Click(x, y, 1)


        WeChatMainWndForPC.ButtonControl(Name="添加朋友").Click()
        searchEdit = WeChatMainWndForPC.EditControl(searchDepth=8,LocalizedControlType="编辑", Name="微信号/手机号")
        searchEdit.Click()
        # 输入搜索内容
        searchEdit.SendKeys(friendid)
        WeChatMainWndForPC.TextControl(Name="搜索：").Click()
        # 判断是否存在搜索结果
        searchResult = WeChatMainWndForPC.ListItemControl(Name="无法找到该用户，请检查你填写的帐号是否正确。")
        if searchResult.Exists(1, 1):
            print("不存在该用户")
            return
        # 点击搜索结果
        NewContactProfileWnd = self.getNewContactProfileWnd()
        if NewContactProfileWnd.Exists(1, 1):
            print("存在添加到通讯录弹窗，开始添加好友")
        else:
            print("未知异常，点击搜索结果后，没有出现添加到通讯录弹窗")
            return
        add=NewContactProfileWnd.ButtonControl(Name="添加到通讯录")
        if add.Exists(1, 1):
            add.Click()
        else:
            print("无法添加到通讯录，可能已经是好友了")
            return
        WeUIDialog = self.getWeUIDialog()
        if WeUIDialog.Exists(1, 1):
            print("填写验证信息和备注")
        else:
            print("未知异常，点击添加到通讯录后，没有出现添加朋友请求")
            return
        ed= WeUIDialog.TextControl(Name="发送添加朋友申请").GetParentControl().GetChildren()[1].GetChildren()[0]
        ed.Click()
        ed.SendKeys("{Ctrl}a")
        ed.SendKeys("{Del}")
        ed.SendKeys(msg)
        # 填写备注
        ed2= WeUIDialog.TextControl(Name="备注名").GetParentControl().GetChildren()[1].GetChildren()[0]
        ed2.Click()
        # 清空文本框
        ed2.SendKeys("{Ctrl}a")
        ed2.SendKeys("{Del}")
        # 当前时间
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ed2.SendKeys(friendid+" "+time)
        # WeUIDialog.ButtonControl(Name="确定").Click()
        WeUIDialog.ButtonControl(Name="取消").Click()
        print("添加好友成功",friendid)


# if __name__ == "__main__":
#     wx = WxUtil()
#     wx.addFriend("15577199924","你好")