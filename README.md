# Chain Reaction: Supply Chain Investment Platform

Chain Reaction is a full-stack application that analyzes small business supply chains and generates strategic investment opportunities to strengthen local economies.

## Overview

This application bridges the gap between investors and local businesses by:
1. Analyzing small business data to understand their supply chains
2. Generating investment opportunities based on supply chain analysis
3. Providing an interactive map interface to explore local businesses
4. Creating optimized investment portfolios for users based on risk preference

The platform uses Google's Gemini AI to generate supply chain analyses and then recommends stock investments that align with supporting those supply chains.

## Features

- **Interactive Business Map**: Explore local businesses in an interactive map interface
- **AI-Generated Supply Chain Analysis**: Utilizes Google Gemini to generate comprehensive supply chain analyses
- **Investment Portfolio Optimization**: Creates optimized investment portfolios based on the supply chain
- **Risk-Based Budgeting**: Allows users to set their investment budget and risk tolerance
- **Real-time Stock Ticker Integration**: Provides real investment opportunities using stock ticker symbols

## Technology Stack

### Backend
- **Python/FastAPI**: RESTful API backend
- **Google Generative AI**: Supply chain analysis generation
- **yfinance**: Stock data integration
- **Pandas/NumPy/SciPy**: Data processing and portfolio optimization
- **BeautifulSoup**: Web scraping for business data

### Frontend
- **React**: Frontend UI framework
- **Leaflet**: Interactive maps
- **Recharts**: Data visualization
- **Lucide**: UI icons

## Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google Generative AI API key

### Backend Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with:
GOOGLE_API_KEY=your_google_api_key_here
```

4. Run the FastAPI server:
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Setup
1. Install dependencies:
```bash
cd my-react-app
npm install
```

2. Start the development server:
```bash
npm start
```

3. Access the application at http://localhost:3000

## Usage Flow

1. **Login**: Authenticate through the Nessie API
2. **Set Budget**: Select your investment budget on the risk selection screen
3. **Explore Map**: Browse local businesses on the interactive map
4. **Analyze Business**: Select a business to view details and generate supply chain analysis
5. **Generate Investment**: Create an optimized investment portfolio based on the supply chain
6. **Adjust Investments**: Fine-tune your investment allocations as needed

## Project Structure

- `backend/`: Python FastAPI backend code
  - `gemini/`: Google Generative AI integration
  - `models/`: Portfolio optimization models
- `my-react-app/`: React frontend application
  - `src/`: Source code
  - `components/`: React components
  - `services/`: API service integration

