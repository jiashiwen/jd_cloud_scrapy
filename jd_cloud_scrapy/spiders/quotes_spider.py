from pathlib import Path
import scrapy
import re
import chompjs 

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
             "https://docs.jdcloud.com/cn/yanxi-cap/manage-workspace"     
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]        
        filename = f"pages/{page}.html"
        
        js=response.selector.xpath("//body/script/text()").get()
        #解析script 中的函数      
        fun = re.search(r"window\.__NUXT__=\(function\((.*?)\)\s*{([\s\S]*?)}\((.*?)\)\);", js,re.M).group(2)
        # 提取aP.content 的 markdown内容            
        content=re.search(r"aP\.content\s*=\s*\"(.*)\";",fun,re.M).group(1).replace("\\n","\n")
        print(content)


   
        