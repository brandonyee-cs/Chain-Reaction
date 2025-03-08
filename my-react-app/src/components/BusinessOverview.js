import React, { useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

// This is a mock to demonstrate the business overview flow
const BusinessOverview = () => {
  const [showSupplyChain, setShowSupplyChain] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showInvestForm, setShowInvestForm] = useState(false);
  
  // Mock business data
  const business = {
    name: "Fresh Goods Market",
    business_type: "Grocery",
    established: 2010,
    annual_revenue: 1200000,
    employees: 12,
    address: "456 Oak Ave, Queens, NY",
    neighborhood: "Kew Gardens Hills",
    sq_footage: 1800,
    phone: "(718) 555-1234"
  };
  
  // Mock supply chain data
  const supplyChainData = [
    { name: "Raw Materials", value: 35, color: "#10b981" },
    { name: "Equipment", value: 25, color: "#f59e0b" },
    { name: "Services", value: 30, color: "#8b5cf6" },
    { name: "Distribution", value: 10, color: "#ef4444" }
  ];
  
  // Mock ETF data
  const etfData = {
    name: "Local Business Growth ETF",
    ticker: "LBGX",
    value: 250,
    returnRate: 5.2,
    risk: "Medium",
    color: "#3b82f6",
    holdings: [
      { name: "Fresh Goods Market", percentage: 15 },
      { name: "Regional Supply Co.", percentage: 25 },
      { name: "Local Tech Services", percentage: 20 },
      { name: "Community Banking", percentage: 18 },
      { name: "Small Business Support", percentage: 12 },
      { name: "Other Holdings", percentage: 10 },
    ]
  };
  
  const handleGenerateSupplyChain = () => {
    setIsGenerating(true);
    // Simulate API call with timeout
    setTimeout(() => {
      setShowSupplyChain(true);
      setIsGenerating(false);
    }, 1500);
  };
  
  // Custom tooltip for the pie chart
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-2 bg-white border rounded shadow">
          <p className="font-semibold">{payload[0].name}</p>
          <p>{payload[0].value}%</p>
        </div>
      );
    }
    return null;
  };
  
  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      {/* Back Button */}
      <button 
        className="mb-4 text-blue-600 flex items-center gap-1"
      >
        ← Back to Map
      </button>
      
      {/* Business Header */}
      <div className="flex justify-between items-start mb-4 bg-white p-4 rounded-lg shadow">
        <div>
          <h2 className="text-2xl font-semibold mb-1">{business.name}</h2>
          <p className="text-gray-600 text-sm">
            {business.business_type} · Established {business.established}
          </p>
        </div>
        <div className="text-right">
          <p className="text-green-600 font-semibold text-lg">
            ${business.annual_revenue.toLocaleString()} Annual Revenue
          </p>
          <p className="text-gray-500 text-sm">{business.employees} Employees</p>
        </div>
      </div>
      
      {/* Business Details */}
      <div className="bg-white p-4 rounded-lg shadow mb-4">
        <h3 className="text-lg font-semibold mb-3">Business Overview</h3>
        
        <div className="grid gap-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Location</span>
            <span className="font-medium">{business.address}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Neighborhood</span>
            <span className="font-medium">{business.neighborhood}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Square Footage</span>
            <span className="font-medium">{business.sq_footage} sq ft</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Contact</span>
            <span className="font-medium">{business.phone}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Years in Operation</span>
            <span className="font-medium">{new Date().getFullYear() - business.established}</span>
          </div>
        </div>
      </div>
      
      {/* Business Description */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h3 className="text-lg font-semibold mb-3">Business Description</h3>
        <p className="text-gray-700 mb-3 leading-relaxed">
          {business.name} is a {business.business_type.toLowerCase()} business located in {business.neighborhood}. 
          With ${business.annual_revenue.toLocaleString()} in annual revenue and {business.employees} employees, 
          it plays an important role in the local economy and community.
        </p>
        <p className="text-gray-700 leading-relaxed">
          Established in {business.established}, this business has built a reputation for quality service
          and contributes to the character and economic health of the neighborhood.
        </p>
      </div>
      
      {/* Generate Button Section */}
      {!showSupplyChain ? (
        <div className="text-center my-8">
          <p className="mb-4 text-gray-600">
            Generate a supply chain analysis and investment options for this business
          </p>
          <button
            onClick={handleGenerateSupplyChain}
            disabled={isGenerating}
            className={`py-3 px-6 rounded-lg font-semibold inline-flex items-center gap-2 ${
              isGenerating ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'
            } text-white transition`}
          >
            {isGenerating ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </>
            ) : (
              'Generate Supply Chain Analysis'
            )}
          </button>
        </div>
      ) : (
        <>
          {/* Supply Chain Analysis */}
          <div className="bg-white p-4 rounded-lg shadow mb-6">
            <h3 className="text-lg font-semibold mb-4">Supply Chain Analysis</h3>
            <div className="flex justify-center mb-6 h-64">
              <PieChart width={400} height={250}>
                <Pie
                  data={supplyChainData}
                  cx={200}
                  cy={125}
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {supplyChainData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
                <Legend />
              </PieChart>
            </div>
            
            <div className="space-y-2 mb-4">
              {supplyChainData.map((item, index) => (
                <div
                  key={index}
                  className="flex justify-between items-center p-3 bg-gray-50 rounded-md border-l-4"
                  style={{ borderLeftColor: item.color }}
                >
                  <div>
                    <h4 className="font-semibold">{item.name}</h4>
                    <p className="text-gray-600 text-sm">{item.value}% of supply chain</p>
                  </div>
                  <div className="w-4 h-4 rounded-full" style={{ backgroundColor: item.color }}></div>
                </div>
              ))}
            </div>
          </div>
          
          {/* ETF Information */}
          <div className="bg-white p-4 rounded-lg shadow mb-6">
            <h3 className="text-lg font-semibold mb-4">ETF Investment Option</h3>
            
            <div className="flex justify-between items-start mb-4 bg-gray-50 p-4 rounded-md">
              <div>
                <h4 className="font-semibold mb-1">
                  {etfData.name} ({etfData.ticker})
                </h4>
                <p className="text-gray-600 text-sm">
                  Risk Level: 
                  <span className={`ml-1 px-2 py-0.5 rounded-full text-xs font-medium ${
                    etfData.risk === 'Low' ? 'bg-green-100 text-green-800' : 
                    etfData.risk === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-red-100 text-red-800'
                  }`}>
                    {etfData.risk}
                  </span>
                </p>
              </div>
              <div className="text-right">
                <p className="text-green-600 font-semibold">
                  {etfData.returnRate}% Return Rate
                </p>
                <p className="text-gray-600 text-sm">
                  Value: ${etfData.value}
                </p>
              </div>
            </div>
            
            <p className="text-gray-700 mb-4">
              This ETF includes {business.name} along with other local businesses in a
              diversified portfolio designed to support community economic growth.
            </p>
            
            <div className="mt-4">
              <h4 className="text-base font-semibold mb-2">ETF Holdings</h4>
              <div className="space-y-1">
                {etfData.holdings.map((holding, index) => (
                  <div
                    key={index}
                    className="flex justify-between py-2 border-b last:border-b-0"
                  >
                    <span className={holding.name === business.name ? 'font-medium text-blue-600' : ''}>
                      {holding.name}
                      {holding.name === business.name && ' (Current Business)'}
                    </span>
                    <span>{holding.percentage}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          {/* Invest Now Button */}
          <div className="text-center my-8">
            {!showInvestForm ? (
              <button
                onClick={() => setShowInvestForm(true)}
                className="py-4 px-8 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg text-lg transition transform hover:scale-105"
              >
                Invest Now
              </button>
            ) : (
              <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg mx-auto">
                <h3 className="text-xl font-semibold mb-4">Invest in {business.name}</h3>
                
                <div className="mb-4">
                  <label className="block text-gray-600 mb-2">Investment Amount ($)</label>
                  <input
                    type="number"
                    defaultValue={Math.round(business.annual_revenue * 0.1)}
                    min="100"
                    step="100"
                    className="w-full p-3 border border-gray-300 rounded-md"
                  />
                </div>
                
                <div className="bg-blue-50 p-4 rounded-md mb-4">
                  <h4 className="text-blue-800 font-semibold mb-2">Investment Summary</h4>
                  <p className="text-gray-700 text-sm mb-1">Expected Return: 12-15% Annual</p>
                  <p className="text-gray-700 text-sm">Term: 24-36 months</p>
                </div>
                
                <div className="flex gap-4">
                  <button
                    onClick={() => setShowInvestForm(false)}
                    className="flex-1 py-3 border border-gray-300 text-gray-600 font-medium rounded-md hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => alert('Investment submitted successfully!')}
                    className="flex-1 py-3 bg-green-600 text-white font-medium rounded-md hover:bg-green-700"
                  >
                    Confirm Investment
                  </button>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default BusinessOverview;