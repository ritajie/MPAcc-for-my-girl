import requests
import xlwt
import os
from bs4 import BeautifulSoup as Bea
import json
import time


# 获取所有学校的主页
def colleges_url_from_web():
    url = 'http://yuanxiao.mpacc.cc/index.php?m=content&c=request&a=public_ajax_lists&page='
    for page in range(1, 28):
        res = requests.get(url+str(page))
        res = json.loads(res.text)
        res.pop('pages')
        for each_college in res.values():
            yield 'http://yuanxiao.mpacc.cc'+each_college.get('url')

# 从文件中获取所有学校的url
def colleges_url():
    with open('colleges_url') as file:
        for line in file.readlines():
            yield line.strip()


# 从文件中读取html
def colleges_htmls():
    for file_name in list(os.walk('colleges_htmls'))[0][2]:
        file_path = 'colleges_htmls/'+file_name
        with open(file_path) as file:
            html = file.read()
            yield html

# 解析一个html学校主页
def parser_html(html):
    ans = dict()
    soup = Bea(html, 'html.parser')
    tables = soup.select('table table')
    # 0.基本信息
    ans['大学名称'] = soup.select('.div0 h3')[0].text.strip()
    ans['所在地区'] = soup.select('.div2')[0].text.replace(' ', '').strip().split('\n')[0][5:]
    # 1.学费
    ans['学费'] = dict()
    for tr in tables[0].select('tr')[1:]:
        year = tr.select('td')[0].text.strip().strip('年')
        money = tr.select('td')[1].text.strip()
        ans['学费'][year] = money
    # 2.历年招生数据
    ans['历年招生数据'] = dict()
    for tr in tables[1].select('tr')[1:]:
        year = tr.select('td')[0].text.strip().strip('年')
        data = tr.select('td')[1].text.strip()
        ans['历年招生数据'][year] = data
    # 3.网报数据
    ans['网报数据'] = dict()
    for tr in tables[2].select('tr')[1:]:
        year = tr.select('td')[0].text.strip().strip('年')
        data = tr.select('td')[1].text.strip()
        # ans['网报数据'][year] = data
        ans['网报数据']['2015'] = data
    # 4.历年分数线
    ans['历年分数线'] = dict()
    for tr in tables[3].select('tr')[1:]:
        year = tr.select('td')[0].text.strip().strip('年')
        data = tr.select('td')[1].text.strip()
        ans['历年分数线'][year] = data
    return ans


# 写入xls
if __name__ == '__main__':
    pattern = xlwt.Pattern()
    book = xlwt.Workbook()
    sheet = book.add_sheet('数据来源mpacc.cc')
    # 第一行目录
    catalogue = [
        '大学名称',
        '所在地区',
        '2018招生',
        '2017招生',
        '2016招生',
        '2015报名人数',
        '2018分数线',
        '2017分数线',
        '2016分数线',
    ]
    # 第一行
    for index,name in enumerate(catalogue):
        sheet.write(0, index, name)
    # 后面的每一行
    line_index = 1
    for html in colleges_htmls():
        print(f'line: {line_index}')
        data = parser_html(html)
        # 0.大学名称
        sheet.write(line_index, 0, data['大学名称'])
        # 1.所在地区
        sheet.write(line_index, 1, data['所在地区'])

        # 2.2018招生
        sheet.write(line_index, 2, data['历年招生数据'].get('2018'))
        # 3.2017招生
        sheet.write(line_index, 3, data['历年招生数据'].get('2017'))
        # 4.2016招生
        sheet.write(line_index, 4, data['历年招生数据'].get('2016'))

        # 5.2015网报数据
        # print(data['网报数据'].get('2015'))
        sheet.write(line_index, 5, data['网报数据'].get('2015'))

        # 6.2018招生
        sheet.write(line_index, 6, data['历年分数线'].get('2018'))
        # 7.2017招生
        sheet.write(line_index, 7, data['历年分数线'].get('2017'))
        # 8.2016招生
        sheet.write(line_index, 8, data['历年分数线'].get('2016'))

        line_index += 1

    book.save('/Users/deer/Desktop/xxx.xls')
    print('ok')









