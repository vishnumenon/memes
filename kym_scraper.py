# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import scrapy

class MemeSpider(scrapy.Spider):
    # output file name
    name="memes"
    # First page of full meme db
    start_urls = [
        'http://knowyourmeme.com/memes/all'
    ]

    def parse(self, response):
        # Return the meme title for each meme on the page
        for meme in response.css('.entry_list td'):
            yield {
                'meme': meme.css('h2 a::text').extract_first()
            }
        # Find the next-page link
        next_page = response.css('.pagination .next_page::attr("href")').extract_first()
        # Follow the link if it exists, then re-run the scraper
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
