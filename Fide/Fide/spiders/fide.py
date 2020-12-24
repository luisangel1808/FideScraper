import scrapy
import re
# XPath
# links = //div[@class="col-lg-12 profile-top-rating-dataCont"]/div/text()
class Fide(scrapy.Spider):
    name = 'fide'
    start_urls = [
        'https://ratings.fide.com/profile/4416856'
    ]
    custom_settings = {
        'FEED_URI': 'fide.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    
    def parse(self, response):

        #players_id = ['4421965','4402898','4416856','4454553','4433491','4430646','4430638','4402324']
        players_id = ['4427564','4472594','4457315','4443195','4415817','4495276','4422848','4412486','4413610','4464591','4450329','4416856','4457307','4479637','4421876','4464605','4471750','4454553','4456637','4421965','4420080','4456645','4402324','4414861','4402898','4437950','4437187','4457420','4457617','4401522','4430638','4430646','4412397','4415914','4433491']

        for link in players_id:
            print(response.urljoin(link))
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': 'https://ratings.fide.com/profile/4416856'})

    def parse_link(self, response, **kwargs):
 
        link = kwargs['url']
        name = response.xpath('//div[@class="col-lg-8 profile-top-title"]/text()').get()
        data= response.xpath('//div[@class="profile-top-info__block__row__data"]/text()').getall()
        title = data[-1]
        sex = data[-2]
        year = data[-3]
        id = data[-4]
        active = response.xpath('//div[@class="profile-top-info__block__row__header"]/text()').get() 
        if(active=="World Rank (Active):"):
            active= True
        else: active = False
        std = response.xpath('//div[@class="profile-top-rating-data profile-top-rating-data_gray"]/text()').getall()[1]
        try:
            std = re.findall("\d+", std)[0]
        except IndexError:
            std = 0 
        rapid = response.xpath('//div[@class="profile-top-rating-data profile-top-rating-data_red"]/text()').getall()[1]
        try:
            rapid = re.findall("\d+", rapid)[0]
        except IndexError:
            rapid = 0  
        blitz = response.xpath('//div[@class="profile-top-rating-data profile-top-rating-data_blue"]/text()').getall()[1]
        try:
            blitz = re.findall("\d+", blitz)[0]
        except IndexError:
            blitz = 0  
        
        yield {
            'name': name,
            'std': std,
            'rapid': rapid,
            'blitz': blitz,
            'year': year,
            'active': active,
            'sex': sex,
            'title': title,
            'id': id
        }