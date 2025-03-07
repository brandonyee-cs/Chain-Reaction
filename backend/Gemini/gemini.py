from backend.Gemini.data_loader import DataLoader

import google.generativeai as genai
from typing import Optional
import os
from dotenv import load_dotenv

class Gemini: # Constructor
    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')

        self.model = genai.GenerativeModel('gemini-pro')

        self.prompt = 'Data Not Found'


    def get_prompt(self, sbID : str): # Mutator
        data_loader = DataLoader()

        self.prompt = f"Act as a agentic machine learning model. You will be given a small business's scraped website data, transaction and business information, local economic data, and weather data. Construct a supply chain from start to endfor the given small business (given the information provided).Please provide your response as a string with each industry in the supply chain separate by a comma. 
        Attached is the data:
        {data_loader.get_weather()}
        {data_loader.get_website_data(sbID)}
        {data_loader.get_economic_data()}
        {data_loader.get_small_business_data(sbID)}"
    
    def get_supply_chain(self, sbID : str): # Accessor
        self.get_prompt(sbID)

        try:
            response = self.model.generate_content(self.prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
