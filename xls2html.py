import xlrd


class Xls2HTML:
    def __init__(self, xlsfile, year, month, filetype):
        self.xlsfile = xlsfile
        self.year = year
        self.month = month
        self.type_text = {
            'hwzs': '海外之声',
            'xqxz': '消歧小组',
            'jydd': '就业大队'
        }[filetype]
        self.htmlfile = open(f'view/{year}/{filetype}/{month}.html', 'w')
        self.headCol = ''

    def xls_template_init(self):
        self.htmlfile.write('<!DOCTYPE html>')
        self.htmlfile.write('<html>')
        self.htmlfile.write('<head>')
        self.htmlfile.write('<meta charset="utf-8" />')
        self.htmlfile.write(f'<title>{self.year}{self.month}微博爬虫数据</title>')
        self.htmlfile.write(
            '<link rel="stylesheet" type="text/css" href="../../index.css" />')
        self.htmlfile.write('</head>')
        self.htmlfile.write("<body class='xls-list'>")
        self.htmlfile.write(
            f'<h2>{self.year}年{self.month}月{self.type_text}微博爬虫数据</h2>')
        self.htmlfile.write("<ol>")

    def xls_template_close(self):
        self.htmlfile.write("</ol>")
        self.htmlfile.write("</body>")
        self.htmlfile.write("</html>")
        self.htmlfile.close()

    def xls_template(self, rowVale, ncols):
        self.htmlfile.write("<li>")

        for colNum in range(ncols):
            if colNum > 0:
                if colNum == 1 or colNum == 6:
                    self.htmlfile.write(
                        f'<p><label>{self.headCol[colNum]}:<b>{rowVale[colNum]}</b></label>')
                elif colNum == 2 or colNum == 7 or colNum == 8:
                    self.htmlfile.write(
                        f'<label>{self.headCol[colNum]}:<b>{rowVale[colNum]}</b></label>')
                elif colNum == 3:
                    self.htmlfile.write(
                        f'<label>{self.headCol[colNum]}:</label><a href="{rowVale[colNum]}">原微博链接</a></p>')
                elif colNum == 9:
                    self.htmlfile.write(
                        f'<label>{self.headCol[colNum]}:<b>{rowVale[colNum]}</b></label></p>')
                elif colNum == 4 or colNum == 5:
                    self.htmlfile.write(
                        f'<p><label>{self.headCol[colNum]}:</label>{str(rowVale[colNum])}</p>')
                elif colNum == 10:
                    self.htmlfile.write(f'<p>{self.headCol[colNum]}:<br/>')
                    comment = str(rowVale[colNum]).replace('\n', '<br/>')
                    self.htmlfile.write(f'{comment}</p>')

        self.htmlfile.write("</li>")

    def xls2html(self):
        # 读取excel文件
        data = xlrd.open_workbook(self.xlsfile)
        table = data.sheet_by_index(0)

        # 对html文件进行初始化
        self.xls_template_init()

        # 遍历excel文件中的数据
        for rowNum in range(table.nrows):
            rowVale = table.row_values(rowNum)
            # 将表头行保存下来
            if rowNum == 0:
                self.headCol = rowVale
            else:
                self.xls_template(rowVale, table.ncols)

        # 保存html文件
        self.xls_template_close()


# 第一个参数：需要进行转换的文件名
# 第二个参数：数据对应的年份
# 第三个参数：数据对应的月份
xh = Xls2HTML('data/2020/1月/海外之声微博2020年01月数据.xls', '2020', '01', 'hwzs')
xh.xls2html()
