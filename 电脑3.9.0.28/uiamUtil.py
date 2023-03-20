import os
import time
import subprocess
 
import uiautomation as ui
 
 
class AiUiAutomation(object):
 
    @staticmethod
    def setLogPath(savePath):
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        fileName = "AutomationLog_%s.txt" % time.strftime("%Y_%m_%d_%H_%M_%S")
        ui.Logger.SetLogFile(os.path.join(savePath, fileName))
 
    @staticmethod
    def openApplication(app, Name=None, ClassName=None, searchDepth=1, timeout=5):
        """
        @summary: 打开应用
        @param app: 应用名称或exe文件的绝对路径
        @param Name: 窗体的Name属性，可通过inspect工具查看
        @param ClassName: 窗体的ClassName属性，可通过inspect工具查看
        @param searchDepth: 搜索深度
        @param timeout: 超时时间
        @return: (True, ) or (False, "打开失败")
        @attention: 非系统自带应用最好通过exe绝对路径打开
        """
        if os.path.isabs(app):
            if not os.path.exists(app):
                return False, "不存在[%s]" % app
        subprocess.Popen(app)
        window = AiUiAutomation.WindowControl(Name, ClassName, searchDepth, timeout)
        if window is None:
            return False, "打开失败"
        return True, window
 
    @staticmethod
    def closeApplication(exeName):
        os.popen('taskkill /F /IM {}'.format(exeName))
        return True, "Ok"
 
    @staticmethod
    def WindowControl(Name, ClassName=None, searchDepth: int = 0xFFFFFFFF, timeout=5):
        """
        @summary: 获取窗体对象
        @param Name: 窗口Name属性值
        @param ClassName: 窗口ClassName属性值
        @param searchDepth: 搜索深度
        @param timeout: 超时时间
        @return:
        """
        searchProperties = {}
        if Name is not None:
            searchProperties.update({"Name": Name})
        if ClassName is not None:
            searchProperties.update({"ClassName": ClassName})
        window = ui.WindowControl(searchDepth=searchDepth, **searchProperties)
        # 可以判断window是否存在
        if ui.WaitForExist(window, timeout):
            return window
        return None
 
    @staticmethod
    def setWindowActive(window: ui.WindowControl):
        """
        @summary: 激活窗口
        @param window: 待激活窗口对象
        @return: True or False
        """
        return window.SetActive()
 
    @staticmethod
    def setWindowTopMost(window: ui.WindowControl):
        """
        @summary: 将窗口置顶
        @param window: 待置顶窗口对象
        @return: True or False
        """
        return window.SetTopmost()
 
    @staticmethod
    def moveWindowToCenter(window: ui.WindowControl):
        """
        @summary: 将窗口居中显示
        @param window: 待居中显示的窗口对象
        @return: True or False
        """
        return window.MoveToCenter()
 
    @staticmethod
    def checkWindowExist(window: ui.WindowControl, timeout):
        """
        @summary: 检查窗口是否存在
        @param window: 待检查的窗口对象
        @param timeout: 最大检查时长
        @return: True or False
        """
        return window.Exists(timeout)
 
    @staticmethod
    def closeWindow(window: ui.WindowControl):
        """
        @summary: 关闭窗口
        @param window: 待关闭的窗口对象
        @return: True or False
        """
        pattern = window.GetWindowPattern()
        if pattern is None:
            return False
        return pattern.Close()
 
    @staticmethod
    def showWindowMax(window: ui.WindowControl):
        """
        @summary: 窗口最大化显示
        @param window: 窗口对象
        @return: True or False
        """
        if window.IsMaximize():
            return True
        return window.Maximize()
 
    @staticmethod
    def showWindowMin(window: ui.WindowControl):
        """
        @summary: 窗口最小化显示
        @param window: 窗口对象
        @return: True or False
        """
        if window.IsMinimize():
            return True
        return window.Minimize()
 
    @staticmethod
    def switchWindow(window: ui.WindowControl):
        """
        @summary: 切换到目标窗口
        @param window: 目标窗口对象
        @return:
        """
        if not window.IsTopLevel():
            return False
        window.SwitchToThisWindow()
        return True
 
    @staticmethod
    def MenuItemControl(parent: ui.WindowControl, SubName=None, Name=None):
        """
        @summary: 获取菜单选项控件
        @param parent: 父窗体
        @param SubName: 控件部分名字
        @param Name: 控件名字，SubName、Name只能使用一个，不能同时使用
        @return:
        @attention: 有时候通过Name可能获取不到控件，可以尝试通过SubName获取
        """
        if SubName is not None:
            return parent.MenuItemControl(SubName=SubName)
        if Name is not None:
            return parent.MenuItemControl(Name=Name)
 
    @staticmethod
    def clickMenuItemBySubName(parent: ui.WindowControl, SubName, waitTime=1, useLoc=False):
        """
        @summary: 根据控件名称部分内容点击菜单选项
        @param parent: 菜单所在窗口
        @param SubName: 菜单控件名称部分内容
        @param waitTime: 点击后等待时长
        @param useLoc: 是否转化成坐标进行点击，之所以转成坐标点击是因为有时候点击名称会失败
        @return:
        """
        menuItem = parent.MenuItemControl(SubName=SubName)
        if useLoc:
            x = menuItem.BoundingRectangle.xcenter()
            y = menuItem.BoundingRectangle.ycenter()
            AiUiAutomation.click(x, y, waitTime)
        else:
            menuItem.Click(waitTime=waitTime)
 
    @staticmethod
    def clickMenuItemByName(parent: ui.WindowControl, Name, waitTime=1, useLoc=False):
        """
        @summary: 根据控件名称点击菜单选项
        @param parent: 菜单所在窗口
        @param Name: 菜单控件名称
        @param waitTime: 点击后等待时长
        @param useLoc: 是否转化成坐标进行点击，之所以转成坐标点击是因为有时候点击名称会失败
        @return:
        """
        menuItem = parent.MenuItemControl(Name=Name)
        if useLoc:
            x = menuItem.BoundingRectangle.xcenter()
            y = menuItem.BoundingRectangle.ycenter()
            AiUiAutomation.click(x, y, waitTime)
        else:
            menuItem.Click(waitTime=waitTime)
 
    @staticmethod
    def getControlRectCenter(control: ui.Control):
        """
        @summary: 获取控件的中心点坐标
        @param control: 目标控件
        @return: (x, y)
        """
        x = control.BoundingRectangle.xcenter()
        y = control.BoundingRectangle.ycenter()
        return x, y
 
    @staticmethod
    def takeScreenshots(savePath, control=None):
        """
        @summary: 截图并保存
        @param savePath: 保存文件路径
        @param control: 控件对象，默认全屏截图
        @return:
        """
        if control is None:
            control = ui.GetRootControl()
        if not isinstance(control, ui.PaneControl):
            return False, "参数control类型错误"
        control.CaptureToImage(savePath)
        # bitmap = ui.Bitmap.FromControl(control, startX, startY, width, height)
        # bitmap.ToFile(savePath)
        return True, savePath
 
    @staticmethod
    def showDesktop():
        """
        @summary: Show Desktop by pressing win + d
        """
        ui.SendKeys('{Win}d')
 
    @staticmethod
    def click(x, y, waitTime=0.5):
        """
        @summary: 鼠标点击指定坐标
        @param x: 横坐标x值，int类型
        @param y: 纵坐标y值，int类型
        @param waitTime: 点击后等待时间
        @return:
        """
        ui.Click(x, y, waitTime)
 
    @staticmethod
    def rightClick(x, y, waitTime=0.5):
        """
        @summary: 鼠标右键单击指定坐标
        @param x: 横坐标x值，int类型
        @param y: 纵坐标y值，int类型
        @param waitTime: 点击后等待时间
        @return:
        """
        ui.RightClick(x, y, waitTime)
 
    @staticmethod
    def dragDrop(startX, startY, endX, endY, moveSpeed=1, waitTime=0.5):
        """
        @summary: 鼠标拖拽(鼠标从(startX,startY)位置按下鼠标拖动到(endX,endY)位置)
        @param startX: 起始位置X坐标
        @param startY: 起始位置Y坐标
        @param endX: 终点位置X坐标
        @param endY: 终点位置Y坐标
        @param moveSpeed: 拖拽速度
        @param waitTime: 拖拽完成后等待时间
        @return:
        """
        ui.PressMouse(startX, startY, 0.05)
        ui.MoveTo(endX, endY, moveSpeed, 0.05)
        ui.ReleaseMouse(waitTime)
 
    @staticmethod
    def ComboBoxControl(parent: ui.WindowControl, Name=None, AutomationId=None, timeout=3):
        """
        @summary: 获取下拉列表控件对象
        @param parent: 所在窗口
        @param Name: 下拉列表Name属性值
        @param AutomationId: 下拉列表AutomationId值
        @param timeout: 超时时间
        @return:
        """
        searchProperties = {}
        if Name is not None:
            searchProperties.update({"Name": Name})
        if AutomationId is not None:
            searchProperties.update({"AutomationId": AutomationId})
        combox = parent.ComboBoxControl(**searchProperties)
        # 可以判断combox是否存在
        if combox.Exists(timeout):
            return combox
        return None
 
    @staticmethod
    def selectComboBoxItem(combo: ui.ComboBoxControl, itemName, waitTime=0.5):
        """
        @summary: 选择下拉框选项
        @param combo: 待操作的下拉框控件对象
        @param itemName: 待选择的选项名称
        @param waitTime: 选择后的等待时长
        @return:
        @attention: 此方法在有些下拉框列表可能不生效, 比如用老的QT版本开发的应用.
        """
        return combo.Select(itemName=itemName, waitTime=waitTime)
 
    @staticmethod
    def ListControl(parent: ui.WindowControl, Name=None, AutomationId=None, timeout=3):
        """
        @summary: 获取列表控件对象
        @param parent: 所在窗口
        @param Name: 列表Name属性值
        @param AutomationId: 列表AutomationId值
        @param timeout: 超时时间
        @return:
        """
        searchProperties = {}
        if Name is not None:
            searchProperties.update({"Name": Name})
        if AutomationId is not None:
            searchProperties.update({"AutomationId": AutomationId})
        listControl = parent.ListControl(**searchProperties)
        # 可以判断列表是否存在
        if listControl.Exists(timeout):
            return listControl
        return None
 
    @staticmethod
    def ListItemControl(parent: ui.ListControl, Name=None, SubName=None, timeout=3):
        """
        @summary: 获取列表item控件对象
        @param parent: 父列表控件对象
        @param Name: Name属性值
        @param SubName: SubName值
        @param timeout: 超时时间
        @return:
        """
        if Name is not None:
            itemControl = parent.ListItemControl(Name=Name)
            if itemControl.Exists(timeout):
                return itemControl
        itemControl = parent.ListItemControl(SubName=SubName)
        if itemControl.Exists(timeout):
            return itemControl
 
    @staticmethod
    def selectListItemByName(parent: ui.ListControl, Name=None, SubName=None, waitTime=0.5, isScroll=True):
        """
        @summary: 根据名称选择列表item
        @param parent: 父列表控件对象
        @param Name: 列表item名称完整内容
        @param SubName: SubName值，列表item名称部分内容
        @param waitTime: 点击完成后等待时长
        @param isScroll: 是否允许滚动查找到目标item后再点击
        @return:
        """
        itemControl = AiUiAutomation.ListItemControl(parent, Name, SubName)
        if itemControl is None:
            return False
        if isScroll:
            itemControl.GetScrollItemPattern().ScrollIntoView()
        itemControl.Click(waitTime=waitTime)
        return True
 
    @staticmethod
    def ButtonControl(parent: ui.WindowControl, Name=None, timeout=3):
        """
        @summary: 获取按钮控件对象
        @param parent: 按钮所在窗口对象
        @param Name: 按钮名称
        @param timeout: 超时时间
        @return:
        """
        button = parent.ButtonControl(Name=Name)
        if button.Exists(timeout):
            return button
        return None
 
    @staticmethod
    def clickButton(button: ui.ButtonControl, waitTime=0.5):
        """
        @summary: 点击按钮
        @param button: 待点击的按钮对象
        @param waitTime: 点击后等待时长
        @return:
        """
        if button is None:
            return False
        button.Click(waitTime=waitTime)
        return True
 
    @staticmethod
    def CheckBoxControl(parent: ui.Control, Name=None, AutomationId=None, timeout=3):
        """
        @summary: 获取复选框控件对象
        @param parent: 复选框所在窗口对象
        @param Name: 复选框名称
        @param AutomationId: 复选框id
        @param timeout: 超时时间
        @return:
        """
        searchProperties = {}
        if Name is not None:
            searchProperties.update({"Name": Name})
        if AutomationId is not None:
            searchProperties.update({"AutomationId": AutomationId})
        checkBox = parent.CheckBoxControl(**searchProperties)
        # 可以判断复选框是否存在
        if checkBox.Exists(timeout):
            return checkBox
        return None
 
    @staticmethod
    def selectCheckBox(checkBox: ui.CheckBoxControl, waitTime=0.5):
        """
        @summary: 选中复选框
        @param checkBox: 复选框对象
        @param waitTime: 等待时间
        @return:
        """
        if checkBox.GetTogglePattern().ToggleState == 0:
            checkBox.Click(waitTime=waitTime)
        if checkBox.GetTogglePattern().ToggleState == 1:  # 1是选中状态，0是未选中状态
            return True
        return False
 
    @staticmethod
    def unSelectCheckBox(checkBox: ui.CheckBoxControl):
        """
        @summary: 取消勾选复选框
        @param checkBox: 复选框对象
        @return:
        """
        if checkBox.GetTogglePattern().ToggleState == 1:
            checkBox.Click()
        if checkBox.GetTogglePattern().ToggleState == 0:
            return True
        return False
 
    @staticmethod
    def ProgressBarControl(parent: ui.WindowControl, ClassName=None, Name=None, AutomationId=None, timeout=3):
        searchProperties = {}
        if ClassName is not None:
            searchProperties.update({"ClassName": ClassName})
        if Name is not None:
            searchProperties.update({"Name": Name})
        if AutomationId is not None:
            searchProperties.update({"AutomationId": AutomationId})
        progressBar = parent.ProgressBarControl(**searchProperties)
        # 可以判断复选框是否存在
        if progressBar.Exists(timeout):
            return progressBar
        return None
 
    @staticmethod
    def getProgressBarValue(progressBar: ui.ProgressBarControl):
        return int(progressBar.GetLegacyIAccessiblePattern().Value)
 
    @staticmethod
    def EditControl(parent: ui.WindowControl, ClassName=None, Name=None, AutomationId=None, timeout=3):
        searchProperties = {}
        if ClassName is not None:
            searchProperties.update({"ClassName": ClassName})
        if Name is not None:
            searchProperties.update({"Name": Name})
        if AutomationId is not None:
            searchProperties.update({"AutomationId": AutomationId})
        edit = parent.EditControl(**searchProperties)
        # 可以判断编辑框是否存在
        if edit.Exists(timeout):
            return edit
        return None
 
    @staticmethod
    def inputEditControlText(editControl: ui.EditControl, text):
        return editControl.GetValuePattern().SetValue(text)
 
if __name__ == '__main__':
    app = r'D:\程序安装\Notepad++\notepad++.exe'
    AiUiAutomation.setLogPath(r'D:\report')
    sta, window = AiUiAutomation.openApplication(app, Name=None, ClassName="Notepad++")
    if sta:
        AiUiAutomation.clickMenuItemByName(window, Name="设置(T)")
        AiUiAutomation.clickMenuItemBySubName(window, SubName="首选项...", useLoc=True)
        firstChoiceWindow = AiUiAutomation.WindowControl("首选项")
        button = AiUiAutomation.ButtonControl(firstChoiceWindow, Name="关闭")
        AiUiAutomation.clickButton(button)