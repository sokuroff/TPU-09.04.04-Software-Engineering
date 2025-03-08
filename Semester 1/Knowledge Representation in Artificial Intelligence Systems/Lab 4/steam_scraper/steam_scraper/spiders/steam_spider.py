import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd


class SteamSpider(CrawlSpider):
    name = "steam"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ['https://store.steampowered.com/search/?category1=998&filter=topsellers&ndl=1'] # список топ продаж

    custom_settings = { # кастомные настройки
        'CONCURRENT_REQUESTS': 8, # параллельные настройки
        'DOWNLOAD_DELAY': 2, # задержка перед скачиванием
        'DEFAULT_REQUEST_HEADERS': { # какой язык мы будем скачивать
            'Accept-Language': 'english'
        }
    }

    rules = (
        Rule(LinkExtractor(allow=r'/app/\d+/', deny=r'\?l=', unique=True), callback='parse_game', follow=True), # забираем ссылки вида /app/31232132, т.е. только с приложениями
    )

    unique_game = set()

    def parse_game(self, response): 
        title = response.xpath('//*[@id="appHubAppName"]/text()').get() # извлекаем название игры с элемента с id appHubAppName
        release_date = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div[2]/div[2]/text()').get() # дату выхода игры
        developer = response.xpath('//*[@id="developers_list"]/a/text()').get()
        publisher = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div[4]/div[2]/a/text()').get()
        tags = response.xpath('//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a/text()').getall()
        bundle = response.xpath('//*[@id="game_area_purchase_top"]/div/h1/span/text()').get()
        music = response.xpath('//*[@id="game_area_purchase"]/div[1]/div/h1/text()').get()

        if title: # если игра уже была то парсим следующую
            if title in self.unique_game:
                return
            self.unique_game.add(title)

        game_data = { # создаём словарь с данными об игре
            'title': title.strip() if title else None,
            'release_date': release_date.strip() if release_date else None,
            'developer': developer.strip() if developer else None,
            'publisher': publisher.strip() if publisher else None,
            'tags': [tag.strip() for tag in tags],
            'bundle': bundle.strip() if bundle else None,
            'music': music.strip() if music else None,
        }

        music_tags = ["downloadbare soundtrack", "downloadable content", "Downloadable Soundtrack", "Downloadable Content"] # если это музыка, то игнорируем (это не игра)
        if game_data['music']:
            for tag in music_tags:
                if tag.lower() in game_data['music'].lower():
                    return

        if len(self.unique_game) >= 1100:
            self.crawler.engine.close_spider(self, reason='Reached limit of 1100 titles')

        if game_data['title'] and game_data['developer']: # если есть название и разработчик, то можем записать в файлик
            yield game_data
