auto.waitFor()



while(true){
    var map = new Map();
    runAllWx_id(map,"哈喽，备考神器ACE用户，拉你进ACE私人教练备考群，报名备考可在社群中反馈，权威导师答疑解惑");
}


// while(true){
//     // for (var [value, key] of map) {
//     //     backToHome();
//     //     print(key + '  ============》  ' + value);
//     //     if(Array.isArray(value)){
//     //         print("是数组，开始切换微信号")
//     //         // 切换微信号，循环数组
//     //         for (var i = 0; i < value.length; i++) {
//     //             print("切换到微信号：" + value[i]);
//     //             // 切换微信号
//     //             boo=changeWx(value[i]);
//     //             print("执行任务中。。。。")
//     //             sleep(1000);
//     //             print("任务结束")
//     //         }
//     //     }else{
//     //         print("不是数组，开始切换app")
//     //         // 切换app
//     //         changeApp(key);
//     //         print("执行任务中。。。。")
//     //         sleep(1000);
//     //         print("任务结束")
//     //     }
//     // }

// }


// 单次运行所有任务
// （已废除）
function runAllWx_id(map,msg){
    backToHome();
    var wx_id_array = getOtherWechatId();
    let str="";
    for (var i = 0; i < wx_id_array.length; i++) {
        str += wx_id_array[i];
    }
    let wx_id_md5=md5(str);
    if(map.has(wx_id_md5)){
        // 已经执行过了
        print("所有微信都执行过了 , 结束这轮任务");
        return;
    }
    // 将记录保存到map
    // 遍历arr ，执行任务
    for (var i = 0; i < wx_id_array.length; i++) {
        str += wx_id_array[i];
        // 切换微信号
        changeWx(wx_id_array[i]);
        backToHome();
        clickTabbar("微信");
        // 执行任务
        for (var j = 0; j < 3; j++) {
            print("执行任务中。。。。")
            addFriends(getData(),msg);
            sleep(1000);
            print("任务结束")
        }
        backToHome();
    }
    map.set(wx_id_md5,wx_id_array);
    backToHome();
    changeApp();
    sleep(1000);
    runAllWx_id(map);
}


// 重新定义，直接从txt中获取一个手机号，然后在txt中删除该手机号，如果txt中没有手机号了，则退出程序
function getData(){
    let path = files.getSdcardPath()+"/脚本/data.txt";
    if(!files.exists(path)){
        console.info("文件不存在: " + path);
        console.info("创建文件: " + path);
        files.createWithDirs(path);
        console.error("请在文件中添加数据, 然后重新运行脚本")
        exit();
    }
    var file = open(path,"r");
    var data = file.readlines();
    file.close();
    data = data.filter(item=>{
                return !( item == '' || item == ' ');
            })
    if(data.length==0){
        print("没有数据了，退出程序");
        exit();
    }

    var phone = data[0];
    print("读取到的数据是："+phone+"，还剩"+(data.length-1)+"条数据");
    // js数组删除第一个元素 不要用splice ，shift()都有问题
    data=deleteLast(data);
    console.log(data);
    // 拼接数据，每个数据之间换行
    let str = "";
    for (var i = 0; i < data.length; i++) {
        str += data[i] + "\r\n"
    }
    // 将数据写回去
    files.write(path, str);
    return phone;
}
function deleteLast(arr){
    var newArr = [];
    for (var i = 1; i <= arr.length-1; i++) {
        newArr.push(arr[i]);
    }
    return newArr;
}

// 循环加好友
function runTask(iphone_arr,msg){
    for (var i = 0; i < iphone_arr.length; i++) {
        var wx_id = iphone_arr[i];
        print("开始添加好友："+wx_id);
        addFriends(wx_id, msg);
        sleep(1000);
    }
}
// 单次加好友

function addFriends(friendNum,msg){
    print("开始添加好友："+friendNum);
    backToHome();
    sleep(2000);
    // 切换到 首页 页面
    print("切换到 微信 页面");
    clickTabbar("微信");
    sleep(2000);
    desc("更多功能按钮").findOne().click();
    sleep(1000);
    click("添加朋友");
    sleep(1000);
    id("com.tencent.mm:id/j69").depth(19).findOne().click();
    sleep(1000);
    id("com.tencent.mm:id/eg6").depth(9).findOne().click();
    sleep(1000);
    setText(friendNum);
    sleep(1000);
    className("android.widget.RelativeLayout").depth(10).clickable(true).findOne().click();
    sleep(1000);

    var widget=id("com.tencent.mm:id/kms").findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
    var ti=10;
    while(true){
        if(ti==0){
            break;
        }
        el1=text("该用户不存在").exists();
        el2=id("com.tencent.mm:id/khj").exists();
        if(el1 || el2){
            break;
        }
        sleep(1000);
        ti--;
    }

    if(text("该用户不存在").exists()){
        toast("该用户不存在");
    }else{
        toast("该用户存在");
        id("com.tencent.mm:id/iwg").waitFor();
        sleep(1000);
        widget=id("com.tencent.mm:id/khj").findOne();
        click(widget.bounds().centerX(), widget.bounds().centerY());
        id("com.tencent.mm:id/j0w").findOne().click();
        
        id("com.tencent.mm:id/iq9").waitFor();
        setText("");
        setText(0,msg);
        // 获取当前时间
        var date = new Date();
        setText(1,friendNum+" "+date.toLocaleString());
        text("发送").findOne().click();

        sleep(3000);
        id("com.tencent.mm:id/g1").waitFor();
        sleep(1000);
        widget=id("com.tencent.mm:id/g1").findOne();
        click(widget.bounds().centerX(), widget.bounds().centerY());
    }
    sleep(1000);
    text("取消").findOne().click();
    sleep(2000);
    widget=id("com.tencent.mm:id/g1").findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
    print("添加好友结束");
 }

// 切换到wx_id所在微信 （已废除）
function findWx_id(map,wx_id){
    // 确保在首页
    backToHome();
    let nowWx_id = getWechatId();
    print("findWx_id:当前微信号："+nowWx_id+"，目标微信号："+wx_id+"")
    if(nowWx_id == wx_id){
        return true;
    }
    // todo 这里需要切换其他微信号，来判断是否有目标微信号，如何防止重复排查？
    






    // }else{
    //     // 遍历map
    //     for (var [value, key] of map) {

    //         // if(value != nowWx_id){
    //         //     // 跳过
    //         //     continue;
    //         // }
    //         // // 判断value是否是数组
    //         // if(Array.isArray(value)){
    //         //     // 遍历数组
    //         //     for (var i = 0; i < value.length; i++) {
    //         //         if(value[i] == nowWx_id){
    //         //             // 跳过
    //         //             continue;
    //         //         }
    //         //         // 切换微信号
    //         //         changeWx(value[i]);
    //         //         findWx_id(map,wx_id);
    //         //     }
    //         // }
    //         // changeApp(key);
    //         // findWx_id(map,wx_id);
    //     }
    // }
}


// 获取手机号数据
// function getData(){
//     if(!files.exists(path)){
//         console.info("文件不存在: " + path);
//         console.info("创建文件: " + path);
//         files.createWithDirs(path);
//         console.error("请在文件中添加数据, 然后重新运行脚本")
//         exit();
//     }
//     // 创建一个数组，保存数据
//     var data = [];
//     var file = open(path);
//     var line = file.readline();
//     while(line){
//         // console.log(line);
//         data.push(line);
//         line = file.readline();
//     }
//     file.close();
//     // 去除数组中的空，或者空格
//     // console.log('原数组：',data)
//     data = data.filter(item=>{
//         return !( item == '' || item == ' ');
//     })
//     console.log('数据列表：',data)
//     return data;
// }


// 同一app内切换微信号
function changeWx(newWx_id){
    print("changeWx:切换到微信号："+newWx_id+"")
    backToHome();
    sleep(2000);
    // 切换到 我 页面
    clickTabbar("我");
    sleep(2000);
    // 点击设置
    // click("设置");
    print("changeWx:设置是否存在："+ text("设置").exists())
    widget = text("设置").findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
    sleep(1000);
    // 往上滑动
    swipe(500, 2000, 500, 1500, 2000);
    // 切换账号
    widget = id("com.tencent.mm:id/khj").depth(20).findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
    sleep(1000);
    // 获取数据
    el = id("com.tencent.mm:id/d8").depth(14).find();
    // el是一个集合，获取该集合的长度，并遍历该集合
    // print(el.length)
    for (var i = 0; i < el.length; i++) {
        // print(el[i].text())
        if(el[i].text() == newWx_id){
            click(newWx_id);
            // id("com.tencent.mm:id/l29").depth(21).waitFor();
            sleep(12000);
            return true;
        }
    }
    return false;
}





// =====================切换任务=====================

// 数据初始化，切换微信，记录每个微信的微信号数量，用map存储
// md5位置和账号写反了，，，难怪key和value对不上
function init(map){
    backToHome();
    // 创建一个map，用于存储每个微信号的数量
    // var map = new Map();
    // 获取当前微信号
    var wx_id_array = getOtherWechatId();
    // 判断wx_id_array长度是否大于1，如果大于1，说明有其他微信号
    if(wx_id_array.length > 1){
        let wx_id_md5="";
        // 遍历wx_id_array，获取每个微信号
        for (var i = 0; i < wx_id_array.length; i++) {
            // 获取当前微信号
            wx_id_md5 += wx_id_array[i];
            // 判断map中是否存在该微信号，如果不存在，设置该微信号的数量为0
        }
        print("拼接后的数据"+wx_id_md5);
        // 取MD5
        wx_id_md5 = md5(wx_id_md5);
        print("MD5后的数据"+wx_id_md5);
        // 判断map中是否存在wx_id_md5
        if(hasKey(map,wx_id_md5)){
            return map;
        }else{
            map.set(wx_id_array,wx_id_md5);
            changeApp();
            init(map);
        }
    }else{
        // 取MD5
        print("拼接后的数据"+wx_id_array[0]);
        wx_id_md5 = md5(wx_id_array[0]);
        print("MD5后的数据"+wx_id_md5);
        // 判断map中是否存在wx_id_md5
        if(hasKey(map,wx_id_md5)){
            return map;
        }else{
            map.set(wx_id_array,wx_id_md5);
            changeApp();
            init(map);
        }
    }
}

// 获取当前微信号,返回数据是字符串
// 使用前需要判断当前处于微信消息界面
function getWechatId(){
    backToHome();
    clickTabbar("我");
    sleep(1000);
    click("设置");
    sleep(1000);
    // 网上滑动
    swipe(500, 2000, 500, 1500, 1000);

    // print(id("com.tencent.mm:id/khj").depth(20).exists())
    sleep(1000);
    widget = id("com.tencent.mm:id/khj").depth(20).findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());


    // print(id("com.tencent.mm:id/d8").depth(14).exists())
    sleep(1000);
    wx_id=text("当前使用").findOne().parent().parent().child(1).child(1).text();
    // print(bo.text());
    print("当前微信ID为：",wx_id);
    backToHome();
    return wx_id;
}

// 获取当前微信登录的其他微信号，返回数据是数组
function getOtherWechatId(){
    print("getOtherWechatId:获取当前微信登录的其他微信号");
    backToHome();
    // 创建一个list，用于存储其他微信号
    list = new Array();
    print("getOtherWechatId:切换到 我 页面");
    sleep(2000);
    clickTabbar("我");
    sleep(2000);
    print("getOtherWechatId:点击设置");
    // while(!click("设置"));
    print("getOtherWechatId:设置是否存在："+ text("设置").exists())
    widget = text("设置").findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
    sleep(2000);
    // 网上滑动
    swipe(500, 2000, 500, 1500, 1000);

    // print(id("com.tencent.mm:id/khj").depth(20).exists())
    sleep(1000);
    widget = id("com.tencent.mm:id/khj").depth(20).findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());


    // print(id("com.tencent.mm:id/d8").depth(14).exists())
    sleep(1000);
    el = id("com.tencent.mm:id/d8").depth(14).find();
    // el是一个集合，获取该集合的长度，并遍历该集合
    // print(el.length)
    for (let i = 0; i < el.length; i++) {
        // print(el[i].text())
        list.push(el[i].text());
    }
    // 返回
    backToHome();
    print("其他微信号为：",list);
    return list;
}

// 确保回到首页
function backToHome(){
    // 若bo1为true，说明当前是 微信/通讯录/发现 界面
    bo1=desc("更多功能按钮").exists();
    // 若bo2为true，说明当前是 我 界面（bo2怎么哪里都能见到？见鬼）
    bo2=text("表情").exists() && text("设置").exists() && text("微信").exists();

    // bo3为true，说明当前在设置页面内 
    bo3=text("关怀模式").exists() && text("隐私").exists() && text("聊天").exists();
    // bo4为true，说明当前在切换账号内
    bo4=text("当前使用").exists();

    // bo5 添加好友页面
    bo5=text("雷达加朋友").exists() && text("添加朋友").exists();
    // bo6 个人信息页面
    bo6=text("发消息").exists() && text("音视频通话").exists();

    // bo7 切换账号内
    bo7=id("com.tencent.mm:id/d8").depth(14).exists();
    bo8=text("当前使用").exists();
    
    // print("bo1:",bo1,"bo2:",bo2,"bo3:",bo3,"bo4:",bo4,"bo5:",bo5,"bo6:",bo6,"bo7:",bo7,"bo8:",bo8);
    if(bo7){
        print("当前在切换账号内");
        if(!bo8){
            print("当前在切换账号内，但是没有当前使用,账号切换出现异常，重新切换");
            el = id("com.tencent.mm:id/d8").depth(14).find();
            //点击第一个
            click(el[0].bounds().centerX(), el[0].bounds().centerY());
            sleep(13000);
        }
        clickBack();
        sleep(2000);
        backToHome();
        return true;
    }
    if(bo3 || bo5){
        print("当前在设置页面或者添加好友页面内");
        clickBack();
        return true;
    }
    if(bo4){
        print("当前在切换账号内");
        clickBack();
        clickBack();
        return true;
    }
    if(bo6){
        print("当前在个人信息页面内");
        clickBack();
        text("取消").click();
        clickBack();
        return true;
    }
    if(bo1 || bo2){
        print("当前在首页");
        return true;
    }
    if(text("取消").exists()){
        print("未知页面，但是有取消按钮");
        text("取消").click();
    }
    if(id("com.tencent.mm:id/g1").exists()){
        print("未知页面，但是有返回按钮");
        clickBack();
    }
    // 若以上都不是，说明在其他app？？启动微信，然后重新执行backToHome()
    print("当前不在微信界面，启动微信");
    launchApp("微信");
    sleep(2000);
    backToHome();
}

// 点击左上角的返回按钮
function clickBack(){
    sleep(1000);
    widget=id("com.tencent.mm:id/g1").findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
}

// 首页底部tabbar栏点击
function clickTabbar(tabbar){
    sleep(1000);
    widget = id("com.tencent.mm:id/f2s").depth(13).text(tabbar).findOne();
    click(widget.bounds().centerX(), widget.bounds().centerY());
}

// 切换任务栏
function changeApp(){
    sleep(2000)
    recents()
    sleep(2000)
    swipe(500, 1500, 900, 1500, 2000)
    click(500, 1500)
    sleep(2000);
    // 若bo1为true，说明当前是 微信/通讯录/发现 界面
    bo1=desc("更多功能按钮").exists();
    // 若bo2为true，说明当前是 我 界面（bo2怎么哪里都能见到？见鬼）
    bo2=text("表情").exists() && text("设置").exists() && text("微信").exists();

    // bo3为true，说明当前在设置页面内 
    bo3=text("关怀模式").exists() && text("隐私").exists() && text("聊天").exists();
    // bo4为true，说明当前在切换账号内
    bo4=text("当前使用").exists();

    // bo5 添加好友页面
    bo5=text("雷达加朋友").exists() && text("添加朋友").exists();
    // bo6 个人信息页面
    bo6=text("发消息").exists() && text("音视频通话").exists();

    if(bo1 || bo2 || bo3 || bo4 || bo5 || bo6){
        backToHome();
        return true;
    }else{
        print("当前不是微信界面，继续切换");
        changeApp();
    }
}


function md5(str){
    return java.math.BigInteger(1, java.security.MessageDigest.getInstance("MD5").digest(java.lang.String(str).getBytes())).toString(16);
}

// 遍历map，判断是否存在该微信号
function hasKey(map, key){
    for (var [a, b] of map) {
        print(a + ' = ' + b, key);
        if(b == key){
            print("map中存在该微信号,ture");
            return true;
        }
    }
    return false;
}
