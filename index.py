'''
从http://mpacc.mpaccedu.org/获取所有学校的会计专硕招生信息
结果以json格式保存在info.json文件中

作者：路小鹿
日期：2019年9月19日
'''
import requests
from bs4 import BeautifulSoup as Bea    
import json

# 获取所有学校的主页url
def colleges_url():
    url = 'http://mpacc.mpaccedu.org/'
    res = requests.get(url)
    res.encoding='utf-8'
    # print(res.text)
    soup = Bea(res.text, 'html.parser')
    for each_college_a in soup.select('.rf_cont ul li a'):
        href = each_college_a.attrs.get('href')
        yield 'http://mpacc.mpaccedu.org'+href

# 提取单个学校的信息
def parser_page(url):
    ans = dict()
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = Bea(res.text, 'html.parser')
    ans['学校名称'] = soup.select('dd h4 a')[0].text
    ans['所在地区'] = soup.select('.a-detail li')[0].text.strip()[5:]
    ans['院校性质'] = soup.select('.a-detail li span')[0].text[5:]
    ans['分数线类别'] = soup.select('.a-detail li span')[1].text[6:].strip()
    ans['院校地址'] = soup.select('.a-detail li')[2].text.strip()[5:].strip()
    ans['官方网址'] = soup.select('.a-detail li')[3].text.strip()[5:]
    ans['QQ交流群'] = soup.select('.a-detail li')[4].text.split()[0][5:]
    # ans['项目简介'] = 
    ans['招生信息'] = dict()
    ans['招生信息']['项目类别'] = soup.select('.pro-3 td')[:10][1].text.strip()
    ans['招生信息']['招生人数'] = soup.select('.pro-3 td')[:10][5].text.strip()
    ans['招生信息']['学费'] = soup.select('.pro-3 td')[:10][7].text.strip()
    ans['招生信息']['学制'] = soup.select('.pro-3 td')[:10][3].text.strip()
    # ans['招生信息']['奖学金'] = soup.select('.pro-3 td')[:10][9].text.strip()
    all_td_text = [i.text.strip() for i in soup.select('.pro-3 td')]
    # 分数线
    ans['招生信息']['历年分数线'] = dict()
    the_table = soup.select('.pro-3 td')[all_td_text.index('历年分数线：')+1].select('table')[0]
    for each_line in the_table.select('tr')[1:]:
        if len(each_line.select('td')) != 2:
            continue
        year = each_line.select('td')[0].text
        score_line = each_line.select('td')[1].text
        ans['招生信息']['历年分数线'][year] = score_line
    # 网报数据
    ans['招生信息']['网报数据'] = dict()
    if soup.select('.pro-3 td')[all_td_text.index('网报数据：')+1].select('table').__len__() == 1:
        the_table = soup.select('.pro-3 td')[all_td_text.index('网报数据：')+1].select('table')[0]
        for each_line in the_table.select('tr')[1:]:
            year = each_line.select('td')[0].text
            count = each_line.select('td')[1].text
            ans['招生信息']['网报数据'][year] = count
    # 历年招生数据
    ans['招生信息']['历年招生数据'] = dict()
    the_table = soup.select('.pro-3 td')[all_td_text.index('历年招生数据：')+1].select('table')[0]
    for each_line in the_table.select('tr')[1:]:
        year = each_line.select('td')[0].text
        count = each_line.select('td')[1].text
        ans['招生信息']['历年招生数据'][year] = count
    ans['url'] = url
    return ans


def print_dict(dic, count_t=0):
    for key,value in dic.items():
        if type(value) == dict:
            print(key)
            print('\t'*count_t, '-'*20)
            print_dict(value, count_t+1)
        else:
            print('\t'*count_t, key, '\t', value)


# parser_page('http://mpacc.mpaccedu.org/html/2015/jiangsu_0416/45.html')
if __name__ == '__main__':
    # 解析所有学校并写入json文件
    ans = list()
    for url in colleges_url():
        print(f'{len(ans)} 解析{url}...')
        ans.append(parser_page(url))
        print('ok')
    with open('info.json', 'w') as file:
        file.write(json.dumps(ans))

    print('写入成功！') 

