# coding: utf-8

import scrapy, json

class Crawler(scrapy.Spider):
    name = "smartphone_spider"
    dados = []
    start_urls = ['https://www.casasbahia.com.br/c/telefones-e-celulares/smartphones/?Filtro=c38_c326&nid=201546']
    custom_settings = {'USER_AGENT':'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)'}

    NAME_SELECTOR = '//b[@itemprop="name"]/text()'
    ID_SELECTOR = '//input[@name="ctl00$Conteudo$hdnIdSkuSelecionado"]/@value'
    PRICE_SELECTOR = '//i[@class="sale price"]/text()'
    CATEGORY_SELECTOR = '//*[@class="breadcrumb"]//*[@itemprop="name"]/text()'
    SET_SELECTOR = '.cont-product'
    URL_PRODUCT_SELECTOR = 'a ::attr(href)'
    NEXT_PAGE_SELECTOR = '//link[@rel="next"]/@href'

    def parse(self, response):
        urls = []
        for smartphone in response.css(self.SET_SELECTOR):

            #NAME_SELECTOR = 'a ::attr(title)'
            #ID_SELECTOR = "a .price-product ::attr(id)"
            #PRICE_SELECTOR = "//*[@live-price='Price']/text()"
            #URL_SELECTOR = 'a ::attr(href)'
            """yield {
                'name':smartphone.css(NAME_SELECTOR).extract_first(),
                'id':smartphone.css(ID_SELECTOR).extract_first(),
                'price':smartphone.xpath(PRICE_SELECTOR).extract_first(),
                'url':smartphone.css(URL_SELECTOR).extract_first()
            }"""

            url = smartphone.css(self.URL_PRODUCT_SELECTOR).extract_first()
            yield scrapy.Request(url, callback = self.parse_detalhes)
            next_page = smartphone.xpath(self.NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
            else:
                with open('resultado.json', 'w',encoding='UTF-8') as fp:
                    json.dump(Crawler.dados,fp)


    def parse_detalhes(self, response):
        name = response.xpath(self.NAME_SELECTOR).extract_first()
        id = response.xpath(self.ID_SELECTOR).extract_first()
        price = response.xpath(self.PRICE_SELECTOR).extract_first()
        category = ' > '.join(response.xpath(self.CATEGORY_SELECTOR).extract())
        Crawler.dados.append({"id":id,"nome":name,"preço":price,"category":category})
        #print(Crawler.dados)


        #PROXIMA_URL_SELECTOR = '//link[@rel="next"]/@href'
        #next_url = response.xpath(PROXIMA_URL_SELECTOR).extract_first()
       # if next_url:


        #yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
         #   SET_SELECTOR2 = '.breadcrumb'
          #  response.css(SET_SELECTOR2)
           # BREADCRUMB_SELECTOR = '//*[@itemprop="name"]/text()'
