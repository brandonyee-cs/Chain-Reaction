import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.gemini.data_loader import DataLoader

import google.generativeai as genai
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Gemini:
    """
    Gemini class integrates with Google's generative AI to analyze small business data 
    and generate relevant supply chain information and stock tickers.
    """
    
    def __init__(self, model_name: str = 'gemini-pro') -> None:
        """
        Initialize the Gemini interface with Google's generative AI.

        Args:
            model_name: Name of the generative model to use (default: 'gemini-pro')
        """
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            logger.warning("No Google API key found in environment variables")
        
        try:
            # Configure the API with the key
            genai.configure(api_key=self.api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Successfully initialized {model_name} model")
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {str(e)}")
            raise
        
        # Initialize other attributes
        self.prompt = ""
        self.supply_chain = None
        self.data_loader = DataLoader()

    def get_prompt(self, sbID: str) -> str:
        """
        Construct a prompt using data from the DataLoader for the given business ID.
        
        Args:
            sbID: Small business ID to get data for
            
        Returns:
            Constructed prompt string
        """
        try:
            # Get current season from the weather API
            season = self.data_loader.get_weather()
            
            # Get website data for the business
            website_data = self.data_loader.get_website_data(sbID)
            
            # Get economic data
            economic_data = self.data_loader.get_economic_data()
            
            # Get small business data
            business_data = self.data_loader.get_small_business_data(sbID)
            
            # Construct a more detailed prompt with improved instructions
            self.prompt = f"""
            Act as an expert supply chain analyst and business intelligence system.

            Your task is to analyze the following small business data and construct a comprehensive 
            supply chain from raw materials to end consumer for the business.

            Consider the following in your analysis:
            1. The current season is {season}, which may affect seasonal products and demand
            2. The business type and its specific requirements
            3. The local economic conditions
            4. The business's existing suppliers and inventory
            5. Any information gleaned from the business's website

            BUSINESS INFORMATION:
            {business_data}

            WEBSITE DATA:
            {website_data}

            LOCAL ECONOMIC DATA:
            {economic_data}

            Please provide your response as a comma-separated list of industries that form 
            the supply chain from raw materials to end consumer.
            Format: industry1, industry2, industry3, ...
            """
            
            logger.info(f"Successfully generated prompt for business ID: {sbID}")
            return self.prompt
            
        except Exception as e:
            logger.error(f"Error generating prompt for business ID {sbID}: {str(e)}")
            raise
    
    def generate_supply_chain(self, sbID: str) -> str:
        """
        Generate a supply chain analysis for the given business ID.
        
        Args:
            sbID: Small business ID to generate supply chain for
            
        Returns:
            Generated supply chain response string
        """
        try:
            # Get the prompt for the business
            self.get_prompt(sbID)
            
            # Generate content using the model
            response = self.model.generate_content(self.prompt)
            
            # Extract and store the text response
            if hasattr(response, 'text'):
                self.supply_chain = response.text
            else:
                self.supply_chain = str(response)
                
            logger.info(f"Successfully generated supply chain for business ID: {sbID}")
            return self.supply_chain
            
        except Exception as e:
            error_msg = f"Error generating supply chain for business ID {sbID}: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def get_ticker_list(self, supply_chain: str) -> Dict[str, List[str]]:
        """
        Generate a list of stock tickers for each industry in the supply chain.
        
        Args:
            supply_chain: Comma-separated string of industries
            
        Returns:
            Dictionary mapping industries to lists of related stock tickers
        """
        try:
            # Construct a prompt to get stock tickers for the industries
            prompt = f"""
            Act as a financial analyst specializing in industry-specific stock screening.
            
            For each of the following industries in a supply chain, provide a list of 3-5 publicly 
            traded companies (with their stock tickers) that are major players in that industry.
            
            Supply chain industries: {supply_chain}
            
            Format your response as:
            Industry1: TICKER1, TICKER2, TICKER3
            Industry2: TICKER1, TICKER2, TICKER3, TICKER4
            ...
            
            Only include actual stock tickers for real companies that trade on major exchanges.
            """
            
            # Generate content
            response = self.model.generate_content(prompt)
            
            # Extract response text
            if hasattr(response, 'text'):
                response_text = response.text
            else:
                response_text = str(response)
            
            # Parse the response into a dictionary
            ticker_dict = {}
            for line in response_text.strip().split('\n'):
                if ':' in line:
                    industry, tickers = line.split(':', 1)
                    ticker_list = [t.strip() for t in tickers.split(',')]
                    ticker_dict[industry.strip()] = ticker_list
            
            logger.info(f"Successfully generated ticker list with {len(ticker_dict)} industries")
            return ticker_dict
            
        except Exception as e:
            error_msg = f"Error generating ticker list: {str(e)}"
            logger.error(error_msg)
            return {"error": [error_msg]}

    def get_supply_chain(self) -> List[str]:
        """
        Get the processed supply chain as a list of industries.
        
        Returns:
            List of industries in the supply chain
        """
        if not self.supply_chain:
            logger.warning("No supply chain data available. Call generate_supply_chain() first.")
            return []
            
        # Split by comma and strip whitespace
        industries = [industry.strip() for industry in self.supply_chain.split(',')]
        logger.info(f"Processed supply chain into {len(industries)} industries")
        return industries
    
    def analyze_business_competitive_landscape(self, sbID: str) -> Dict[str, Any]:
        """
        Analyze the competitive landscape for a business.
        
        Args:
            sbID: Small business ID to analyze
            
        Returns:
            Dictionary with competitive analysis data
        """
        try:
            # Get business data
            business_data = self.data_loader.get_small_business_data(sbID)
            
            # Extract competitors if available
            competitors = business_data.get('competitors', [])
            
            # Analyze competitors and provide insights
            if competitors:
                prompt = f"""
                Act as a competitive intelligence analyst.
                
                Analyze the following competitors of {business_data.get('name')} 
                (a {business_data.get('business_type')} business) and provide 
                strategic recommendations:
                
                {competitors}
                
                Provide a concise SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
                based on this competitive landscape.
                """
                
                # Generate content
                response = self.model.generate_content(prompt)
                
                # Extract response text
                if hasattr(response, 'text'):
                    analysis = response.text
                else:
                    analysis = str(response)
                
                return {
                    "business_name": business_data.get('name'),
                    "business_type": business_data.get('business_type'),
                    "competitors": competitors,
                    "competitive_analysis": analysis
                }
            else:
                return {
                    "business_name": business_data.get('name'),
                    "business_type": business_data.get('business_type'),
                    "competitors": [],
                    "competitive_analysis": "No competitor data available for analysis."
                }
                
        except Exception as e:
            error_msg = f"Error analyzing competitive landscape for business ID {sbID}: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}

def main():
    """
    Main function to demonstrate Gemini functionality
    """
    try:
        # Initialize Gemini with default model
        gemini = Gemini()
        print("Initialized Gemini successfully")

        # Example small business ID (using one from the DataLoader urls)
        sbID = "FWR"  # The Flower Wall Rental Co.

        # Generate supply chain
        print("\nGenerating supply chain...")
        supply_chain_response = gemini.generate_supply_chain(sbID)
        print(f"Supply Chain: {supply_chain_response}")

        # Get the processed supply chain as a list
        supply_chain_list = gemini.get_supply_chain()
        print(f"\nProcessed Supply Chain: {supply_chain_list}")

        # Get related stock tickers
        print("\nGetting related stock tickers...")
        ticker_dict = gemini.get_ticker_list(supply_chain_response)
        print("Related Tickers by Industry:")
        for industry, tickers in ticker_dict.items():
            print(f"  {industry}: {', '.join(tickers)}")
            
        # Analyze competitive landscape
        print("\nAnalyzing competitive landscape...")
        comp_analysis = gemini.analyze_business_competitive_landscape(sbID)
        print(f"Competitive Analysis for {comp_analysis.get('business_name')}:")
        print(comp_analysis.get('competitive_analysis'))

    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()