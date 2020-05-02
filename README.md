# 微博爬虫数据
- [微博爬虫数据集合](/summary.html)

## 下载爬虫数据文件

1. 逐级访问data下的文件夹，直到找到你想下载的爬虫数据文件

2. 点击该文件，找到 `Download` 按钮，点击即可下载该文件


# 微博爬虫教程

**如果遇到问题，可以在网上搜索相关提示；若依然无法解决，可到群里@楼楼**

## 配置爬虫运行环境
想要运行爬虫的代码，需要先在电脑上配置好运行环境，最首要的是安装Python:

⚠️安装Python的版本一定要3.x

- [安装Python](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624)

*↑这个链接跳转的是一个Python教程，如果没有接触过Python的小伙伴，可以从这个教程开始学习一下Python的基础语法呀~*

请确保Python已经安装完成，再进行下述操作；是否成功安装的标准在上文链接中可以看到。

接下来，我们安装爬虫所需的库文件：selenium。

打开命令行

 - Window系统：通过快捷键 `Win+R` 打开cmd窗口
 - MacOS系统：[如何在Mac电脑上打开终端](https://zh.wikihow.com/%E5%9C%A8Mac%E7%94%B5%E8%84%91%E4%B8%8A%E6%89%93%E5%BC%80%E7%BB%88%E7%AB%AF)


在命令行中输入以下代码：

    pip install selenium

如果电脑中同时存在Python 2.x和3.x 则将上述代码改为：

    pip3 install selenium

同时，在代码中因为需要将爬取的数据保存到Word及Excel中，因而还需要安装其所依赖的库文件。

依然是在命令行中，输入以下代码：

    pip install xlwt xlrd xlutils python-docx

如果电脑中同时存在Python 2.x和3.x 则将上述代码改为：

    pip3 install xlwt xlrd xlutils python-docx


安装完爬虫依赖的库文件后，我们还需要安装 Chrome驱动：
- [chromedirver下载地址](http://npm.taobao.org/mirrors/chromedriver/)

找到你电脑中chrome对应的版本下载，若非对应版本有一定几率会报错。

chrome的版本可以在chrome 右上角三个点 -> 设置 -> 关于chrome 中查看。

下载完成后，需要将chromedriver放到系统可以找到的路径下，  

如果是**Window**系统，[Windows下配置Chrome WebDriver](https://blog.csdn.net/u013360850/article/details/54962248)

如果是**MacOS**系统，则在命令行中依次输入：

    cd /usr/local/bin

    open .

然后将下载好的chromedriver文件拖入到此目录下。

至此，如果一切进展顺利，我们就成功完成了爬虫运行环境的配置工作。

接下来就是指使小蜘蛛为我们爬取微博数据的时候啦~

## 运行爬虫代码

1. 在浏览器中打开链接

    https://github.com/jyjcdd/jyjcdd.github.io

2. 找到 `Clone or download` 按钮点击，在弹窗中找到 `Download ZIP`，点击下载文件

3. 解压下载的ZIP文件

4. 在命令行中跳转到你解压的爬虫文件中

       cd jyjcdd.github.io-master
       
    Win系统下，[CMD如何切换目录](https://jingyan.baidu.com/article/425e69e6918df1be15fc1695.html)
    
    MacOS系统下，[mac怎么使用终端cd到这个目录下的命令](https://zhidao.baidu.com/question/1240910514944666059.html)

5. 在命令行中输入代码运行爬虫

    ⚠️ 如果你之前没有接触过代码，请先看代码解释！

        python weiboExcel.py jydd 2020 01 6 [uername] [password]
    
    如果电脑中同时存在Python 2.x和3.x 则将上述代码改为：

        python3 weiboExcel.py jydd 2020 01 6 [uername] [password]

    **⚠️ 代码解释：**
    `python weiboExcel.py` 代表用`python`运行`weiboExcel.py`文件

    `jydd` 代表你要抓取的范围，现有范围为: 

        jydd — 就业大队 | xqxz — 消歧小组 | hwzs — 海外之声

    `2020` `01` 代表你要抓取的年份和月份
    
    `6` 代表当前这个月所发微博的页数，需要到微博查看

    `[username] [password]` 是大队的微博登录账号和密码


如果一切进展顺利，爬虫将会开始执行代码，然后爬取微博数据啦~

如果进展不顺利，那就多拜拜雍正让他治一治bug吧~


## 规范化数据
⚠️ 此部分需要下载一款代码编辑器，个人推荐[vscode](https://code.visualstudio.com/)

1. 在`data`目录下找到对应年份，创建你刚刚抓取的数据对应的月份目录
2. 将抓取的数据放到该目录下
3. 在命令行中输入代码运行数据转化页面

    ⚠️ 如果你之前没有接触过代码，请先看代码解释！

        python xls2html.py 2020 01 jydd 就业大队
    
    如果电脑中同时存在Python 2.x和3.x 则将上述代码改为：

        python3 xls2html.py 2020 01 jydd 就业大队

    **⚠️ 代码解释：**
    `python xls2html.py` 代表用`python`运行`xls2html.py`文件

    `jydd` 代表你要转化的文件名缩写，现有缩写与文件名对应为: 

        jydd — 就业大队 | xqxz — 消歧小组 | hwzs — 海外之声

    `就业大队`代表你要转化的文件名

4. 在编辑器中打开`summary.html`文件（编辑器推荐使用[vscode](https://code.visualstudio.com/))

5. 将你刚刚转化生成的文件添加到`summary.html`中，按照格式只需要改动月份，最多再加一个年份，跟你刚刚抓取的数据对应上就好

## 上传爬虫数据
⚠️ 此部分需要学习一些关于GitHub和ssh的知识

Ps：但是别担心，如果你看见这俩词很懵，那你就想想拉💩：蹲坑 -> 用力 -> 擦屁股。它们不过是坑和纸，用来达成你新陈代谢的目的。所以即使你弄不懂它们是啥，也一样可以完成你上传代码的目的。

这里有一篇浅显易懂的[博客](https://www.liaoxuefeng.com/wiki/896043488029600/896954117292416)，如果你感兴趣点开了，可以认真看一下“远程仓库”和“添加远程库”这两节，如果不感兴趣，就照着下面的步骤做就好，我们一样能到达盥洗室。

1. 在浏览器中访问就业大队的仓库地址→[https://github.com/jyjcdd/jyjcdd.github.io](https://github.com/jyjcdd/jyjcdd.github.io)
2. 此时你多半是没有登录的状态，那么接着点击右上角的`Sign In`

此时输入就业大队仓库的账号密码（⚠️ 与楼楼私聊获得）

3. 到此，你得是仓库主人的身份访问就业大队仓库地址，如果不是，请检查上述步骤是否有误
4. 点击`Settings`
5. 在此页面左侧导航栏找到`Deploy keys`狠狠的点击它（只要你的手指别弄疼就行
6. 在这个页面上，你可以很容易看见一个`Add deploy key`按钮，对，点它

OK，我们到这都很顺利，稍微简单的回过头去说一下，这个网站就是`GitHub`，而这个页面里面我们需要添加的key就是`ssh key`，我们怎么添加它呢？它在哪呢？你如果这时有了兴趣，那么这篇[博客](https://www.liaoxuefeng.com/wiki/896043488029600/896954117292416)你完全可以点开看一看👍如果你依然不感兴趣，没关系，咱们接着往下看。

7. 在命令行中，输入以下代码

        ssh-keygen -t rsa -C "youremail@example.com"

    ⚠️将 `youremail@example.com` 替换为你的真实邮箱。
    代码不做解释了，那篇[博客](https://www.liaoxuefeng.com/wiki/896043488029600/896954117292416)里面有，你去看看就知道。

8. 然后一路回车，使用默认值即可
9. 打开`.ssh`文件夹
    - 如果你是MacOS系统，在命令行中输入以下代码
    
        cd ~/.ssh
        open .
    
    - 如果你是Win系统，在文件夹中切换到C盘 -> Users -> Administrator -> .ssh
10. 打开`id_rsa.pub`文件
    - 如果你是MacOS系统，在命令行中输入以下代码

        cat id_rsa.pub

    - 如果你是Win系统，双击`id_rsa.pub`文件

哎呀，费可大劲，终于搞到了，这`id_rsa.pub`文件中的内容就是我们的`ssh key`呀~

11. 将`id_rsa.pub`文件内容拷贝
12. 回到我们刚刚的`Deploy keys`页面里面，将拷贝内容放入`Key`下面的输入框中
13. 给你的`ssh key`任意命名，只要你知道那是你的`key`而不至于被楼楼误删，然后放入到Title下的输入框里面
14. 点击`Allow write access`

啊，让我们暂停几秒钟，享受这即将成功的美妙时刻~

15. 点击`Add Key`

如果不出意外，列表中将会有你的`ssh key`躺在那里。欢呼雀跃，但是别高兴太早，我们只是完成了准备工作...不过还是可以小小开心一下，因为我们完成了一大半了~接下来一鼓作气，搞定它！

回到我们的爬虫项目，在命令行里切到该项目的目录下。

16. 将代码提交到远程仓库，在命令行中输入以下代码



