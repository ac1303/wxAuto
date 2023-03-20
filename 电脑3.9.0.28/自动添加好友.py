import re
from wxutil import WxUtil


# 从当前目录下的phone.txt中按行分割读取手机号码
def getPhone():
    phone = []
    with open("phone.txt","r") as f:
        for line in f.readlines():
            line = line.strip()
            line = re.sub("\D", "", line)
            if line not in phone:
                phone.append(line)
    # 获取倒数第一个手机号码
    # 判断是否读完
    if len(phone) == 0:
        raise Exception("手机号码已经读取完毕，请添加手机号码")
    p = phone[0]
    # 删除p
    phone.remove(p)
    with open("phone.txt","w") as f:
        for p1 in phone:
            f.write(p1 + "\r")
    return p

if __name__ == "__main__":
    wx = WxUtil()
    # 这里填写一个微信号需要添加的好友数量
    # 比如一个微信号需要添加10个好友，那么这里就填写10
    for i in range(0,10):
        # 这里填写发送好友申请时候携带的消息,
        wx.addFriend(getPhone(),"好友申请消息")

# 运行流程,先爬取手机号 不练不可后台爬取手机号.py 第126行和第128行填写数据
# 爬取手机号后会在当前目录下生成一个phone.txt文件
# 然后运行这个 自动添加好友.py 文件,设置一次需要添加多少个好友,然后运行

