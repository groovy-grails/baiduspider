'''
Created on 30 Apr 2020

@author: bros
'''
# -*- coding: utf-8 -*-
import base64
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
from .. items import BaiduItem


# splash lua script
script = """
         local random = math.random
         json = require("json")
         function main(splash, args)
             splash.private_mode_enabled = false
             splash:set_viewport_size(1366, 768)
             assert(splash:go(args.url))
             assert(splash:wait(2))
             local cookies = splash:get_cookies()
             png1 = splash:png{render_all=true}
             keyword = args.keyword
             input_text = splash:select("#kw")
             login_btn = splash:select("#su")
             if input_text  then
                 input_text:mouse_click({x=5, y=5})
                 input_text:send_text(keyword)
                 login_btn:mouse_click({x=5, y=5})
             end
             assert(splash:wait(math.random(2,3)))
             local cookies1 = splash:get_cookies()
             png2 = splash:png{render_all=true}
             if input_text  then
                 login_btn:mouse_click({x=5, y=5})
             end
             assert(splash:wait(math.random(10,20)))
             png3 = splash:png{render_all=true}
             local entries = splash:history()
             local last_response = entries[#entries].response
             return {
                url = splash.args.url,
                html = splash:html(),
                http_status = last_response.status,
                headers = last_response.headers,
                cookies = cookies,
                cookies1 = cookies1,
                png1 = png1,
                png2 = png2,
                png3 = png3,
                har = json.encode(splash:har()),
                }
         end
         """

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-languange': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://www.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        
    }

class facebookSpider(Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    url = 'https://www.baidu.com'
    
    # start requests
    def start_requests(self):
        yield SplashRequest(self.url, 
                            callback=self.parse,
                             endpoint='execute',
                              args={'lua_source': script,
                                     'keyword':'python  cursor.execute 没有更新数据库',
                                     'timeout': 60,
                                     'wait': 10, 
                                     'images_enabled': 'false', 
                                     'resource_timeout': 20, 
                                     'webgl_enabled': 'false',
                                     'media_source_enabled':'false'},
                              headers=headers)
    
    # parse the html content
    def parse(self, response):
        item=BaiduItem()
        print('='*40)
        print(response.data['http_status'])
        print('='*40)
        print(response.data['url'])
        print('='*40)
        print(response.data['cookies'])
        print('='*40)
        print(response.data['cookies1'])
        print('='*40)
        print(response.data['headers'])
        print('='*40)
        
        f = open('/home/bros/others/baidu.txt','w', encoding='utf-8')
        f.write(response.text)
        f.close
        f = open('/home/bros/others/baidu_har.txt','w', encoding='utf-8')
        f.write(response.data['har'])
        f.close
        f = open('/home/bros/others/b01.png','wb')
        f.write(base64.b64decode(response.data['png1']))
        f.close
        f = open('/home/bros/others/b02.png','wb')
        f.write(base64.b64decode(response.data['png2']))
        f.close
        f = open('/home/bros/others/b03.png','wb')
        f.write(base64.b64decode(response.data['png3']))
        f.close
        
        element=response.css('.result.c-container')
        for litag in element :
            try:
                nickname=litag.xpath('h3/a/text()').extract()
                nicknamestr=''.join(nickname)
                item['detail']=litag.css('.f13').xpath('a/@href').extract_first()
                item['nickname']=nicknamestr[0:50]
                item['phone_no']=''
                item['email']=''
                item['languange_code']=''
                item['languange_name']=''
                print('-'*40)
                print(nickname)
                print(item['detail'])
                print('-'*40)
                yield item
            except:
                print('!'*40)
                continue
        
        
        
        