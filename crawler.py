# -*- coding: utf-8 -*-

import scrapy, json

class Crawler(scrapy.Spider):
    name = "smartphone_spider"
    dados = []
    # página 1 da categoria smartphone
    start_urls = ['https://www.casasbahia.com.br/c/telefones-e-celulares/smartphones/?Filtro=c38_c326&nid=201546']
    custom_settings = {'USER_AGENT':'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)'}

    # define os seletores xpath ou css utilizados
    NAME_SELECTOR = '//b[@itemprop="name"]/text()'
    ID_SELECTOR = '//input[@name="ctl00$Conteudo$hdnIdSkuSelecionado"]/@value'
    PRICE_SELECTOR = '//i[@class="sale price"]/text()'
    CATEGORY_SELECTOR = '//*[@class="breadcrumb"]//*[@itemprop="name"]/text()'
    SET_SELECTOR = '.cont-product'
    URL_PRODUCT_SELECTOR = 'a ::attr(href)'
    NEXT_PAGE_SELECTOR = '//link[@rel="next"]/@href'
    PRICE_DISCOUNT_SELECTOR = '//*[@class="for price discount"]/text()'


    def parse(self, response):

        # para cada smartphone presente na página da categoria, pegar sua url
        for smartphone in response.css(self.SET_SELECTOR):

            url = smartphone.css(self.URL_PRODUCT_SELECTOR).extract_first()

            # acessar o endereço do smartphone atual
            if url:
                yield scrapy.Request(url, callback = self.parse_detalhes)

            # se não tem mais smartphones na página, passar para a próxima
            next_page = smartphone.xpath(self.NEXT_PAGE_SELECTOR).extract_first()

            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
            # se não tem mais páginas da categoria smartphone, escrever o arquivo json com o resultado
            else:
                with open('resultado.json', 'w') as fp:
                    json.dump(Crawler.dados,fp)

    # capturar os dados de cada smartphone em seu endereço específico e armazenar na lista
    def parse_detalhes(self, response):
        name = response.xpath(self.NAME_SELECTOR).extract_first()
        id = response.xpath(self.ID_SELECTOR).extract_first()
        price = response.xpath(self.PRICE_SELECTOR).extract_first()
        price_discount = response.xpath(self.PRICE_DISCOUNT_SELECTOR).extract_first()
        category = ' > '.join(response.xpath(self.CATEGORY_SELECTOR).extract())
        Crawler.dados.append({"id":id,"nome":name,"preço_boleto":price_discount,"preço_atual":price,"category":category})