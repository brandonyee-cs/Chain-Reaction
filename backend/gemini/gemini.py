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
    
    def __init__(self, model_name: str = 'gemini-2.0-flash-lite-preview') -> None:
        """
        Initialize the Gemini interface with Google's generative AI.

        Args:
            model_name: Name of the generative model to use (default: 'gemini-2.0-flash-lite-preview')
        """
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            logger.warning("No Google API key found in environment variables")
        
        try:
            # Configure the API with the key
            genai.configure(api_key=self.api_key)
            
            # Initialize the model with optimized settings for Gemini 2.0 Lite
            generation_config = {
                'temperature': 0.7,  # Balanced between creativity and precision
                'top_p': 0.9,       # More focused response distribution
                'top_k': 40,        # Diverse but controlled token selection
                'max_output_tokens': 2048  # Reasonable output length for analysis
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            logger.info(f"Successfully initialized {model_name} model with optimized settings")
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
            
            # Construct a more focused prompt optimized for Gemini 2.0 Lite
            self.prompt = f"""
            As a supply chain analyst, create a concise supply chain analysis for this business.

            Key Information:
            - Season: {season} (impacts seasonal demand)
            - Business Data: {business_data}
            - Website Info: {website_data}
            - Economic Context: {economic_data}

            Required: List the supply chain stages from raw materials to end consumer.
            Format: stage1, stage2, stage3, ...
            Keep responses focused and precise.
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
            
            # Generate content using the model with stream=False for Gemini 2.0 Lite
            response = self.model.generate_content(
                self.prompt,
                stream=False
            )
            
            # Extract and store the text response
            if hasattr(response, 'text'):
                self.supply_chain = response.text.strip()
            else:
                self.supply_chain = str(response).strip()
                
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
            # Construct a focused prompt for Gemini 2.0 Lite
            prompt = f"""
            List 3 major publicly traded companies (stock tickers) for each industry:
            Industries: {supply_chain}

            Format:
            Industry1: TICK1, TICK2, TICK3
            Industry2: TICK1, TICK2, TICK3

            Rules:
            - Only include real companies on major exchanges
            - Use official ticker symbols
            - Focus on market leaders
            = Only include the tickers, no additional information as per the stated format
            """
            
            # Generate content with stream=False for Gemini 2.0 Lite
            response = self.model.generate_content(
                prompt,
                stream=False
            )
            
            # Extract response text
            if hasattr(response, 'text'):
                response_text = response.text.strip()
            else:
                response_text = str(response).strip()
            
            # Parse the response into a dictionary
            ticker_dict = {}
            for line in response_text.split('\n'):
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

def main():
    """
    Main function to demonstrate Gemini functionality
    """
    try:
        # Initialize Gemini with Gemini 2.0 Lite model
        gemini = Gemini()
        print("Initialized Gemini 2.0 Lite successfully")

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

    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()