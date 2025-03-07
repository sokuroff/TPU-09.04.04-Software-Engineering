import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SteamSpider(CrawlSpider):
    name = "steam"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ['https://store.steampowered.com/search/?category1=998&supportedlang=english&filter=globaltopsellers&ndl=1']

    # Уникальные игры
    unique_games = set()

    # Счётчик добавленных записей
    records_count = 0

    custom_settings = {
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0.5,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept-Language': 'english'
        },
    }

    rules = (
        Rule(LinkExtractor(allow=r'/app/\d+/', deny=(r'\?l=')), callback='parse_game', follow=True),
    )

    def parse_game(self, response):
        title = response.xpath('//*[@id="appHubAppName"]/text()').get()
        release_date = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div[2]/div[2]/text()').get()
        developer = response.xpath('//*[@id="developers_list"]/a/text()').get()
        publisher = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div[4]/div[2]/a/text()').get()
        tags = response.xpath('//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a/text()').getall()
        bundle = response.xpath('//*[@id="game_area_purchase_top"]/div/h1/span/text()').get()
        music = response.xpath('//*[@id="game_area_purchase"]/div[1]/div/h1/text()').get()

        # Проверка на уникальность
        if title and title in self.unique_games:
            return
        self.unique_games.add(title)

        # Очистка данных
        game_data = {
            'title': title.strip() if title else None,
            'release_date': release_date.strip() if release_date else None,
            'developer': developer.strip() if developer else None,
            'publisher': publisher.strip() if publisher else None,
            'tags': [tag.strip() for tag in tags],
            'bundle': bundle.strip() if bundle else None,
            'music': music.strip() if music else None,
        }

        # Фильтрация по "Bundle"
        if game_data['bundle'] is not None and game_data['bundle'] == 'Bundle':
            return

        # Фильтрация по музыкальным тегам
        music_tags = ["downloadbare soundtrack", "downloadable content", "Downloadable Soundtrack", "Downloadable Content"]
        for tag in music_tags:
            if game_data['music'] is not None and tag == game_data['music']:
                return

        # Увеличиваем счётчик только при добавлении в документ
        if game_data['title'] and game_data['developer']:
            self.records_count += 1
            yield game_data

        # Остановка паука при достижении лимита
        if self.records_count >= 1000:
            self.crawler.engine.close_spider(self, reason='Reached limit of 1000 titles')
