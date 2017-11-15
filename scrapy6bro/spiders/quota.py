#!/usr/bin/python  
import scrapy
import re
import hashlib
import json
import codecs  
import random
import pymongo
import requests
import base64
import time
from scrapy.selector import Selector
from scrapy6bro.items import Scrapy6BroItem
from scrapy.spider import Spider  
from scrapy.http import Request  
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from pyDes import *

def get_md5_value(src):
      myMd5 = hashlib.md5()
      myMd5.update(src.encode('utf-8'))
      myMd5_Digest = myMd5.hexdigest()
      return myMd5_Digest



class QuotesSpider(scrapy.Spider):
    name = "quotes"
    Des_Key =  "AB+ujs@u" # Key
    Des_IV = "12345678" # 自定IV向量
  #  def start_requests(self):
    page = random.randint(20000000,28000000)
    url = "http://www.budejie.com/detail-"+str(25069978)+'.html'
    allowed_domains = ["budejie.com"]
    start_urls  = [

            # 'https://www.qiushibaike.com/text/',
            # 'http://www.budejie.com/text/1',
            # 'http://www.budejie.com/detail-25888769.html',
            url,
      
        ]
    rules = ( #自动从response中根据正则表达式提取url，再根据这个url再次发起请求，并用callback解析返回的结果
        Rule(LinkExtractor(allow=(r'https://www.budejie.com/detail-\d*')), follow = True),
        )
       #Rule(LinkExtractor(allow=(r'https://movie.douban.com/tag/\[wW]+'))), # 从网页中提取http链接
        
    
  #      for url in urls:
   #         yield scrapy.Request(url=url, callback=self.parse)



 

    def find_url(self) :
     page = random.randint(24000000,26000000)
     url = "http://www.budejie.com/detail-"+str(page)+'.html'

      #"yyyy/MM/dd HH:mm:ss"
     res=requests.post('http://192.168.1.101:8080/GetJokeDataByContent',data =json.dumps({"contentid":page}))
     dates=json.loads(res.text)
     print(dates['code'])
    
     if dates['code'] == 200 :
       # print(json.dumps(dates['data']))
       self.find_url()
     else:
       return scrapy.Request(url,callback=self.parse)  


     # mongo_uri = "mongodb://localhost:27017",
     # mongo_db ="src6bro"
     # client = pymongo.MongoClient(mongo_uri)
     # db = client[mongo_db]
     # table = db['budejie']
     if table.find_one({"source":url}) :
        # client.close()
         self.find_url()
     else :
        # client.close()
        return scrapy.Request(url,callback=self.parse)  
        



    def parse_start_url(self, response):
        urls = response.xpath('//a[@class="c-next-btn"]//@href').extract()
        for url in urls:
            if 'https' not in url: # 去除多余的链接
                 url = response.urljoin(url) # 补全
                 print(url)
                
                 yield scrapy.Request(url) 



    def parse(self, response):
        # for quote in response.css('div.fr'):
        #     yield {
        #         'text': quote.css('p::text').extract_first(),
        #         # 'author': quote.css('small.author::text').extract_first(),
        #         # 'tags': quote.css('div.tags a.tag::text').extract(),
        #     }

        # next_page = response.css('a.a1::attr(href)')[1]
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # page = response.url.split("/")
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        # 	for one in response.xpath('//script/text()'):
        #           f.write(one.extract().encode('utf-8'))
        #           continue
        # f.close()    
    
 

     
    
     if response.status == 200:
        	
        

# budejie detail parse
         page = response.url.split("/")
         filename = 'quotes-%s.html' % page
         pattern = re.compile('/\{.+\}/s',re.I)
         soup = BeautifulSoup(response.body,"lxml")

         script = soup.find('script', text=re.compile('_BFD\.BFD_INFO'))
         try :
          json_text = re.search(r'^\s*_BFD\.BFD_INFO\s*=\s*({.*?})\s*;\s*$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)
       



          m = re.compile(r'//.*')
          outtmp = re.sub(m, ' ', json_text)
          n =  re.compile(r'^(?:http|ftp)s?://',re.IGNORECASE)
          outtmp1 = re.sub(n, ' ', outtmp)
          outstring = outtmp1

         

          try :
           data = json.loads(outstring)
           if "段子" in data['tag'] :
            print(outstring)
            myMd5 = hashlib.md5()
            myMd5.update(data['title'].encode('utf-8'))
            myMd5_Digest = myMd5.hexdigest()
            item = Scrapy6BroItem()
            item['md5'] = myMd5_Digest
            item['content'] =data['title']
            item['source'] = response.url
            item['contentid'] = data['id']
            now_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
            d = k.encrypt(now_time)
            # print(data['title'])
            token=base64.b64encode(d).decode('utf-8') #转base64编码返回) #转base64编码返回
            rof=json.dumps({"token":token,"data":{"md5":myMd5_Digest,
                "content":data['title'],"source":response.url,"contentid":data['id']}})
            print(rof)  
            resp=requests.post('http://192.168.1.101:8080/UploadJokesData',data = rof )
            dates=json.loads(resp.text)
            print(dates)
            yield item 

          except Exception as e:
            print('parse json error')
         #   find_url()
            yield self.find_url()
        
         except:
            yield self.find_url()
      
        # # pattern_end = re.compile('<\s*/\s*span\s*>',re.I)
        # with open(filename, 'wb') as f:
        # 	for one in response.xpath('//script/text()'):
        #           if "BFD.BFD_INFO" in one.extract() :
        #              f.write(one.extract().encode('utf-8'))
        #           continue
        # f.close()   
# 





      # json parse
      # items = []  
    
      # f = open('qiushibaike.txt','a')
      # pattern = re.compile('<span\*?[^>]*>',re.I)
      # pattern_end = re.compile('<\s*/\s*span\s*>',re.I)

    #   pattern = re.compile('<a\*?[^>]*>',re.I)
    #   pattern_end = re.compile('<s*/\s*a\s*>',re.I)

    #   # #budejie
    #   # # for content in response.xpath('//div[@class="j-r-list"]//ul//li') :
    #   # for content in response.xpath('//div[@class="j-r-list"]//ul//li//div[@class="j-r-list-c-desc"]//a') :
    #   #       # yield{'text':content.xpath('div[@class="j-r-list-c"]//div[@class="j-r-list-c-desc"]//a').extract() }
    #   #       item = Scrapy6BroItem()
    #   #       # item['content'] = [t.encode('utf-8') for t in content.xpath('div[@class="j-r-list-c"]//div[@class="j-r-list-c-desc"]//a').extract()]  
    #   #       # item['content'] =  content.xpath('div[@class="j-r-list-c"]//div[@class="j-r-list-c-desc"]//a').extract() 
    #   #       s= pattern.sub('',content.extract())
    #   #       s=pattern_end.sub('',s)
    #   #       item['content'] =  re.sub(r'[\t\r\n\s]', '',s)
    #   #       myMd5 = hashlib.md5()
    #   #       myMd5.update(item['content'].encode('utf-8'))
    #   #       myMd5_Digest = myMd5.hexdigest()
    #   #       item['md5'] = myMd5_Digest
    #   #       item['source'] = response.url
    #   #       items.append(item) 

    #   #       continue
            







    #   #qiushibaike
    #   # re_style=re.compile('<\s*span[^>]*>*<\s*/\s*span\s*>',re.I)#style



    #   # for content in response.xpath('//div[contains(@class,"article")]//div[@class="content"]/span') :
    #   #       # yield{'text':content.xpath('div[@class="j-r-list-c"]//div[@class="j-r-list-c-desc"]//a').extract() }
    #   #       item = Scrapy6BroItem()
    #   #       # item['content'] = [t.encode('utf-8') for t in content.xpath('div[@class="j-r-list-c"]//div[@class="j-r-list-c-desc"]//a').extract()]  
    #   #       # item['content'] =  content.xpath('div[@class="j-r-list-c"]//div[@class="j-r-list-c-desc"]//a').extract() 
    #   #       s= pattern.sub('',content.extract())
    #   #       s=pattern_end.sub('',s)
    #   #       item['content'] =  re.sub(r'[\t\r\n\s]', '',s)
    #   #       items.append(item) 
    #   #       continue



    #   for one in items :           
    #      yield one 


         yield self.find_url()

     else :    
         yield self.find_url()
         # page = random.randint(24000000,26000000)
         # url = "http://www.budejie.com/detail-"+str(page)+'.html'
         # mongo_uri = "mongodb://localhost:27017",
         # mongo_db ="src6bro"
         # client = pymongo.MongoClient(mongo_uri)
         # db = client[mongo_db]
         # table = db['budejie']
         # if table.find_one({"source":url}) :
         #    find_url()
         # else :
        	# # client.close()
         # 	yield scrapy.Request("http://www.budejie.com/detail-"+str(page)+'.html',callback=self.parse) 
         	


    #   # # proceeding crwal
       
       
    #   # while page<13 :
    #   while page<52 :
    #      page +=1
    #      # yield scrapy.Request(" https://www.qiushibaike.com/text/page/"+str(page)+"/",callback=self.parse)
    #      yield scrapy.Request("http://www.budejie.com/text/"+str(page),callback=self.parse)          
    #   # #end 

    #  #end 
     


    # # def clear_span_br(self,txt):
    # #     p = re.compile(r'((<span>)|(</span>)|(<br>))+')
    # #     a = []
    # #     for t in txt:
    # #         a.append(p.sub(' ',t))
    # #     return a

     
