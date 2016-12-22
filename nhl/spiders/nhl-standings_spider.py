import os
import time
import json
import base64
import scrapy
from scrapy_splash import SplashRequest
from scrapy.conf import settings

class NHLStandingsSpider(scrapy.Spider):
    name = "nhl-standings"

    def start_requests(self):
        urls = [
            'http://www.nhl.com/standings/'

        ]
        for url in urls:
            splash_args = {
                'html': 1,
                'png': 1,
                'width': 800,
                'render_all': 1,
                'wait': 1.5,
            }
            yield SplashRequest(url, self.parse_result, endpoint='render.json',
                                args=splash_args)

    def parse_result(self, response):
        # magic responses are turned ON by default,
        # so the result under 'html' key is available as response.body
        html = response.body

        # you can also query the html result as usual
        title = response.css('title').extract_first()

        # full decoded JSON data is available as response.data:
        png_bytes = base64.b64decode(response.data['png'])

        # TODO: Customize filename pattern and path.
        self.save_file(response, 'png', png_bytes)
        # self.save_file(response, 'html', response.body)

        # TODO: Store table name (Atlantic) (Eastern-Wildcard)
        matrix = [
            ["wildcard-division-18", 1, 4],
            ["wildcard-division-17", 1, 4],
            ["wildcard-conference-6", 1, 11],
            ["wildcard-division-16", 1, 4],
            ["wildcard-division-15", 1, 4],
            ["wildcard-conference-5", 1, 9],
        ]

        for row in matrix:
            section_name = row[0];
            from_range = row[1];
            to_range = row[2];

            # eg:table_section = response.xpath("//*[contains(@id, 'wildcard-division-18')]")
            table_section = response.xpath("//*[contains(@id, '"+ section_name+ "')]")

            for x in xrange(from_range, to_range):

                yield {
                    'pos': str(x),
                    # eg: table_section.xpath("./div/div/div[2]/table/tbody/tr[1]/td[1]/span/a/span[3]/text()").extract_first(),
                    # TODO colocar SIGLA (PIT)
                    'team-name': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[1]/span/a/span[3]/text()").extract_first(),
                    'short-name': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[1]/span/a/span[4]/text()").extract_first(),
                    'gp': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[2]/span/text()").extract_first(),
                    'w': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[3]/span/text()").extract_first(),
                    'l': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[4]/span/text()").extract_first(),
                    'ot': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[5]/span/text()").extract_first(),
                    'pts': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[6]/span/text()").extract_first(),

                    'row': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[7]/span/text()").extract_first(),
                    'gf': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[8]/span/text()").extract_first(),
                    'ga': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[9]/span/text()").extract_first(),
                    'diff': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[10]/span/span/text()").extract_first(),
                    'home': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[11]/span/text()").extract_first(),

                    'away': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[12]/span/text()").extract_first(),
                    'so': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[13]/span/text()").extract_first(),
                    'l10': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[14]/span/text()").extract_first(),
                    'strk': table_section.xpath("./div/div/div[2]/table/tbody/tr["+ str(x) +"]/td[15]/span/text()").extract_first(),

                }

    def save_file(self, response, filetype, data):
        page = response.url.split("/")[-2]

        timestr = time.strftime("%Y%m%d-%H%M%S")
        pngfile = '%s_nhl-%s.%s' % (timestr, page, filetype)

        with open (os.path.expanduser("./photos/" + pngfile), 'wb') as f:
            f.write(data)

        self.log('Saved %s image %s on' % (filetype, pngfile))
