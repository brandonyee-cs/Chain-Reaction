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

    def get_prompt(self, sbID : str): # Mutator
        data_loader = DataLoader()

        self.prompt = f"Act as a agentic machine learning model. You will be given a small business's scraped website data, transaction and business information, local economic data, and weather data. Construct a supply chain from start to endfor the given small business (given the information provided).Please provide your response as a string with each industry in the supply chain separate by a comma. 
        Attached is the data:
        {data_loader.get_weather()}
        {data_loader.get_website_data(sbID)}
        {data_loader.get_economic_data()}
        {data_loader.get_small_business_data(sbID)}"
    
    def generate_supply_chain(self, sbID : str): # Accessor
        self.get_prompt(sbID)

        try:
            response = self.model.generate_content(self.prompt)
            self.supply_chain = response
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def get_ticker_list(self, supply_chain : str):
        
        prompt = f"Act as a stock screener. You will be given a list of industries in a supply chain. Provide a list of stock tickers that are in the given industries. Please provide your response as a string with each industry seperated by a semicolon (;) stock ticker separate by a comma(,). Please ensure that each group of industrys in the response coresponds to the industry in the supply chain in the exact same order.
        {supply_chain}"
        response = self.model.generate_content(prompt)

        response.split(";")
        
        for i in range(len(response)): response[i] = response[i].split()

    def get_supply_chain(self):
        return (self.supply_chain).split()

def main():
    try:
        # Initialize Gemini
        gemini = Gemini()

        # Example small business ID (using one from the DataLoader urls)
        sbID = "FWR"  # The Flower Wall Rental Co.

        # Generate supply chain
        print("Generating supply chain...")
        supply_chain_response = gemini.generate_supply_chain(sbID)
        print(f"Supply Chain: {supply_chain_response}")

        # Get the processed supply chain as a list
        supply_chain = gemini.get_supply_chain()
        print(f"\nProcessed Supply Chain: {supply_chain}")

        # Get related stock tickers
        print("\nGetting related stock tickers...")
        ticker_list = gemini.get_ticker_list(supply_chain_response)
        print(f"Related Tickers by Industry: {ticker_list}")

    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
    