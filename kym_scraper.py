import scrapy

class MemeSpider(scrapy.Spider):
    name="memes"
    start_urls = [
        'http://knowyourmeme.com/memes/all'
    ]

    def parse(self, response):
        for meme in response.css('.entry_list td'):
            yield {
                'meme': meme.css('h2 a::text').extract_first()
            }

        next_page = response.css('.pagination .next_page::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
