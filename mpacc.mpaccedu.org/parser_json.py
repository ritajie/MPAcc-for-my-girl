import json
import xlwt


def read_json(path='info.json'):
    with open(path) as file:
        for each_college in json.loads(file.readline()):
            yield each_college


if __name__ == '__main__':
    pattern = xlwt.Pattern()
    book = xlwt.Workbook()
    sheet = book.add_sheet('路志远精心整理！')

    # 第一行目录
    catalogue = [
        '学校名称', 
        '所在地区', 

        '招生人数',
        '2018分数线',
        '2017分数线',
        '2016分数线',
        '2015分数线',
        '2014分数线',
        '2013分数线',
        # '网报数据',
        '2018招生人数',
        '2017招生人数',
        '2016招生人数',
        '2015招生人数',
        '2014招生人数',
        '2013招生人数',

        '院校性质', 
        '分数线类别', 
        '官方网址',
        'QQ交流群', 
        '项目类别',
        '学制',
        '学费',
        'url'
    ]
    for index,name in enumerate(catalogue):
        sheet.write(0, index, name)

    # 接下来的各个学校
    line_index = 0
    for each_college in read_json():
        line_index += 1
        for col_index,name in enumerate(catalogue):
            # 1.学校属性
            if type(each_college.get(name)) == str:
                sheet.write(line_index, col_index, each_college.get(name))
                continue
            # 2.简单属性
            if name in each_college['招生信息']:
                sheet.write(line_index, col_index, each_college['招生信息'].get(name))
                continue
            # 3.各年分数线
            if '分数线' in name:
                sheet.write(line_index, col_index, each_college['招生信息']['历年分数线'].get(name[:-3]+'年'))
                continue
            # 4.历年招生数据
            if '招生人数' in name:
                sheet.write(line_index, col_index, each_college['招生信息']['历年招生数据'].get(name[:-4]+'年'))
                continue

    book.save('info.xls')


