# NHL-Standings

### A python scrapy-splash spider project to scrap data from NHL Standings day-to-day (for personal use only).

A splash-scrapy project for gettting nhl standings everyday from nhl.com. The motivation is that there is no way to follow the ups and downs
off  the standings using the NHL web site. Since NHL.com does not provide a way so that the fans can see the stats in a specific day.

Before you use this, please read the NHL.com [terms of service](https://www.nhl.com/info/terms-of-service). In essence, you can download content
FOR PERSONAL USE ONLY.

## Getting started

* Install Scrapy

Instructions: https://doc.scrapy.org/en/latest/intro/install.html

* Install Scrapy-Splash

https://github.com/scrapy-plugins/scrapy-splash

OBS: Follow all the instructions, and remember to install docker as well.

In the end, you should be able to run:
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash

* Test and Running

### Write results in a JSON file called nhl.json
scrapy crawl nhl-standings -o nhl.json

### Run scrapy on shell mode
scrapy shell 'http://192.168.99.100:8050/render.html?url=http://www.nhl.com/standings/&html=1&png=1&wait=1.0'
(MUST CHANGE TO YOUR IP ADDRESS)
