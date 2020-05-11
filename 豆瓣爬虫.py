'''
*爬 取 豆 瓣 的 top250电影 榜单
*爬 取 的 文 件 保 存 在 用 户 c盘下主目录
文件目录名为 ‘苏炜迪爬虫文件’

程序运行时间约三分钟（在本机，不同平台可能有差异）
'''

import re
import requests
from os import mkdir

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}
base_url = 'https://movie.douban.com/top250?start={}&filter='
base_catelog = 'C:\苏炜迪_豆瓣爬虫文件\ '
mkdir(base_catelog)
num = 0
for i in range(10):
    page_url = base_url.format(num)
    response = requests.get(page_url, headers=headers)
    title_1 = re.findall('<em class="">(.*?)</em>.*?', response.text)  # 数字文件目录名
    title_2 = re.findall('img width="100" alt="(.*?)" src="', response.text)  # 文字文件目录名
    title = ['NO.' + title_1[i1] + ' ' + title_2[i1] for i1 in range(25)]  # 文件名合体
    son_url = re.findall('<div class="info">.*?<a href="(.*?)" class="">',
                         response.text, re.S)  # 找到单独的url
    for i2 in range(25):
        son_catelog = base_catelog + title[i2]
        mkdir(son_catelog)
        # 在此导入每页电影海报信息与文本信息
        page_response = requests.get(son_url[i2], headers=headers)
        pic_url_base = re.findall('"image": "(.*?)"', page_response.text, re.S)
        pic_url = pic_url_base[0]
        pic_response = requests.get(pic_url, headers=headers)
        pic_catelog = son_catelog + "\电影海报.jpg"

        with open(pic_catelog, 'wb') as f:
            f.write(pic_response.content)
        f.close()
        word_catelog = son_catelog + "\电影简介.txt"
        # word_re_title = re.findall()
        word_re_intro = re.findall(
            '<div class="related-info" style="margin-bottom:-10px;">.*? <span property="v:summary.*?>\n          (.*?)</span>',
            page_response.text,
            re.S)
        title_re = re.findall('<head>.*?<title>\n        (.*?)\n</title>', page_response.text, re.S)  # 标题的正则
        director_re = re.findall(
            '<span >.*?导演</span>:.*?directedBy">(.*?)</a>', page_response.text,
            re.S)  # 导演正则
        editor_re = re.findall('>编剧<.*?">(.*?)</a>', page_response.text, re.S)
        actor_re = re.findall('rel="v:starring">(.*?)</a>', page_response.text, re.S)
        time_re = re.findall('"v:runtime".*?">(.*?)</span>', page_response.text, re.S)
        another_name = re.findall('">又名:</span> (.*?)<br/>', page_response.text, re.S)
        kind_re = re.findall('"v:genre">(.*?)</span>', page_response.text, re.S)
        with open(word_catelog, 'w', encoding='utf-8') as  f:
            f.write("导演：" + director_re[0] + "\n\n")
            f.write("主演：\n\n")
            for i4 in range(len(actor_re)):
                f.write(actor_re[i4] + " ")
            f.write("类型：" + kind_re[0] + "\n\n")
            f.write("片长：" + time_re[0] + "\n\n")
            f.write("电影简介:\n")
            f.write(word_re_intro[0])
        f.close()
    num += 25
