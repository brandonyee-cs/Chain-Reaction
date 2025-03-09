import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Now we can import from backend
from backend.gemini.weather import WeatherAPI
from backend.gemini.web_scraper import WebScraper
import wbgapi as wb
import json
from typing import Dict, Any, List, Optional, Union

class SmallBusinessDataLoader:
    """
    Class to load small business data for the supply chain generation system
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data loader
        
        Args:
            data_dir: Directory containing small business data files
        """
        self.data_dir = data_dir
        self.data_cache = {}
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Path to the small business data file
        self.data_file = Path(data_dir) / "small_business_data.json"
        
        # Load data if file exists
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    self.data_cache = json.load(f)
            except Exception as e:
                print(f"Error loading small business data: {str(e)}")
        else:
            # If file doesn't exist, try to generate data
            self._generate_initial_data()
    
    def get_small_business_data(self, sbID: str) -> Dict[str, Any]:
        """
        Get data for a specific small business
        
        Args:
            sbID: Small business ID
            
        Returns:
            Dictionary containing business data or empty dict if not found
        """
        # Check if data is in cache
        if sbID in self.data_cache:
            return self.data_cache[sbID]
        
        # If not in cache, check if there's a specific file for this business
        specific_file = Path(self.data_dir) / f"{sbID.lower()}_data.json"
        if specific_file.exists():
            try:
                with open(specific_file, 'r') as f:
                    business_data = json.load(f)
                    self.data_cache[sbID] = business_data
                    return business_data
            except Exception as e:
                print(f"Error loading specific business data: {str(e)}")
        
        # If we have a generator, generate data on demand
        try:
            # Import here to avoid circular imports
            from backend.gemini.small_business_data_generator import SmallBusinessDataGenerator
            generator = SmallBusinessDataGenerator()
            business_data = generator.generate_business_data(sbID)
            self.data_cache[sbID] = business_data
            
            # Save to cache file
            self.save_data(sbID, business_data)
            
            return business_data
        except ImportError as e:
            print(f"SmallBusinessDataGenerator not available: {str(e)}")
            # If generator not available, return basic info
            return self._get_default_business_data(sbID)
    
    def save_data(self, sbID: str, data: Dict[str, Any]) -> None:
        """
        Save data for a specific small business
        
        Args:
            sbID: Small business ID
            data: Business data to save
        """
        # Add to cache
        self.data_cache[sbID] = data
        
        # Update main data file
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data_cache, f, indent=2)
        except Exception as e:
            print(f"Error saving small business data: {str(e)}")
    
    def get_all_business_ids(self) -> List[str]:
        """
        Get a list of all available business IDs
        
        Returns:
            List of business IDs
        """
        return list(self.data_cache.keys())
    
    def _generate_initial_data(self) -> None:
        """Generate initial data for businesses if generator is available"""
        try:
            # Import here to avoid circular imports
            from backend.gemini.small_business_data_generator import SmallBusinessDataGenerator
            generator = SmallBusinessDataGenerator()
            
            # Generate data for each business ID in the business types dictionary
            all_data = {}
            for business_id in generator.business_types.keys():
                business_data = generator.generate_business_data(business_id)
                all_data[business_id] = business_data
            
            # Save to cache
            self.data_cache = all_data
            
            # Save to file
            with open(self.data_file, 'w') as f:
                json.dump(all_data, f, indent=2)
                
            print(f"Generated initial data for {len(all_data)} businesses")
        except ImportError:
            print("SmallBusinessDataGenerator not available, skipping initial data generation")
    
    def _get_default_business_data(self, sbID: str) -> Dict[str, Any]:
        """Generate minimal default data for a business when generator is not available"""
        business_types = {
            'FWR': 'Flower Wall Rental',
            'GRAZE': 'Catering',
            'NAOMIS': 'Kosher Pizza',
            'BANDH': 'Plumbing and Heating',
            'AEROLA': 'Tattoo Shop',
            'ENOODLE': 'Noodle Restaurant',
            'BTFLI': 'Bathtub Refinishing',
            'MST': 'Taiwanese Restaurant',
            'ANDA': 'Cafe',
            'ARONS': 'Farms Market',
            'FARS': 'Appliance Repair',
            'OTNPP': 'Pizza Restaurant',
            'TSB': 'Sandwich Shop',
            'AS': 'Discount Store',
            'ZFSTG': 'Fusion Cuisine'
        }
    
        
        business_names = {
            "FWR": "The Flower Wall Rental Co.",
            "GRAZE": "Graze & Gather Catering",
            "NAOMIS": "Naomi's Kosher Pizza",
            "BANDH": "B&H Plumbing and Heating",
            "AEROLA": "Areola Tattooing Studio",
            "ENOODLE": "East Noodle House",
            "BTFLI": "Bathtub Refinishing Long Island",
            "MST": "Main Street Taiwanese",
            "ANDA": "Anda Cafe Flushing",
            "ARONS": "Aron's Kissena Farms",
            "FARS": "Flushing Appliance Repair Specialists",
            "OTNPP": "Pizza Professor",
            "TSB": "The Sandwich Bar",
            "AS": "Amazing Savings",
            "ZFSTG": "Zen Fusion Cuisine To Go"
        }
        
        business_type = business_types.get(sbID, "Unknown Business")
        business_name = business_names.get(sbID, f"{sbID} Business")
        
        return {
            "business_id": sbID,
            "name": business_name,
            "business_type": business_type,
            "address": f"{random.randint(40, 190)} Main St, Queens, NY",
            "zip_code": "11367",
            "annual_revenue": 100000,
            "suppliers": [],
            "inventory": {"total_items": 0, "categories": [], "top_items": []}
        }


class DataLoader:
    """
    Main data loader class for the Gemini system.
    Loads various types of data including weather, website data,
    economic data, and small business information.
    """
    
    def __init__(self):
        """Initialize the data loader with necessary components"""
        # Initialize small business data loader
        self.sb_data_loader = SmallBusinessDataLoader()
        self.economic_API_key = ''
        
        # Business URL mapping
        self.business_urls = {
            'FWR': 'https://www.theflowerwallrentalco.com',
            'GRAZE': 'https://grazebrands.com/upper-crust#uppercrust-locations',
            'NAOMIS': 'https://www.naomiskosherpizzamenu.com/?utm_source=gbp',
            'BANDH': 'https://www.bandhplumbingandheating.info/servicesplumbing.html',
            'AEROLA': 'https://www.areolatattooing.org',
            'ENOODLE': 'https://www.enoodle.nyc',
            'BTFLI': 'https://bathtubrefinishinglongisland.com',
            'MST': 'https://www.mainstreettaiwanese.com',
            'ANDA': 'https://andacafeflushing.com/',
            'ARONS': 'https://www.aronskissenafarms.com',
            'FARS': 'https://flushingappliancerepairspecialists.com',
            'OTNPP': 'https://www.orderthenewpizzaprofessor.com/?utm_source=gbp',
            'TSB': 'https://www.thesandwichbar.getsauce.com/',
            'AS': 'http://www.amazingsavings.com/',
            'ZFSTG': 'https://zenfusioncuisinetogo.com'
        }
    
    def get_weather(self) -> str:
        """
        Get current weather season data
        
        Returns:
            String representing the current season
        """
        try:
            weather = WeatherAPI()
            season = weather.get_season("America/New_York", "northern")
            return season
        except Exception as e:
            print(f"Error getting weather data: {str(e)}")
            return "Unknown"

    def get_website_data(self, sbID: str) -> Dict[str, Any]:
        """
        Get website data for a specific business by scraping its URL
        
        Args:
            sbID: Small business ID
            
        Returns:
            Dictionary containing scraped website data
        """
        try:
            # Get URL for the business
            if sbID not in self.business_urls:
                return {"error": f"No URL found for business ID: {sbID}"}
            
            url = self.business_urls[sbID]
            
            # Initialize web scraper and scrape the URL
            scraper = WebScraper(delay=1.5)  # 1.5 seconds delay between requests
            results = scraper.scrape_urls([url])  # Pass as a list since the method expects a list
            
            # Return first result if available, otherwise empty dict
            return results[0] if results else {}
        except Exception as e:
            print(f"Error scraping website data: {str(e)}")
            return {"error": str(e)}
    
    def get_economic_data(self) -> Dict[str, Any]:
        """
        Get economic data from World Bank API
        
        Returns:
            Dictionary containing economic data
        """
        try:
            # Fetch GDP data for the USA from 2010 to 2019
            gdp_data = wb.data.DataFrame('NY.GDP.MKTP.CD', economy='USA', time=range(2010, 2020))

            # Retrieve general economic information about the USA
            economy_info = wb.economy.info(q='USA')
            
            # For local economic data specific to Queens, NY (would require additional API)
            local_data = {
                "region": "Queens, NY",
                "zip_code": "11367",
                "median_income": 68000,
                "unemployment_rate": 5.2,
                "population": 27000
            }

            # Return structured data as dictionaries
            return {
                "gdp_data": gdp_data.to_dict() if not gdp_data.empty else {},
                "economy_info": economy_info if economy_info else {},
                "local_data": local_data
            }
        except Exception as e:
            print(f"Error getting economic data: {str(e)}")
            return {"error": str(e)}

    def get_small_business_data(self, sbID: str) -> Dict[str, Any]:
        """
        Get data for a specific small business
        
        Args:
            sbID: Small business ID
            
        Returns:
            Dictionary containing business data
        """
        try:
            return self.sb_data_loader.get_small_business_data(sbID)
        except Exception as e:
            print(f"Error getting small business data: {str(e)}")
            return {"error": str(e)}

# Need to import random for the default business data generator
import random

# For testing
if __name__ == "__main__":
    # Test the data loader
    loader = DataLoader()
    
    # Test weather data
    print("\nWeather Data:")
    print(loader.get_weather())
    
    # Test small business data
    business_id = "FWR"
    print(f"\nSmall Business Data for {business_id}:")
    business_data = loader.get_small_business_data(business_id)
    if "error" not in business_data:
        print(f"Name: {business_data.get('name')}")
        print(f"Type: {business_data.get('business_type')}")
        print(f"Suppliers: {business_data.get('suppliers', [])}")
        print(f"Competitors: {business_data.get('competitors', [])}")
    else:
        print(f"Error: {business_data.get('error')}")
    
    # Test website data (summary)
    print(f"\nWebsite Data for {business_id}:")
    website_data = loader.get_website_data(business_id)
    if "error" not in website_data:
        print(f"Title: {website_data.get('title')}")
        print(f"Meta Description: {website_data.get('meta_description')}")
    else:
        print(f"Error: {website_data.get('error')}")
    
    # Test economic data (summary)
    print("\nEconomic Data:")
    economic_data = loader.get_economic_data()
    if "error" not in economic_data:
        print("GDP data and economy info loaded successfully")
        print(economic_data)
    else:
        print(f"Error: {economic_data.get('error')}")