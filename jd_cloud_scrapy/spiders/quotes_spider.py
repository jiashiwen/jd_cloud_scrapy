from pathlib import Path
import scrapy
import re
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            # "https://docs.jdcloud.com/cn/yanxi-cap/product-overview"
            "https://docs.jdcloud.com/cn/virtual-machines/learning"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url_list = response.selector.xpath(
            '//ul[contains(@class,"nav-inner-list")]/li/a/@href').getall()
        for url in url_list:
            if url == "javascript:;":
                continue
            url = "https://docs.jdcloud.com"+url
            yield scrapy.Request(url=url, callback=self.get_markdown)

    def get_markdown(self, response):
        name = response.url.split("/")[-1]
        filename = f"pages/{name}.md"
        js = response.selector.xpath("//body/script/text()").get()
        # 解析script 中的函数
        fun = re.search(
            r"window\.__NUXT__=\(function\((.*?)\)\s*{([\s\S]*?)}\((.*?)\)\);", js, re.M).group(2)
        # 提取aP.content 的 markdown内容
        markdown = re.search(r".content\s*=\s*\"(.*)\";",
                             fun, re.M).group(1).replace("\\n", "\n")
        Path(filename).write_bytes(bytes(markdown, encoding="utf8"))
        self.log(f"Saved file {filename}")
        # print(markdown)
