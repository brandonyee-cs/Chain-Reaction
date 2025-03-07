from backend.Gemini.weather import WeatherAPI
from backend.Gemini.web_scraper import WebScraper

class DataLoader:
    def __init__(self):
        economic_API_key = ''
    
    def get_weather(self):
        weather = WeatherAPI()
        season = weather.get_season("America/New_York", "northern")
        return season

    def get_website_data(self, sbID : str):
        urls = {
            'FWR' : 'https://www.theflowerwallrentalco.com',
            'GRAZE' : 'https://grazebrands.com/upper-crust#uppercrust-locations',
            'NAOMIS' : 'https://www.naomiskosherpizzamenu.com/?utm_source=gbp',
            'BANDH' : 'https://www.bandhplumbingandheating.info/servicesplumbing.html',
            'AEROLA' : 'https://www.areolatattooing.org',
            'ENOODLE' : 'https://www.enoodle.nyc',
            'BTFLI' : 'https://bathtubrefinishinglongisland.com',
            'MST' : 'https://www.mainstreettaiwanese.com',
            'ANDA' : 'https://andacafeflushing.com/',
            'ARONS' : 'https://www.aronskissenafarms.com',
            'FARS' : 'https://flushingappliancerepairspecialists.com',
            'OTNPP' : 'https://www.orderthenewpizzaprofessor.com/?utm_source=gbp',
            'TSB' : 'https://www.thesandwichbar.getsauce.com/',
            'AS' : 'http://www.amazingsavings.com/',
            'ZFSTG' : 'https://zenfusioncuisinetogo.com'
        }

        url = urls[sbID]
        scraper = WebScraper(delay=1.5)  # 1.5 seconds delay between requests
        results = scraper.scrape_urls(url)
        return results
    
    def get_economic_data(self):
        pass

    def get_small_business_data(self, name : str):
        pass