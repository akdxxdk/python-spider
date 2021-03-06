import random,os
from requests_html import HTMLSession, HTML, AsyncHTMLSession
from pprint import pprint


class DouBanTest:
    def __init__(self,url):
        self.start_url = url  # 实例化url
        self.session = HTMLSession()  # 实例化session
        self.aSession = AsyncHTMLSession()  # 实例化异步session
        users = {# 可以在发送请求的时候更换user-agent
                1 : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                2 : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                3 : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                4 : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                5 : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        ur1 = random.sample(users.keys(),1)
        self.headers = "users"+str(ur1)

    def get_response(self):
        """获取响应，并返回requests_html中的HTML对象"""
        start_url = self.start_url
        r = self.session.get(start_url, headers={'user-agent': self.headers})
        print("网页状态",r)

        return r.html

    # 快速获取页面中的url
    def fast_get_urls(self):
        """快速获取页面中的url"""
        html = self.get_response()

        #"All_paths"
        #网页所有链接：HTML的 links属性 可以快速获取到页面中 a标签中的href属性
        urls = html.links
        # pprint(urls)

        #"Absolute_path"
        #网页绝对链接：HTML的 absolute_links属性 可以快速获取到页面中 a标签中的href属性，并返回绝对url地址
        absolute_urls = html.absolute_links
        pprint(absolute_urls)

    # 清洗数据（提取数据）
    def get_data_by_xpath(self):
        """使用xpath获取数据"""
        html = self.get_response()
        a_list = html.xpath('//div')
        # pprint(a_list)

        # 提取它的标题和url
        movies_info = dict()
        for a in a_list:
            title = a.text  # 获取标题（文本）
            print(title)
            # self.download(title,"协程与任务.txt")
            # movie_url = a.attrs.get('href')  # 使用 attrs 来解析element元素，并获得一个字典
            # print(movie_url)
            # print('-----')
            # movies_info[title] = movie_url

        pprint(movies_info)


    # 加载JS页面
    def load_js(self):
        html = self.get_response()

        '''
        渲染网站
        下载chromium
        '''
        # script = """
            # () => {
                # return {
                    # width: document.documentElement.clientWidth,
                    # height: document.documentElement.clientHeight,
                    # deviceScaleFactor: window.devicePixelRatio,
                # }
            # }
            # """
        # val = r.html.render(script=script,reload=False)
        # print(val)
        
        # 使用一个 render()方法 来加载js（实际上使用这个pyppeteer）
        # html.render(wait=3)  # js加载
        print(html.html)

    def download(self,texts,file_name):
        file_paths = os.path.abspath(os.path.dirname(__file__)) + "\\" + file_name
        with open(file_paths,'a',encoding="utf-8") as f:#使用追加模式写入文件
            f.write(texts)
            f.close()

if __name__ == '__main__':
    url = 'https://cn.bing.com/images/search?q=%e6%9c%ac%e5%85%ae%e5%9b%be%e7%89%87%e5%a3%81%e7%ba%b8%e9%ab%98%e6%b8%85&qpvt=%e6%9c%ac%e5%85%ae%e5%9b%be%e7%89%87%e5%a3%81%e7%ba%b8%e9%ab%98%e6%b8%85&form=IGRE&first=1&tsc=ImageBasicHover'
    test = DouBanTest(url)
    test.get_data_by_xpath()