Flasky搭建的博客系统
=======
## 作品简介
大三上学期开始，看了下分布式爬虫和分布式系统的内容，python用的挺爽。以前一直写java spring,快写傻了，有点烦，就看了下python的web框架flask，脚本语言嘛玩儿玩儿就好，不过真的好玩儿，像我这种前端白痴都能很快写出能让人类看懂的页面！后台代码也不知少了多少（放飞自我的时候，谁还会去考虑稳定性哈哈）

上个月写的一个小比赛的作品不想浪费，精简改装了下，成了基于flask的轻博客系统，博客文章基于markdown语法，基本功能还是比较全的，详见功能介绍。最近主要准备考试，考试结束后会尽快加入前端美化、文章自定义标签、selenium自动化测试、阿里云部署步骤和刚看的nlp搜索功能。

![图一](https://thumbnail0.baidupcs.com/thumbnail/1df3d3afe20ade463b4efef8b5a1acf0?fid=1335854244-250528-441279785711769&time=1513252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-O2ZXn82LZf1PX6%2FSH1vFeT%2Foqn8%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=8068012804480000451&dp-callid=0&size=c710_u400&quality=100&vuk=-&ft=video)

![图二](https://thumbnail0.baidupcs.com/thumbnail/2eb81afe687efb87b524657a6d37efa7?fid=1335854244-250528-889445863332395&time=1513252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-Nbn9r48W7XyZLUnpaAcjZADKQ5g%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=8067946394048852066&dp-callid=0&size=c710_u400&quality=100&vuk=-&ft=video)

![图三](https://thumbnail0.baidupcs.com/thumbnail/f0bb55f63486c06adb09487b47673aca?fid=1335854244-250528-1001010918076558&time=1513252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-FBkIIja%2FXeUsGOWPNFJitgpDgtM%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=8068033678849065101&dp-callid=0&size=c710_u400&quality=100&vuk=-&ft=video)

![图四](https://thumbnail0.baidupcs.com/thumbnail/4a0e8d81dcc3477772a91f012bc1b0a1?fid=1335854244-250528-789284151977961&time=1513252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-gqTXIh2dcryKC2JdxagtBxREKd0%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=8068073223942287696&dp-callid=0&size=c710_u400&quality=100&vuk=-&ft=video)

![图五](https://thumbnail0.baidupcs.com/thumbnail/4e187135d92b102627da5c6efff785d9?fid=1335854244-250528-675476897580897&time=1513252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-pm2xn62Qd5D1sru7ExvR5E5q6aQ%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=8068083517568459482&dp-callid=0&size=c710_u400&quality=100&vuk=-&ft=video)

![图六](https://thumbnail0.baidupcs.com/thumbnail/70a125fea8daf3698e62d3957195dee9?fid=1335854244-250528-246148296011746&time=1513252800&rt=sh&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-BpfdBnRN9pQAjzNz%2B%2Bs1jDWxUSg%3D&expires=8h&chkv=0&chkbd=0&chkpc=&dp-logid=8068092394804843965&dp-callid=0&size=c710_u400&quality=100&vuk=-&ft=video)


## 功能简介
1.用户邮箱注册，登入登出，更改邮箱账户等。
2.用户间关注、取关，设置个人信息、头像等。
3.发布修改博文（markdown），发布评论，评论回复。
4.协管员管理评论（屏蔽、删除）。
5.管理员上天入地为所欲为。


## 环境搭建（以MacOS,Ubuntu16.04为例，centOS6.7也亲测有效，在此不举例了)
#### 1.创建virtualenv
检查系统是否安装virtualenv:
$virtualenv --version

若结果报错：
$sudo easy_install virtualenv

#### 2.下载Github代码
$git clone https://github.com/zyiwei/ywblog.git

#### 在ywblog文件夹中创建虚拟环境
进入下载的文件目录:
$cd ywblog
或$cd ywblog_master

将创建的虚拟环境命名为venv:
$virtualenv venv

激活虚拟环境:
$source venv/bin/activate

#### 4.配置虚拟环境
安装依赖：
(venv)$pip install -r requirements/dev.txt

(配置邮箱用户、管理员自动识别邮箱及服务器，若想直接试用网站默认账户，可跳过此步骤至第五步骤）：
(venv)$export MAIL_USERNAME=<你的邮箱>

(venv)$export MAIL_PASSWORD=<邮箱服务器密码>

(venv)$export FLASKY_ADMIN=<管理员邮箱(可以填你的邮箱)>

(venv)$export FLASKY_MAIL_SENDER=<服务器发送邮件邮箱>

#### 5.网站初始账户
#####（1)管理员账户：
    邮箱：admin@example.com 密码：admin
##### (2)协管员账户(3个)：
    邮箱：mod1@example.com 密码：mod1
    邮箱：mod2@example.com 密码：mod2
    邮箱：mod3@example.com 密码：mod3

#### 6.运行程序
(venv)$python manage.py runserver

#### 7.打开浏览器，前往地址http://127.0.0.1:5000/

#### 注：
若想试验更多功能，在数据库中生成虚用户和虚博文对象，如下：
(venv)$python manage.py shell
后在shell命令行下输入：


>>>User.generate_fake(100)

>>>Post.generate_fake(100)

>>>exit()

这样，就人工向数据库中添加了100个虚拟用户和100个虚拟文章，打开浏览器看看吧！

