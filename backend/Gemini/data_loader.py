from backend.Gemini.weather import WeatherAPI
from backend.Gemini.web_scraper import WebScraper
import yfinance as yf
import wbgapi as wb

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
    
    def get_stock_data(self):
        # sample
        dat = yf.Ticker("MSFT")
        # multiple tickers
        tickers = yf.Tickers('MSFT AAPL GOOG')
        tickers.tickers['MSFT'].info
        yf.download(['MSFT', 'AAPL', 'GOOG'], period='1mo')
        # Funds
        spy = yf.Ticker('SPY').funds_data
        spy.description
        spy.top_holdings

    def get_economic_data(self):
         # List available databases
        sources = wb.source.info()

        # Fetch GDP data for the USA from 2010 to 2019
        gdp_data = wb.data.DataFrame('NY.GDP.MKTP.CD', economy='USA', time=range(2010, 2020))

        # Retrieve general economic information about the USA
        economy_info = wb.economy.info(q='USA')

        # Return structured data
        return {
            "sources": sources, 
            "gdp_data": gdp_data,
            "economy_info": economy_info
        }

    def get_small_business_data(self, name : str):
        #Implement API call to get small business data
        pass