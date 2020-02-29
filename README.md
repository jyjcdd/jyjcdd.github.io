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

    pip install xlwt xlrd xlutils docx

如果电脑中同时存在Python 2.x和3.x 则将上述代码改为：

    pip3 install xlwt xlrd xlutils docx


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