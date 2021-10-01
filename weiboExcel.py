# 代码运行环境：
# Python 3.x
# 代码运行所需库文件：
# selenium + xlwt + xlrd + xlutils

from selenium import webdriver
import time
import os
import re
import sys
import datetime
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy


class Weibo_spider:
    # Excel文件的标头
    excelTitle = {
        # 就业大队
        'jydd': '序号 发布日期 发布时间 微博链接 内容 阅读量 转发 评论 点赞 评论内容',
        # 消歧小组
        'xqxz': '序号 发布日期 发布时间 微博链接 招录单位 招聘岗位 岗位要求 招聘链接 阅读量 转发 评论 点赞 评论内容',
        # 海外之声 （新增 来源 翻译
        'hwzs': '序号 发布日期 发布时间 微博链接 国家 内容 来源 翻译 阅读量 转发 评论 点赞 评论内容',
        # 举报回复
        'jbhf': '序号 发布日期 发布时间 微博链接 回复主体 回复内容 前情链接 招录单位 招聘岗位 岗位要求 全部内容 阅读量 转发 评论 点赞 评论内容'
    }
    # Excel文件名
    excelName = {
        'jydd': '就业大队',
        'xqxz': '消歧小组',
        'hwzs': '海外之声',
        'jbhf': '举报回复'
    }

    def __init__(self, excel_type, year, month, page, username, password, instance):
        page = int(page)
        year = str(year)
        if len(month) == 1:
            month = '0' + str(month)

        # 账户信息
        self.username = username
        self.password = password
        # 页面信息
        if excel_type == 'jbhf':
            self.homeUrl = 'https://weibo.com/u/5327831786/home'
            self.baseUrl = 'https://weibo.com/5327831786/profile?is_all=1&is_search=1&key_word=%23举报回复%23'
        elif excel_type == 'hwzs':
            #self.homeUrl = 'https://weibo.com/u/5327831786/home'
            #self.baseUrl = f'https://weibo.com/5327831786/profile?is_all=1&stat_date={year}{month}'
            #煎茶小队
            self.homeUrl = 'https://weibo.com/u/7403993086/home'
            self.baseUrl = f'https://weibo.com/7403993086/profile?is_all=1&stat_date={year}{month}'
        else:
            self.homeUrl = 'https://weibo.com/u/5327831786/home'
            self.baseUrl = f'https://weibo.com/5327831786/profile?is_all=1&stat_date={year}{month}'

        self.totalPageNum = page
        # 内容关键字
        if excel_type == 'xqxz':
            self.keyWord = '消歧投稿'
        elif excel_type == 'hwzs':
            self.keyWord = f'海外之声 {year}.{month}'
        elif excel_type == 'jydd' or excel_type == 'jbhf':
            self.keyWord = ''
        #elif excel_type == 'jbhf':
        #   self.keyWord = '#举报回复#'

        # 爬虫
        self.driver = webdriver.Chrome()
        self.cur_data = []
        self.data_list = []
        # Excel表信息
        self.excelType = excel_type
        self.excelTitle = Weibo_spider.excelTitle[excel_type]
        self.excelName = f'{Weibo_spider.excelName[excel_type]}微博{year}年{month}月数据'
        self.file = None
        self.rowNum = 1
        self.initExcel()

    # 初始化Excel表
    def initExcel(self):
        try:
            # 当前目录下是否有num.txt和相应excel文件
            file = open_workbook(f'{self.excelName}.xls')
            self.operate_file(f'{self.excelName}num.txt', 'r')
            print('txt & excel文件都存在')
            # 获取已有行的个数
            rowNum = file.sheets()[0].nrows
            # 开始追加数据的行数
            self.rowNum = rowNum
            # 将xlrd的对象转化为xlwt的对象
            self.file = copy(file)
            self.sheet = self.file.get_sheet(0)
        except:
            print('创建文件')
            self.file = Workbook()
            self.sheet = self.file.add_sheet('Sheet 1')
            # 写入表头
            excel_title_list = self.excelTitle.split(' ')
            for index in range(len(excel_title_list)):
                self.sheet.write(0, index, excel_title_list[index])

            # 创建excel文件
            self.file.save(f'{self.excelName}.xls')

            # 创建num.txt并写入当前页码
            self.operate_file(f'{self.excelName}num.txt', 'w')

    def operate_file(self, filename, action):
        with open(filename, action) as f:
            # 写入页码记录
            if action == 'w':
                f.write(str(self.totalPageNum))
            elif action == 'r':
                # 将要抓的页码赋值
                self.totalPageNum = int(f.read())

    # 登录微博
    def login(self):
        # 访问微博首页
        self.driver.implicitly_wait(10)
        self.driver.get('https://weibo.com')
        time.sleep(5)
        # 登录账号
        user_input = self.driver.find_element_by_id('loginname')
        user_input.send_keys(self.username)
        psd_input = self.driver.find_element_by_css_selector(
            '.password .W_input')
        psd_input.send_keys(self.password)
        # 点击登录按钮
        submit_btn = self.driver.find_element_by_css_selector(
            '.W_btn_a.btn_32px')
        time.sleep(1)
        submit_btn.click()
        try:
            vail_input = self.driver.find_element_by_css_selector(
                '[node-type="verifycode"]')
            vail_input.send_keys('')
            print('请输入验证码...')
            time.sleep(3)
            while True:
                if self.driver.current_url != self.homeUrl:
                    time.sleep(1)
                else:
                    break
        except:
            # 等待网页加载
            time.sleep(3)

    # 将滚动条移动到页面的底部
    def scroll_page(self):
        # 执行js代码
        scroll_js = "window.scrollTo(0, document.body.scrollHeight + 100);"
        scroll_height_js = "return document.body.scrollHeight;"

        # 微博pc端每页需要两次滚动加载完所有当页数据
        while True:
            # 获取滚动之前的高度
            prev_height = self.driver.execute_script(scroll_height_js)
            # 将滚动条置底
            self.driver.execute_script(scroll_js)
            time.sleep(3)
            # 获取滚动之后的高度
            next_height = self.driver.execute_script(scroll_height_js)
            try:
                # 比较滚动前后高度 若已经到底最退出循环
                pre_text = self.driver.find_element_by_css_selector(
                    '.page.prev').text
                if pre_text == '上一页' or pre_text == '上一頁':
                    break
            except:
                try:
                    next_text = self.driver.find_element_by_css_selector(
                        '.page.next').text
                    if next_text == '下一页' or next_text == '下一頁':
                        break
                except:
                    pass

        # 等待滚动完成
        time.sleep(1)
        # 回到顶部
        self.driver.execute_script('window.scrollTo(0, 0);')
        time.sleep(1)

    # 访问当前页码的网页
    def visit_current_page(self, page):
        self.driver.implicitly_wait(10)
        current_url = self.baseUrl + '&page=' + str(page)
        self.driver.get(current_url)
        time.sleep(3)
        for i in range(2):
            if self.driver.current_url == current_url:
                break

            self.driver.get(current_url)
            time.sleep(3)

    # 获取日期和时间 & 微博链接
    def __spider_date(self, ele):
        ele_time = ele.find_element_by_css_selector(
            '.WB_from [node-type="feed_list_item_date"]')
        date_list = ele_time.text.split(' ')
        # 尝试获取日期和时间，若报错，则代表是 今天且是一小时内
        try:
            if date_list[0] == '今天':
                today = datetime.date.today()
                self.cur_data.append(f'{today.month}月{today.day}日')
            else:
                self.cur_data.append(date_list[0])  # 日期

            self.cur_data.append(date_list[1])  # 时间
        except:
            today = datetime.date.today()
            self.cur_data.append(f'{today.month}月{today.day}日')  # 日期
            mins = int(date_list[0].split('分')[0])
            self.cur_data.append((
                datetime.datetime.now() - datetime.timedelta(minutes=mins)
            ).strftime('%H:%M'))  # 时间

        # 获取微博链接
        full_text_href = ele_time.get_attribute('href')
        self.cur_data.append(full_text_href)

    # 展开全文
    def __spider_full_text(self, ele):
        # 是否有展开全文
        has_full_text = False
        has_full_text_num = 3
        while has_full_text_num > 0 and not has_full_text:
            try:
                full_text_ele = ele.find_element_by_css_selector(
                    '.WB_text_opt[action-type="fl_unfold"]')
                has_full_text = True
                # 展开全文
                full_text_click_num = 5
                full_text_need_click = True
                while full_text_click_num > 0 and full_text_need_click:
                    try:
                        full_text_ele.click()
                        print('展开全文!')
                        full_text_need_click = False

                    except Exception:
                        full_text_click_num -= 1
                        # 曝光，以使得当前链接可点击
                        self.driver.execute_script(
                            'window.scrollTo(0, window.scrollY + 50);')
                        time.sleep(1)

            except:
                has_full_text_num -= 1
                # 曝光，以使得当前链接可点击
                self.driver.execute_script(
                    'window.scrollTo(0, window.scrollY + 50);')
                time.sleep(1)

            if not has_full_text:
                print('无展开全文')

        time.sleep(3)

    # 抓取文案内容
    def __spider_content(self, ele):
        # 展开全文
        text_ele = ele.find_element_by_css_selector('.WB_text')
        self.__spider_full_text(text_ele)
        try:
            # 展开全文
            full_text_ele = ele.find_element_by_css_selector(
                '[node-type="feed_list_content_full"]')
            full_text = full_text_ele.text[:-5]  # 去除收起全文
        except:
            # 无展开全文
            full_text_ele = ele.find_element_by_css_selector(
                '[node-type="feed_list_content"]')
            full_text = full_text_ele.text

        if self.excelType == 'xqxz':
            try:
                regObj = re.search('举报(.*?)。', full_text)
                # 按照中文逗号分隔信息
                job_text_list = regObj.group(1).split('，')
                for i in range(3):
                    job_text = job_text_list[i]
                    if i == 0:
                        self.cur_data.append(job_text)
                    else:
                        # 把文本中的 招聘|要求 去掉
                        job_text = job_text[2:]
                        self.cur_data.append(job_text)
                try:
                    full_text.index('招聘链接')
                    self.cur_data.append('有')
                except:
                    self.cur_data.append('无')
            except:
                for i in range(4):
                    self.cur_data.append('无')

        elif self.excelType == 'hwzs':
            try:
                full_text_list = full_text.split('【')[1]
                full_text_list = full_text_list.split('】')
                self.cur_data.append(full_text_list[0])
                # 来源 翻译
                full_text_blankLine = full_text_list[1].split('\n\n')
                last_blankLine = full_text_blankLine[-1]
                if last_blankLine[0] == '（' and last_blankLine[-1] == '）':
                    self.cur_data.append('\n\n'.join(full_text_blankLine[0:-1]))
                    # 去除 （）
                    last_blankLine = last_blankLine[1:-1]
                    # 分隔来源和翻译
                    full_text_originAndTrans = last_blankLine.split('；')
                    for item in full_text_originAndTrans:
                        name, con = item.split('：')
                        self.cur_data.append(con.replace('\n', '').replace('\r', ''))
                else:
                    self.cur_data.append(full_text_list[1])
                    self.cur_data.append('无')
                    self.cur_data.append('无')
            except:
                self.cur_data.append('转发 无内容')

        elif self.excelType == 'jydd':
            try:
                expand_ele = ele.find_element_by_css_selector('.WB_expand')
                expand_ele_title = expand_ele.find_element_by_css_selector(
                    '.WB_info a').text
                expand_ele_text = expand_ele.find_element_by_css_selector(
                    '.WB_text')
                self.__spider_full_text(expand_ele_text)
                try:
                    # 展开全文
                    expand_full_text_ele = expand_ele.find_element_by_css_selector(
                        '[node-type="feed_list_reason_full"]')
                    expand_full_text = expand_full_text_ele.text[:-5]  # 去除收起全文
                except:
                    # 无展开全文
                    expand_full_text_ele = expand_ele.find_element_by_css_selector(
                        '[node-type="feed_list_reason"]')
                    expand_full_text = expand_full_text_ele.text

                full_text = full_text + '\n' + expand_ele_title + '\n' + expand_full_text
                self.cur_data.append(full_text)

            except:
                self.cur_data.append(full_text)
        
        elif self.excelType == 'jbhf':
            try:
                #回复主体&回复内容
                full_text_list = full_text.split('【')[1].split('】')[0].split('：')
                self.cur_data.append(full_text_list[0])
                self.cur_data.append(full_text_list[1])
                part_text = full_text.split('前情')[1]
                try:
                    #前情链接 待改
                    try:
                        pre_link = full_text_ele.find_element_by_css_selector("a[title='就业性别歧视监察大队']")
                    except:
                        pre_link = full_text_ele.find_element_by_css_selector('a[title][href]')
                    #print(pre_link)
                    #pre_link = re.search('前情：',full_text).split('\n')[0]
                    pre_href = pre_link.get_attribute('href')
                    #print(pre_href)
                    self.cur_data.append(pre_href)
                    try:
                        #单位|岗位|要求
                        regObj = re.search('举报(.*?)。', part_text)
                        # 按照中文逗号分隔信息
                        job_text_list = regObj.group(1).split('，')
                        for i in range(3):
                            job_text = job_text_list[i]
                            if i == 1:
                                 # 把文本中的 招聘 去掉
                                job_text = job_text[2:]
                                self.cur_data.append(job_text)
                            else:
                                # 把文本中的 招聘|要求 去掉
                                #job_text = job_text[2:]
                                self.cur_data.append(job_text)
                        self.cur_data.append(full_text)
                    except:
                        for i in range(3):
                            self.cur_data.append('')
                        self.cur_data.append(full_text)
                except:
                    for i in range(4):
                        self.cur_data.append('')
                    print("爬取前情链接失败！！")
                    self.cur_data.append(full_text)
            except:
                for i in range(6):
                    self.cur_data.append('')
                self.cur_data.append(full_text)



    # 获取点赞数等
    def __spider_evaluations(self, ele):
        data_line = ele.find_element_by_css_selector('.WB_row_line')
        data_lis = data_line.find_elements_by_css_selector('li')
        num = 0

        # 获取阅读数
        self.__spider_read_num(data_lis[num])
        num += 1
        # 仅自己可见时，没有转发
        if len(data_lis) == 3:
            self.cur_data.append('无')
        else:
            # 获取转发数
            self.__spider_evaluations_num(data_lis[num], 'forward')
            num += 1

        # 获取评论数
        has_comment = self.__spider_evaluations_num(data_lis[num], 'comment')
        num += 1
        # 获取点赞数
        self.__spider_evaluations_num(data_lis[num], 'agree')
        # 获取评论
        # 评论一栏 倒数第二项
        if has_comment:
            self.__spider_comment(data_lis[num - 1], ele)
        else:
            self.cur_data.append('无')

    # 获取阅读数
    def __spider_read_num(self, ele):
        try:
            read_num_str = ele.find_element_by_css_selector('i.S_txt2').text
            read_num = read_num_str.split(' ')[1]
        except:
            read_num = '无'

        self.cur_data.append(read_num)

    # 转发数|评论数|点赞数
    def __spider_evaluations_num(self, ele, evaluationsType):
        try:
            evaluations_num = ele.find_element_by_css_selector('em+em').text
        except:
            try:
                evaluations_num = ele.find_element_by_css_selector(
                    '.WB_row_line li .icon_att_like+em').text
            except:
                evaluations_num = '无'

        if evaluations_num == '转发' or evaluations_num == '评论' or evaluations_num == '赞':
            evaluations_num = 0

        self.cur_data.append(evaluations_num)
        # 判断是否需要爬取评论
        if evaluationsType == 'comment':
            if evaluations_num == 0:
                return False
            else:
                return True

    # 获取评论
    def __spider_comment(self, clickEle, ele):
        replays = ''
        need_click = True
        click_num = 5
        while click_num > 0 and need_click:
            try:
                self.driver.execute_script('')
                clickEle.click()
                # 回复评论
                time.sleep(5)
                replay_list = ele.find_elements_by_css_selector(
                    '.repeat_list [node-type="replywrap"]>.WB_text')
                time.sleep(1)
                if len(replay_list) > 0:
                    for replay in replay_list:
                        replays += replay.text
                        replays += '\n'
                else:
                    replays = '无'

                need_click = False

            except Exception:
                click_num -= 1
                # 曝光，以使得当前链接可点击
                self.driver.execute_script(
                    'window.scrollTo(0, window.scrollY + 50);')
                time.sleep(1)

            self.cur_data.append(replays)

    # 将数据写入Excel表
    def __write_excel(self):
        # 写入微博数据
        # 微博倒叙排序，此处再倒叙一次
        index = len(self.data_list) - 1
        while index >= 0:
            col = 1
            self.sheet.write(self.rowNum, 0, self.rowNum)
            for item in self.data_list[index]:
                self.sheet.write(self.rowNum, col, item)
                col += 1

            self.rowNum += 1
            index -= 1

        self.file.save(f'{self.excelName}.xls')
        self.operate_file(f'{self.excelName}num.txt', 'w')
        # 清空当页数据列表
        self.data_list = []

    # 抓取数据
    def spider_data(self):
        # 登录
        self.login()
        time.sleep(5)
        while self.totalPageNum >= 1:
            print('page:', self.totalPageNum)
            # 访问网页
            self.visit_current_page(self.totalPageNum)
            # 保证循环继续到下一页
            self.totalPageNum -= 1
            # 滚动
            self.scroll_page()
            # 抓取数据
            elements = self.driver.find_elements_by_css_selector(
                '.WB_cardwrap.WB_feed_type')
            for ele in elements:
                detail_ele = ele.find_element_by_css_selector(
                    '.WB_feed_detail')
                text_ele = detail_ele.find_element_by_css_selector('.WB_text')
                if self.keyWord in text_ele.text:
                    self.cur_data = []
                    # 抓取时间 & 微博原文链接
                    self.__spider_date(detail_ele)
                    # 抓取文案内容
                    self.__spider_content(detail_ele)
                    # 获取点赞数等
                    self.__spider_evaluations(ele)
                    # 写入数据列表
                    self.data_list.append(self.cur_data)
                    print(f'cur_data:{self.cur_data}')

            print(f'data_list:{self.data_list}')
            # 写入本页数据
            self.__write_excel()

        # 关闭driver
        self.driver.close()
        # 并删除txt文件
        try:
            os.remove(f'{self.excelName}num.txt')
            print('已删除num.txt')
        except:
            print('无num.txt')


# 第一个参数是要抓取数据的对应缩写
# 第二、三个参数是抓取的年份、月份
# 第三个参数是一共的页数（到微博查看）
spider_type = sys.argv[1]
year = sys.argv[2]
month = sys.argv[3]
page = sys.argv[4]
username = sys.argv[5]
password = sys.argv[6]
# 不同的账号主体
# 默认为就业大队，现阶段也可能为 消除家暴
try:
    instance = sys.argv[7]
except:
    instance = ''

ws = Weibo_spider(spider_type, year, month, page, username, password, instance)
ws.spider_data()
print('Done')
