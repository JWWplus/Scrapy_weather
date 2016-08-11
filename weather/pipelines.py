# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 这个类对返回的item进行筛选
import MySQLdb


class WeatherPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        # 创建mysql连接对象，按照自己的设置修改
        conn = MySQLdb.connect(host='localhost', user='root', passwd='jww930729', port=3306, charset='utf8')
        # 该对象有一个方法可用来执行命令
        cur = conn.cursor()

        cur.execute('create database if not exists weather ')
        conn.select_db('weather')

        cur.execute('show tables;')
        # 接受全部返回结果行
        tables = cur.fetchall()
        findtables = False

        for table in tables:
            if 'localweather' in table:
                findtables = True

        if not findtables:
            cur.execute('''
        		create table if not exists weather.localweather (
        		`id` int not null auto_increment,
        		`日期` varchar(8) not null,
        		`日间天气` varchar(20) not null,
        		`日间温度` varchar(8) not null,
        		`夜间天气` varchar(20) not null,
        		`夜间温度` varchar(8) not null,
        		primary key(`id`)) DEFAULT CHARSET = utf8;
        		''')
        with open('wea.txt', 'w+') as f:
            city = item['city'][0].encode('utf-8')
            f.write('city:' + str(city) + '\n\n')

            date = item['date']
            desc = item['dayDesc']

            # 切片取早晚天气状态
            daydesc = desc[1::2]
            nightdesc = desc[0::2]

            daytemp = item['dayTemp']
            # zip函数使用方法可自行百度
            weaitem = zip(date, daydesc, nightdesc, daytemp)

            for i in range(len(weaitem)):
                item = weaitem[i]

                d = item[0]
                dd = item[1]
                nd = item[2]
                ta = item[3].split('/')
                dt = ta[0]
                nt = ta[1]
                # 这里注意所有的都要用utf-8编码
                txt = 'date :{0}\t\tday:{1}({2})\t\tnight:{3}({4}))\n\n'.format(
                    d,
                    dd.encode('utf-8'),
                    dt.encode('utf-8'),
                    nd.encode('utf-8'),
                    nt.encode('utf-8')
                )
                f.write(txt)
                value = [d, dd.encode('utf-8'), dt.encode('utf-8'), nd.encode('utf-8'), nt.encode('utf-8')]
                cur.execute("insert into localweather (日期,日间天气,日间温度,夜间天气,夜间温度) values (%s,%s,%s,%s,%s)",
                            value)
                # 一定要提交
                conn.commit()
            cur.close()
            conn.close()
        return item
