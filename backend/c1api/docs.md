# Nessie Python SDK

The Nessie Python SDK provides a client library for interacting with Capital One's Nessie Banking API, a RESTful API that simulates a banking system. This SDK makes it easy to interact with the API in Python applications, particularly for hackathons and educational projects.

## Installation

Since the SDK is not currently on PyPI, install it directly from the GitHub repository:

```bash
git clone https://github.com/nessieisreal/nessie-python-sdk.git
pip install -e ./nessie-python-sdk/
```

## Authentication

You'll need an API key from the [Nessie API Getting Started page](http://api.reimaginebanking.com/#getting-started).

There are three ways to provide your API key:

1. **Environment Variable (Recommended)**:
   ```bash
   export NESSIE_API_KEY=your_api_key_here
   ```

2. **Using a .env File**:
   Create a `.env` file in your project directory with:
   ```
   NESSIE_API_KEY=your_api_key_here
   ```

3. **Directly in Code**:
   ```python
   client = Client("your_api_key_here")
   ```

## Basic Usage

```python
from nessie.client import Client
from nessie.models.address import Address

# Initialize the client
client = Client()

# Now you can access API endpoints through the client
```

## Core Components

### Client

The `Client` class is the main entry point for using the SDK. It provides access to all API resources.

```python
from nessie.client import Client

# Initialize with API key from environment variable
client = Client()

# Or specify the key explicitly
client = Client("your_api_key_here")

# Access resources through properties
client.customer  # CustomerRequest instance
client.account   # AccountRequest instance
client.bill      # BillRequest instance
client.deposit   # DepositRequest instance
client.data      # DataRequest instance
```

### Models

The SDK uses model classes to represent API resources:

- `Address`: Street address with validation
- `Customer`: Bank customer information
- `Account`: Banking account with type validation
- `Bill`: Payment bill with status and scheduling
- `Deposit`: Money added to an account
- `ATM`: ATM location with geolocation
- `Branch`: Bank branch with geolocation

## API Resources

### Customers

Create and manage bank customers.

```python
# Create a new customer
address = Address("123", "Main St", "Boston", "MA", "02115")
customer = client.customer.create_customer("John", "Doe", address)
customer_id = customer.customer_id

# Get all customers
customers = client.customer.get_all_customers()

# Get customer by ID
customer = client.customer.get_customer_by_id(customer_id)