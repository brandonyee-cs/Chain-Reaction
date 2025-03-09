import L from "leaflet";
import "leaflet/dist/leaflet.css";
import React, { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { Cell, Pie, PieChart, Tooltip as RechartsTooltip } from "recharts";
import businessData from "../data/small_business_data.json";

// Supply Chain List Component (text-only, no visual diagram)
const SupplyChainList = ({ supplyChainList }) => {
  if (!supplyChainList || supplyChainList.length === 0) {
    return <p style={{ color: "#9ca3af" }}>No supply chain data available</p>;
  }
  
  // Generate colors for nodes
  const nodeColors = [
    "#10b981", // green
    "#f59e0b", // amber
    "#8b5cf6", // purple
    "#3b82f6", // blue
    "#ec4899", // pink
    "#f43f5e", // rose
    "#6366f1", // indigo
  ];

  return (
    <div style={{ marginBottom: "2rem" }}>
      <h3 style={{
        fontSize: "18px",
        fontWeight: "600",
        marginBottom: "1rem",
        color: "white",
      }}>
        Supply Chain Components
      </h3>
      <div style={{ 
        padding: "1rem",
        backgroundColor: "#111827",
        borderRadius: "0.5rem",
        border: "1px solid #374151",
      }}>
        <div style={{ 
          display: "flex", 
          flexDirection: "column",
          gap: "0.75rem",
        }}>
          {supplyChainList.map((node, index) => (
            <div key={index} style={{
              padding: "0.75rem 1rem",
              backgroundColor: "#1f2937",
              borderRadius: "0.375rem",
              borderLeft: `4px solid ${nodeColors[index % nodeColors.length]}`,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}>
              <div>
                <span style={{ fontWeight: "600", color: "white" }}>
                  {index + 1}. {node.trim()}
                </span>
              </div>
              <div style={{
                backgroundColor: nodeColors[index % nodeColors.length],
                width: "1rem",
                height: "1rem",
                borderRadius: "50%",
              }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Editable Investment Pie Chart Component
const EditableInvestmentPieChart = ({ investmentData, setInvestmentData }) => {
  if (!investmentData || !investmentData.portfolio || investmentData.portfolio.length === 0) {
    return <p style={{ color: "#9ca3af" }}>No investment data available</p>;
  }
  
  const handleInvestmentChange = (index, newValue) => {
    // Create a copy of the investment data
    const newInvestmentData = {...investmentData};
    const newPortfolio = [...newInvestmentData.portfolio];
    
    // Update the investment amount
    newPortfolio[index].investment = parseFloat(newValue);
    
    // Calculate new total
    const newTotal = newPortfolio.reduce((sum, item) => sum + item.investment, 0);
    
    newInvestmentData.portfolio = newPortfolio;
    newInvestmentData.total_investment = newTotal;
    
    // Update the state
    setInvestmentData(newInvestmentData);
  };
  
  // Generate colors for the pie chart
  const COLORS = ['#10b981', '#f59e0b', '#8b5cf6', '#3b82f6', '#ec4899', '#f43f5e', '#6366f1'];
  
  return (
    <div style={{
      marginTop: "2rem",
      padding: "1.5rem",
      backgroundColor: "#1a1a1a",
      borderRadius: "0.5rem",
      border: "1px solid #374151",
    }}>
      <h3 style={{
        fontSize: "18px",
        fontWeight: "600",
        marginBottom: "1.5rem",
        color: "white",
        textAlign: "center"
      }}>
        Investment Portfolio Allocation
      </h3>
      
      <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "2rem",
      }}>
        {/* Pie Chart */}
        <div style={{ width: "100%", height: "300px", position: "relative" }}>
          <PieChart width={400} height={300} style={{ margin: "0 auto" }}>
            <Pie
              data={investmentData.portfolio}
              cx={200}
              cy={150}
              labelLine={true}
              outerRadius={100}
              fill="#8884d8"
              dataKey="investment"
              label={({ name, ticker, percent }) => 
                `${ticker} (${(percent * 100).toFixed(0)}%)`
              }
            >
              {investmentData.portfolio.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[index % COLORS.length]} 
                  stroke="#111"
                />
              ))}
            </Pie>
            <RechartsTooltip 
              formatter={(value) => `$${value.toFixed(2)}`} 
              labelFormatter={(index) => investmentData.portfolio[index].ticker}
            />
          </PieChart>
        </div>
        
        {/* Investment Editor */}
        <div style={{
          width: "100%",
          maxWidth: "500px",
          backgroundColor: "#111827",
          padding: "1.5rem",
          borderRadius: "0.5rem",
          border: "1px solid #374151",
        }}>
          <h4 style={{
            fontSize: "16px",
            fontWeight: "600",
            marginBottom: "1rem",
            color: "white",
          }}>
            Edit Investments
          </h4>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            {investmentData.portfolio.map((item, index) => (
              <div key={index} style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0.5rem",
                backgroundColor: "#1f2937",
                borderRadius: "0.375rem",
                borderLeft: `3px solid ${COLORS[index % COLORS.length]}`
              }}>
                <div style={{ display: "flex", flexDirection: "column" }}>
                  <span style={{ 
                    fontWeight: "600",
                    color: COLORS[index % COLORS.length]
                  }}>
                    {item.ticker}
                  </span>
                  <span style={{ fontSize: "0.75rem", color: "#9ca3af" }}>
                    ${item.price.toFixed(2)} per share
                  </span>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <span style={{ color: "white" }}>$</span>
                  <input
                    type="number"
                    value={item.investment}
                    onChange={(e) => handleInvestmentChange(index, e.target.value)}
                    min="0"
                    step="100"
                    style={{
                      width: "100px",
                      backgroundColor: "#374151",
                      color: "white",
                      border: "1px solid #4b5563",
                      borderRadius: "0.25rem",
                      padding: "0.375rem 0.5rem",
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
          
          <div style={{
            marginTop: "1.5rem",
            padding: "0.75rem",
            backgroundColor: "#059669",
            borderRadius: "0.375rem",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}>
            <span style={{ color: "white", fontWeight: "500" }}>Total Investment:</span>
            <span style={{ color: "white", fontWeight: "600" }}>
              ${investmentData.total_investment.toFixed(2)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Business Details Component
const BusinessDetailsView = ({ business, onBack }) => {
  const [activeView, setActiveView] = useState("overview");
  const [showInvestmentForm, setShowInvestmentForm] = useState(false);

  // Mock supply chain data
  const supplyChainData = [
    { name: "Raw Materials", value: 35, color: "#10b981" },
    { name: "Equipment", value: 25, color: "#f59e0b" },
    { name: "Services", value: 30, color: "#8b5cf6" },
    { name: "Distribution", value: 10, color: "#ef4444" },
  ];

  const InvestmentForm = () => (
    <div
      style={{
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        backgroundColor: "black",
        padding: "2rem",
        borderRadius: "8px",
        boxShadow:
          "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
        width: "90%",
        maxWidth: "500px",
        zIndex: 2000,
      }}
    >
      <h2
        style={{ marginBottom: "1rem", fontSize: "1.5rem", fontWeight: "600" }}
      >
        Invest in {business.name}
      </h2>

      <div style={{ marginBottom: "1.5rem" }}>
        <label
          style={{ display: "block", marginBottom: "0.5rem", color: "#4b5563" }}
        >
          Investment Amount ($)
        </label>
        <input
          type="number"
          defaultValue={Math.round(business.annual_revenue * 0.1)}
          min="100"
          step="100"
          style={{
            width: "100%",
            padding: "0.75rem",
            border: "1px solid #d1d5db",
            borderRadius: "0.375rem",
            fontSize: "1rem",
          }}
        />
      </div>

      <div
        style={{
          backgroundColor: "#f0f9ff",
          padding: "1rem",
          borderRadius: "0.5rem",
          marginBottom: "1.5rem",
        }}
      >
        <h3
          style={{
            fontSize: "1rem",
            fontWeight: "600",
            marginBottom: "0.5rem",
            color: "#0369a1",
          }}
        >
          Investment Summary
        </h3>
        <p
          style={{
            color: "#4b5563",
            fontSize: "0.875rem",
            marginBottom: "0.5rem",
          }}
        >
          Expected Return: 12-15% Annual
        </p>
        <p style={{ color: "#4b5563", fontSize: "0.875rem" }}>
          Term: 24-36 months
        </p>
      </div>

      <div style={{ display: "flex", gap: "1rem" }}>
        <button
          onClick={() => setShowInvestmentForm(false)}
          style={{
            padding: "0.75rem 1rem",
            borderRadius: "0.375rem",
            border: "1px solid #d1d5db",
            backgroundColor: "white",
            color: "#4b5563",
            fontWeight: "500",
            cursor: "pointer",
            flex: 1,
          }}
        >
          Cancel
        </button>
        <button
          onClick={() => {
            alert("Investment submitted successfully!");
            setShowInvestmentForm(false);
          }}
          style={{
            padding: "0.75rem 1rem",
            borderRadius: "0.375rem",
            backgroundColor: "#059669",
            color: "white",
            border: "none",
            fontWeight: "500",
            cursor: "pointer",
            flex: 1,
          }}
        >
          Confirm Investment
        </button>
      </div>
    </div>
  );

  return (
    <div
      className="business-details"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "black",
        zIndex: 1000,
        padding: "20px",
        overflow: "auto",
      }}
    >
      {showInvestmentForm && <InvestmentForm />}

      <button
        onClick={onBack}
        style={{
          background: "none",
          border: "none",
          color: "#2563eb",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          gap: "4px",
          marginBottom: "20px",
          fontSize: "14px",
        }}
      >
        ← Back to Map
      </button>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "1rem",
        }}
      >
        <div>
          <h2
            style={{
              fontSize: "24px",
              fontWeight: "600",
              marginBottom: "8px",
              color: "white",
            }}
          >
            {business.name}
          </h2>
          <p style={{ color: "#9ca3af", fontSize: "14px" }}>
            {business.business_type} · Established {business.established}
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <p
            style={{
              color: "#34d399",
              fontSize: "18px",
              fontWeight: "600",
            }}
          >
            ${business.annual_revenue.toLocaleString()} Annual Revenue
          </p>
          <p style={{ color: "#9ca3af", fontSize: "14px" }}>
            {business.employees} Employees
          </p>
        </div>
      </div>

      <div
        style={{
          display: "flex",
          gap: "1rem",
          marginBottom: "1rem",
          background: "#1a1a1a",
          padding: "0.5rem",
          borderRadius: "0.5rem",
          border: "1px solid #374151",
        }}
      >
        <button
          onClick={() => setActiveView("overview")}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "0.25rem",
            background: activeView === "overview" ? "#2563eb" : "transparent",
            color: activeView === "overview" ? "white" : "#9ca3af",
            border: "none",
            fontWeight: "500",
            cursor: "pointer",
          }}
        >
          Business Overview
        </button>
        <button
          onClick={() => setActiveView("supplyChain")}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "0.25rem",
            background: activeView === "supplyChain" ? "#2563eb" : "transparent",
            color: activeView === "supplyChain" ? "white" : "#9ca3af",
            border: "none",
            fontWeight: "500",
            cursor: "pointer",
          }}
        >
          Supply Chain
        </button>
      </div>

      {activeView === "overview" ? (
        <div>
          <div
            className="card"
            style={{
              backgroundColor: "#1a1a1a",
              borderRadius: "8px",
              padding: "20px",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              marginBottom: "20px",
              border: "1px solid #374151",
            }}
          >
            <h3
              style={{
                fontSize: "18px",
                fontWeight: "600",
                marginBottom: "16px",
                color: "white",
              }}
            >
              Business Details
            </h3>
            <div style={{ display: "grid", gap: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Location</span>
                <span style={{ fontWeight: "500", color: "white" }}>{business.address}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Neighborhood</span>
                <span style={{ fontWeight: "500", color: "white" }}>
                  {business.neighborhood}
                </span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Square Footage</span>
                <span style={{ fontWeight: "500", color: "white" }}>
                  {business.sq_footage} sq ft
                </span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Contact</span>
                <span style={{ fontWeight: "500", color: "white" }}>{business.phone}</span>
              </div>
            </div>
          </div>

          <div
            className="card"
            style={{
              backgroundColor: "#1a1a1a",
              borderRadius: "8px",
              padding: "20px",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              border: "1px solid #374151",
            }}
          >
            <h3
              style={{
                fontSize: "18px",
                fontWeight: "600",
                marginBottom: "16px",
                color: "white",
              }}
            >
              Investment Opportunity
            </h3>
            <div style={{ display: "grid", gap: "12px", marginBottom: "20px" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Investment Needed</span>
                <span style={{ fontWeight: "600", color: "#34d399" }}>
                  ${Math.round(business.annual_revenue * 0.1).toLocaleString()}
                </span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Expected Return</span>
                <span style={{ fontWeight: "500", color: "#60a5fa" }}>
                  12-15% Annual
                </span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#9ca3af" }}>Investment Term</span>
                <span style={{ fontWeight: "500", color: "white" }}>24-36 months</span>
              </div>
            </div>
            <button
              style={{
                width: "100%",
                padding: "12px",
                backgroundColor: "#059669",
                color: "white",
                border: "none",
                borderRadius: "6px",
                fontWeight: "600",
                cursor: "pointer",
                transition: "all 0.2s",
              }}
              onClick={() => setShowInvestmentForm(true)}
              onMouseOver={(e) => {
                e.target.style.transform = "scale(1.02)";
                e.target.style.filter = "brightness(1.1)";
              }}
              onMouseOut={(e) => {
                e.target.style.transform = "scale(1)";
                e.target.style.filter = "brightness(1)";
              }}
            >
              Invest Now
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div
            className="card"
            style={{
              backgroundColor: "#1a1a1a",
              borderRadius: "8px",
              padding: "20px",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              marginBottom: "20px",
              border: "1px solid #374151",
            }}
          >
            <h3
              style={{
                fontSize: "18px",
                fontWeight: "600",
                marginBottom: "16px",
                color: "white",
              }}
            >
              Supply Chain Breakdown
            </h3>
            <div style={{ marginBottom: "20px" }}>
              {supplyChainData.map((item, index) => (
                <div
                  key={index}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "12px",
                    backgroundColor: "#111827",
                    borderRadius: "6px",
                    marginBottom: "8px",
                    borderLeft: `4px solid ${item.color}`,
                    border: "1px solid #374151",
                  }}
                >
                  <div>
                    <h4 style={{ fontWeight: "600", marginBottom: "4px", color: "white" }}>
                      {item.name}
                    </h4>
                    <p style={{ color: "#9ca3af", fontSize: "14px" }}>
                      {item.value}% of supply chain
                    </p>
                  </div>
                  <div
                    style={{
                      width: "16px",
                      height: "16px",
                      borderRadius: "50%",
                      backgroundColor: item.color,
                    }}
                  ></div>
                </div>
              ))}
            </div>
            <button
              style={{
                width: "100%",
                padding: "12px",
                backgroundColor: "#059669",
                color: "white",
                border: "none",
                borderRadius: "6px",
                fontWeight: "600",
                cursor: "pointer",
                transition: "all 0.2s",
                marginTop: "20px",
              }}
              onClick={() => setShowInvestmentForm(true)}
              onMouseOver={(e) => {
                e.target.style.transform = "scale(1.02)";
                e.target.style.filter = "brightness(1.1)";
              }}
              onMouseOut={(e) => {
                e.target.style.transform = "scale(1)";
                e.target.style.filter = "brightness(1)";
              }}
            >
              Invest Now
            </button>
          </div>

          <div
            className="info-box"
            style={{
              backgroundColor: "#111827",
              padding: "20px",
              borderRadius: "8px",
              marginTop: "20px",
              border: "1px solid #374151",
            }}
          >
            <h3
              style={{
                fontSize: "18px",
                fontWeight: "600",
                marginBottom: "12px",
                color: "white",
              }}
            >
              Supply Chain Impact
            </h3>
            <p
              style={{ color: "#9ca3af", fontSize: "14px", lineHeight: "1.5" }}
            >
              Investing in {business.name}'s supply chain helps strengthen local
              business relationships, improve operational efficiency, and
              support sustainable growth in the Queens community. Your
              investment directly contributes to improving inventory management,
              reducing costs, and creating more jobs in the area.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

// Get color based on revenue
const getRevenueColor = (revenue) => {
  // Define revenue thresholds
  const thresholds = {
    low: 500000,
    medium: 1000000,
    high: 1500000,
  };

  // Color scale from light to dark green
  if (revenue <= thresholds.low) {
    return "#90EE90"; // Light green
  } else if (revenue <= thresholds.medium) {
    return "#32CD32"; // Lime green
  } else if (revenue <= thresholds.high) {
    return "#228B22"; // Forest green
  } else {
    return "#006400"; // Dark green
  }
};

// Custom icon generator
const getBusinessIcon = (business) => {
  const color = getRevenueColor(business.annual_revenue);

  return L.divIcon({
    className: "custom-div-icon",
    html: `
      <div style="
        background-color: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 0 4px rgba(0,0,0,0.3);
      ">
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12],
  });
};

const BusinessOverview = ({ business, onBack }) => {
  // State variables for generating and displaying data
  const [showSupplyChain, setShowSupplyChain] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showInvestForm, setShowInvestForm] = useState(false);
  const [supplyChainData, setSupplyChainData] = useState(null);
  const [isGeneratingInvestment, setIsGeneratingInvestment] = useState(false);
  const [investmentData, setInvestmentData] = useState(null);

  // Base API URL - change this to match your FastAPI server
  const API_BASE_URL = 'http://localhost:8000';

  // Handle supply chain generation
  const handleGenerateSupplyChain = () => {
    setIsGenerating(true);
    const bus_id = business.business_id;
    
    console.log(`Calling supply chain API for business ID: ${bus_id}`);
    
    // Try both methods - query params and request body
    fetch(`${API_BASE_URL}/generate-supply-chain/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ business_id: bus_id }),
    })
    .then(response => {
      console.log('Supply chain API response status:', response.status);
      if (!response.ok) {
        console.log('Response not OK:', response.statusText);
      }
      return response.json();
    })
    .then(data => {
      console.log("Supply chain data received:", data);
      setSupplyChainData(data);
      setShowSupplyChain(true);
      setIsGenerating(false);
    })
    .catch(error => {
      console.error('Error generating supply chain:', error);
      
      // Fallback to mock data if API call fails
      const mockData = {
        supply_chain_text: "Raw Materials, Component Manufacturing, Assembly, Distribution, Retail, Consumer",
        supply_chain_list: ["Raw Materials", "Component Manufacturing", "Assembly", "Distribution", "Retail", "Consumer"]
      };
      console.log("Using mock supply chain data:", mockData);
      setSupplyChainData(mockData);
      setShowSupplyChain(true);
      setIsGenerating(false);
    });
  };
  
  // Handle investment generation
  const handleGenerateInvestment = () => {
    if (!supplyChainData || !supplyChainData.supply_chain_text) {
      console.error('No supply chain data available');
      return;
    }
    
    setIsGeneratingInvestment(true);
    
    // Prepare investment parameters
    const params = {
      supply_chain: supplyChainData.supply_chain_text,
      investment_amount: Math.round(business.annual_revenue * 0.1),
      min_investment_score: 0.60,
      risk_aversion: 2.0,
      max_weight_per_stock: 0.3
    };
    
    console.log('Calling investment API with params:', params);
    
    // Call the backend API to generate investment - with request body
    fetch(`${API_BASE_URL}/generate-investment/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    })
    .then(response => {
      console.log('Investment API response status:', response.status);
      if (!response.ok) {
        console.log('Response not OK:', response.statusText);
      }
      return response.json();
    })
    .then(data => {
      console.log("Investment data received:", data);
      setInvestmentData(data);
      setIsGeneratingInvestment(false);
    })
    .catch(error => {
      console.error('Error generating investment:', error);
      
      // Fallback to mock data
      const mockInvestmentData = {
        portfolio: [
          { ticker: "AMZN", price: 130.50, investment: 2500 },
          { ticker: "WMT", price: 165.75, investment: 2000 },
          { ticker: "TGT", price: 145.20, investment: 1500 },
          { ticker: "COST", price: 550.30, investment: 1300 },
          { ticker: "UPS", price: 180.10, investment: 1000 },
          { ticker: "FDX", price: 250.30, investment: 1000 },
          { ticker: "SHOP", price: 75.60, investment: 700 },
        ],
        total_investment: 10000,
      };
      console.log("Using mock investment data:", mockInvestmentData);
      setInvestmentData(mockInvestmentData);
      setIsGeneratingInvestment(false);
    });
  };

  return (
    <div
      className="p-4 bg-gray-100 min-h-screen"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "black",
        zIndex: 1000,
        padding: "20px",
        overflow: "auto",
      }}
    >
      {/* Back Button */}
      <button
        onClick={onBack}
        className="mb-4 text-blue-600 flex items-center gap-1"
        style={{
          background: "none",
          border: "none",
          color: "#2563eb",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          gap: "4px",
          marginBottom: "20px",
          fontSize: "14px",
        }}
      >
        ← Back to Map
      </button>

      {/* Business Header */}
      <div
        className="flex justify-between items-start mb-4 bg-white p-4 rounded-lg shadow"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "1rem",
          backgroundColor: "black",
          padding: "1rem",
          borderRadius: "0.5rem",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
          border: "1px solid #374151",
        }}
      >
        <div>
          <h2
            className="text-2xl font-semibold mb-1"
            style={{
              fontSize: "24px",
              fontWeight: "600",
              marginBottom: "8px",
              color: "white",
            }}
          >
            {business.name}
          </h2>
          <p
            className="text-gray-600 text-sm"
            style={{ color: "#9ca3af", fontSize: "14px" }}
          >
            {business.business_type} · Established {business.established}
          </p>
        </div>
        <div className="text-right" style={{ textAlign: "right" }}>
          <p
            className="text-green-600 font-semibold text-lg"
            style={{
              color: "#34d399",
              fontSize: "18px",
              fontWeight: "600",
            }}
          >
            ${business.annual_revenue.toLocaleString()} Annual Revenue
          </p>
          <p
            className="text-gray-500 text-sm"
            style={{ color: "#9ca3af", fontSize: "14px" }}
          >
            {business.employees} Employees
          </p>
        </div>
      </div>

      {/* Business Details */}
      <div
        className="bg-white p-4 rounded-lg shadow mb-4"
        style={{
          backgroundColor: "black",
          padding: "1rem",
          borderRadius: "0.5rem",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
          marginBottom: "1rem",
          border: "1px solid #374151",
        }}
      >
        <h3
          className="text-lg font-semibold mb-3"
          style={{
            fontSize: "18px",
            fontWeight: "600",
            marginBottom: "0.75rem",
            color: "white",
          }}
        >
          Business Overview
        </h3>

        <div className="grid gap-3" style={{ display: "grid", gap: "0.75rem" }}>
          <div
            className="flex justify-between"
            style={{ display: "flex", justifyContent: "space-between" }}
          >
            <span className="text-gray-600" style={{ color: "#9ca3af" }}>
              Location
            </span>
            <span className="font-medium" style={{ fontWeight: "500", color: "white" }}>
              {business.address}
            </span>
          </div>
          <div
            className="flex justify-between"
            style={{ display: "flex", justifyContent: "space-between" }}
          >
            <span className="text-gray-600" style={{ color: "#9ca3af" }}>
              Neighborhood
            </span>
            <span className="font-medium" style={{ fontWeight: "500", color: "white" }}>
              {business.neighborhood}
            </span>
          </div>
          <div
            className="flex justify-between"
            style={{ display: "flex", justifyContent: "space-between" }}
          >
            <span className="text-gray-600" style={{ color: "#9ca3af" }}>
              Square Footage
            </span>
            <span className="font-medium" style={{ fontWeight: "500", color: "white" }}>
              {business.sq_footage} sq ft
            </span>
          </div>
          <div
            className="flex justify-between"
            style={{ display: "flex", justifyContent: "space-between" }}
          >
            <span className="text-gray-600" style={{ color: "#9ca3af" }}>
              Contact
            </span>
            <span className="font-medium" style={{ fontWeight: "500", color: "white" }}>
              {business.phone}
            </span>
          </div>
          <div
            className="flex justify-between"
            style={{ display: "flex", justifyContent: "space-between" }}
          >
            <span className="text-gray-600" style={{ color: "#9ca3af" }}>
              Years in Operation
            </span>
            <span className="font-medium" style={{ fontWeight: "500", color: "white" }}>
              {new Date().getFullYear() - business.established}
            </span>
          </div>
        </div>
      </div>

      {/* Business Description */}
      <div
        className="bg-white p-4 rounded-lg shadow mb-6"
        style={{
          backgroundColor: "black",
          padding: "1rem",
          borderRadius: "0.5rem",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
          marginBottom: "1.5rem",
          border: "1px solid #374151",
        }}
      >
        <h3
          className="text-lg font-semibold mb-3"
          style={{
            fontSize: "18px",
            fontWeight: "600",
            marginBottom: "0.75rem",
            color: "white",
          }}
        >
          Business Description
        </h3>
        <p
          className="text-gray-700 mb-3 leading-relaxed"
          style={{
            color: "#9ca3af",
            marginBottom: "0.75rem",
            lineHeight: "1.6",
          }}
        >
          {business.name} is a {business.business_type.toLowerCase()} business
          located in {business.neighborhood}. With $
          {business.annual_revenue.toLocaleString()} in annual revenue and{" "}
          {business.employees} employees, it plays an important role in the
          local economy and community.
        </p>
        <p
          className="text-gray-700 leading-relaxed"
          style={{
            color: "#9ca3af",
            lineHeight: "1.6",
          }}
        >
          Established in {business.established}, this business has built a
          reputation for quality service and contributes to the character and
          economic health of the neighborhood.
        </p>
      </div>

      {/* Generate Button Section */}
      {!showSupplyChain ? (
        <div
          className="text-center my-8"
          style={{ textAlign: "center", margin: "2rem 0" }}
        >
          <p
            className="mb-4 text-gray-600"
            style={{ marginBottom: "1rem", color: "#9ca3af" }}
          >
            Generate a supply chain analysis and investment options for this
            business
          </p>
          <button
            onClick={handleGenerateSupplyChain}
            disabled={isGenerating}
            className={`py-3 px-6 rounded-lg font-semibold inline-flex items-center gap-2 ${
              isGenerating ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
            } text-white transition`}
            style={{
              padding: "0.75rem 1.5rem",
              borderRadius: "0.5rem",
              fontWeight: "600",
              display: "inline-flex",
              alignItems: "center",
              gap: "0.5rem",
              backgroundColor: isGenerating ? "#9ca3af" : "#2563eb",
              color: "white",
              transition: "all 0.2s",
              border: "none",
              cursor: isGenerating ? "default" : "pointer",
            }}
          >
            {isGenerating ? (
              <>
                <svg
                  className="animate-spin h-4 w-4 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  style={{
                    animation: "spin 1s linear infinite",
                    height: "1rem",
                    width: "1rem",
                    color: "white",
                  }}
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    style={{ opacity: 0.25 }}
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    style={{ opacity: 0.75 }}
                  ></path>
                </svg>
                Generating...
              </>
            ) : (
              "Generate Supply Chain Analysis"
            )}
          </button>
        </div>
      ) : (
        <>
          {/* Supply Chain Analysis */}
          <div
            className="bg-white p-4 rounded-lg shadow mb-6"
            style={{
              backgroundColor: "black",
              padding: "1rem",
              borderRadius: "0.5rem",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              marginBottom: "1.5rem",
              border: "1px solid #374151",
            }}
          >
            <h3
              className="text-lg font-semibold mb-4"
              style={{
                fontSize: "18px",
                fontWeight: "600",
                marginBottom: "1rem",
                color: "white",
              }}
            >
              Supply Chain Analysis
            </h3>
            
            {/* Supply Chain List */}
            {supplyChainData && supplyChainData.supply_chain_list && (
              <SupplyChainList supplyChainList={supplyChainData.supply_chain_list} />
            )}
            
            <div
              style={{
                marginTop: "1.5rem",
                padding: "1rem",
                backgroundColor: "#111827",
                borderRadius: "0.5rem",
                border: "1px solid #374151",
              }}
            >
              <h4
                style={{
                  fontSize: "16px",
                  fontWeight: "600",
                  marginBottom: "0.75rem",
                  color: "white",
                }}
              >
                Supply Chain Details
              </h4>
              <p
                style={{
                  color: "#9ca3af",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  marginBottom: "1rem",
                }}
              >
                {business.name}'s supply chain involves several key components that work together
                to deliver products/services to the end customers. Each node represents a critical
                stage in the process, from raw materials to the final consumer interaction.
              </p>
            </div>
            
            {/* Generate Investment Button */}
            {!investmentData && (
              <div style={{ textAlign: "center", marginTop: "2rem" }}>
                <button
                  onClick={handleGenerateInvestment}
                  disabled={isGeneratingInvestment}
                  style={{
                    padding: "0.75rem 1.5rem",
                    borderRadius: "0.5rem",
                    backgroundColor: isGeneratingInvestment ? "#9ca3af" : "#10b981",
                    color: "white",
                    border: "none",
                    fontWeight: "600",
                    cursor: isGeneratingInvestment ? "default" : "pointer",
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "0.5rem",
                  }}
                >
                  {isGeneratingInvestment ? (
                    <>
                      <svg
                        className="animate-spin"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        style={{
                          animation: "spin 1s linear infinite",
                          height: "1rem",
                          width: "1rem",
                        }}
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                          style={{ opacity: 0.25 }}
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          style={{ opacity: 0.75 }}
                        ></path>
                      </svg>
                      Generating Investment Portfolio...
                    </>
                  ) : (
                    "Generate Investment Portfolio"
                  )}
                </button>
              </div>
            )}
          </div>
          
          {/* Investment Portfolio Section */}
          {investmentData && (
            <EditableInvestmentPieChart 
              investmentData={investmentData} 
              setInvestmentData={setInvestmentData} 
            />
          )}
        </>
      )}
    </div>
  );
};

const MapScreen = ({ budget }) => {
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showBusinessDetails, setShowBusinessDetails] = useState(false);

  // Center coordinates for Kew Gardens Hills area
  const center = [40.7328, -73.8219];

  // Define coordinates for known business locations
  const businessCoordinates = {
    // Union St locations
    ZFSTG: [40.7352, -73.8208], // 157 Union St
    MST: [40.7358, -73.8208], // 182 Union St
    FARS: [40.7355, -73.8208], // 177 Union St

    // Main St locations
    ANDA: [40.7336, -73.8147], // 103 Main St

    // Parsons Blvd locations
    AS: [40.7332, -73.8178], // 80 Parsons Blvd

    // 150th St locations
    TSB: [40.7329, -73.8219], // 57 150th St

    // Melbourne Ave locations
    OTNPP: [40.7329, -73.8239], // 59 Melbourne Ave

    // Horace Harding Expy locations
    ARONS: [40.7352, -73.8208], // 81 Horace Harding Expy
  };

  useEffect(() => {
    const fetchBusinesses = async () => {
      try {
        // Convert the object of businesses into an array
        const businessArray = Object.entries(businessData).map(
          ([id, business]) => {
            // Get coordinates for the business or use random coordinates as fallback
            const coordinates = businessCoordinates[id] || [
              center[0] + (Math.random() - 0.5) * 0.005,
              center[1] + (Math.random() - 0.5) * 0.005,
            ];

            return {
              ...business,
              business_id: id,
              coordinates,
              investment_needed: Math.round(business.annual_revenue * 0.1),
            };
          },
        );

        setBusinesses(businessArray);
        setLoading(false);
      } catch (error) {
        console.error("Error processing business data:", error);
        setLoading(false);
      }
    };

    fetchBusinesses();
  }, []);

  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          backgroundColor: "#000000",
          color: "#ffffff",
          fontSize: "18px",
          fontWeight: "500",
        }}
      >
        Loading map data...
      </div>
    );
  }

  return (
    <div
      style={{
        padding: "20px",
        backgroundColor: "#000000",
        minHeight: "100vh",
        position: "relative",
      }}
    >
      {showBusinessDetails && selectedBusiness && (
        <BusinessOverview
          business={selectedBusiness}
          onBack={() => {
            setShowBusinessDetails(false);
            setSelectedBusiness(null);
          }}
        />
      )}

      <h1
        style={{
          marginBottom: "8px",
          textAlign: "center",
          fontSize: "42px",
          fontWeight: "800",
          fontFamily: "'Inter', 'Poppins', sans-serif",
          color: "#ffffff",
          textTransform: "none",
          letterSpacing: "-0.5px",
          marginTop: "20px",
          padding: "0 20px",
          lineHeight: "1.2",
          textShadow: "0 2px 4px rgba(0,0,0,0.1)",
        }}
      >
        Local Business Investment Opportunities
      </h1>
      <div
        style={{
          fontSize: "20px",
          fontWeight: "600",
          textAlign: "center",
          marginBottom: "20px",
          background: "linear-gradient(135deg, #ef4444, #f59e0b)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
          display: "inline-block",
          width: "100%",
        }}
      >
        Available Investment Budget: ${budget.toLocaleString()}
      </div>

      {/* Legend */}
      {!showBusinessDetails && (
        <div
          style={{
            position: "absolute",
            top: "100px",
            right: "20px",
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            padding: "15px",
            borderRadius: "8px",
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
            zIndex: 1000,
            border: "1px solid #333",
          }}
        >
          <h3
            style={{ marginBottom: "10px", fontSize: "14px", color: "#ffffff" }}
          >
            Annual Revenue
          </h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div
                style={{
                  width: "12px",
                  height: "12px",
                  backgroundColor: "#90EE90",
                  borderRadius: "50%",
                }}
              ></div>
              <span style={{ fontSize: "12px", color: "#ffffff" }}>
                Under $500K
              </span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div
                style={{
                  width: "12px",
                  height: "12px",
                  backgroundColor: "#32CD32",
                  borderRadius: "50%",
                }}
              ></div>
              <span style={{ fontSize: "12px", color: "#ffffff" }}>
                $500K - $1M
              </span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div
                style={{
                  width: "12px",
                  height: "12px",
                  backgroundColor: "#228B22",
                  borderRadius: "50%",
                }}
              ></div>
              <span style={{ fontSize: "12px", color: "#ffffff" }}>
                $1M - $1.5M
              </span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div
                style={{
                  width: "12px",
                  height: "12px",
                  backgroundColor: "#006400",
                  borderRadius: "50%",
                }}
              ></div>
              <span style={{ fontSize: "12px", color: "#ffffff" }}>
                Over $1.5M
              </span>
            </div>
          </div>
        </div>
      )}

      <div style={{ height: "85vh", width: "100%" }}>
        <style>
          {`
                  ${showBusinessDetails ? ".leaflet-control-zoom { display: none !important; }" : ""}
                `}
        </style>
        <MapContainer
          center={center}
          zoom={15}
          style={{ height: "100%", width: "100%" }}
          scrollWheelZoom={true}
          zoomControl={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {businesses.map((business) => (
            <Marker
              key={business.business_id}
              position={business.coordinates}
              icon={getBusinessIcon(business)}
              eventHandlers={{
                click: () => {
                  setSelectedBusiness(business);
                },
              }}
            >
              <Popup>
                <div
                  style={{
                    padding: "12px",
                    maxWidth: "200px",
                    textAlign: "center",
                    backgroundColor: "white",
                    borderRadius: "6px",
                  }}
                >
                  <h3
                    style={{
                      marginBottom: "8px",
                      color: "#111827",
                      fontSize: "16px",
                      fontWeight: "600",
                    }}
                  >
                    {business.name}
                  </h3>
                  <p
                    style={{
                      color: "#4b5563",
                      fontSize: "14px",
                      marginBottom: "12px",
                    }}
                  >
                    {business.address}
                  </p>
                  <button
                    style={{
                      padding: "8px 16px",
                      backgroundColor: "#10b981",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                      width: "100%",
                      transition: "all 0.2s",
                      fontWeight: "600",
                      fontSize: "14px",
                    }}
                    onClick={() => {
                      setShowBusinessDetails(true);
                    }}
                    onMouseOver={(e) => {
                      e.target.style.transform = "scale(1.02)";
                      e.target.style.filter = "brightness(1.1)";
                    }}
                    onMouseOut={(e) => {
                      e.target.style.transform = "scale(1)";
                      e.target.style.filter = "brightness(1)";
                    }}
                  >
                    Learn More
                  </button>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default MapScreen;