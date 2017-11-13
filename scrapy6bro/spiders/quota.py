#!/usr/bin/python  
import scrapy
import re
import hashlib
import json
import codecs  
from scrapy.selector import Selector
from scrapy6bro.items import Scrapy6BroItem
from scrapy.spider import Spider  
from scrapy.http import Request  
from w3lib.html import remove_tags
from bs4 import BeautifulSoup



def get_md5_value(src):
      myMd5 = hashlib.md5()
      myMd5.update(src.encode('utf-8'))
      myMd5_Digest = myMd5.hexdigest()
      return myMd5_Digest

class QuotesSpider(scrapy.Spider):
    name = "quotes"

  #  def start_requests(self):
    start_urls  = [

            # 'https://www.qiushibaike.com/text/',
            # 'http://www.budejie.com/text/1',
            'http://www.budejie.com/detail-25888769.html',
      
        ]
  #      for url in urls:
   #         yield scrapy.Request(url=url, callback=self.parse)



 



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


# budejie detail parse
        page = response.url.split("/")
        filename = 'quotes-%s.html' % page
        pattern = re.compile('/\{.+\}/s',re.I)
        soup = BeautifulSoup(response.body,"lxml")

        script = soup.find('script', text=re.compile('_BFD\.BFD_INFO'))
        json_text = re.search(r'^\s*_BFD\.BFD_INFO\s*=\s*({.*?})\s*;\s*$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)


        m = re.compile(r'//.*')
        outtmp = re.sub(m, ' ', json_text)
        outstring = outtmp

        
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
          yield item 

      
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

    #   # # proceeding crwal
    #   page=48   
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
