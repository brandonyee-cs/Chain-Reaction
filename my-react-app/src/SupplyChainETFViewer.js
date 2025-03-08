// To integrate this with your existing application, you'll need to update or add these files:

// 1. Create a new file: SupplyChainETFViewer.js
import React, { useState } from "react";
import { Cell, Legend, Pie, PieChart, Tooltip } from "recharts";

// Mock data for supply chain visualization
const mockETFSupplyChain = {
  1: [ // For ETF ID 1 - Local Supply Chain ETF
    { name: "Raw Materials", value: 35, color: "#10b981" },
    { name: "Manufacturing", value: 25, color: "#f59e0b" },
    { name: "Distribution", value: 30, color: "#8b5cf6" },
    { name: "Retail", value: 10, color: "#ef4444" }
  ],
  2: [ // For ETF ID 2 - Sustainable Food Chain
    { name: "Farm Production", value: 40, color: "#10b981" },
    { name: "Processing", value: 30, color: "#f59e0b" },
    { name: "Distribution", value: 20, color: "#8b5cf6" },
    { name: "Retail", value: 10, color: "#ef4444" }
  ],
  3: [ // For ETF ID 3 - Tech Supply Innovation
    { name: "Component Sourcing", value: 35, color: "#10b981" },
    { name: "Assembly", value: 40, color: "#f59e0b" },
    { name: "Distribution", value: 15, color: "#8b5cf6" },
    { name: "Direct Sales", value: 10, color: "#ef4444" }
  ],
  4: [ // For ETF ID 4 - Retail Supply Network
    { name: "Wholesale", value: 45, color: "#10b981" },
    { name: "Logistics", value: 25, color: "#f59e0b" },
    { name: "Retail Operations", value: 30, color: "#8b5cf6" }
  ]
};

const SupplyChainETFViewer = ({ etf, onBack, onViewSupplyChain }) => {
  const [activeView, setActiveView] = useState('holdings');
  
  if (!etf) return null;
  
  // Define onViewSupplyChain if it's not provided as a prop
  const viewSupplyChain = onViewSupplyChain || ((supplierId) => {
    console.log(`Viewing supply chain for supplier ID: ${supplierId}`);
    alert(`Viewing supply chain for supplier ID: ${supplierId}`);
  });
  
  const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"];
  
  // Format holdings data for the pie chart
  const holdingsData = etf.holdings.map(holding => ({
    name: holding.name,
    value: holding.percentage,
    supplierId: holding.supplierId
  }));
  
  // Get supply chain data for this ETF
  const supplyChainData = mockETFSupplyChain[etf.id] || [];

  // Custom tooltip for charts
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div
          style={{
            backgroundColor: "white",
            padding: "10px",
            border: "1px solid #ccc",
            borderRadius: "4px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.15)",
          }}
        >
          <p>
            <strong>{data.name}</strong>
          </p>
          <p>{data.value}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <button onClick={onBack} className="back-link">
        ← Back to Portfolio Overview
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
          <h2 className="card-title">
            {etf.name} ({etf.ticker})
          </h2>
          <p>
            Risk Level:{" "}
            <span
              className={`risk-badge risk-${etf.risk.toLowerCase().replace("-", "")}`}
            >
              {etf.risk}
            </span>
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <p className="stat-value green">{etf.returnRate}% Return Rate</p>
          <p style={{ color: "#6b7280", fontSize: "0.875rem" }}>
            Value: ${etf.value}
          </p>
        </div>
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <div style={{ 
          display: "flex", 
          gap: "1rem", 
          marginBottom: "1rem",
          background: "#f1f5f9",
          padding: "0.5rem",
          borderRadius: "0.5rem"
        }}>
          <button 
            onClick={() => setActiveView('holdings')}
            style={{
              padding: "0.5rem 1rem",
              borderRadius: "0.25rem",
              background: activeView === 'holdings' ? "#2563eb" : "white",
              color: activeView === 'holdings' ? "white" : "#1f2937",
              border: "none",
              fontWeight: "500",
              cursor: "pointer"
            }}
          >
            Holdings Distribution
          </button>
          <button 
            onClick={() => setActiveView('supplyChain')}
            style={{
              padding: "0.5rem 1rem",
              borderRadius: "0.25rem",
              background: activeView === 'supplyChain' ? "#2563eb" : "white",
              color: activeView === 'supplyChain' ? "white" : "#1f2937",
              border: "none",
              fontWeight: "500",
              cursor: "pointer"
            }}
          >
            Supply Chain View
          </button>
        </div>

        <h3 className="card-title">
          {activeView === 'holdings' ? 'ETF Holdings' : 'Supply Chain Distribution'}
        </h3>
        
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "300px",
            marginBottom: "1.5rem",
          }}
        >
          <PieChart width={500} height={300}>
            <Pie
              data={activeView === 'holdings' ? holdingsData : supplyChainData}
              cx={250}
              cy={150}
              labelLine={false}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {(activeView === 'holdings' ? holdingsData : supplyChainData).map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={
                    activeView === 'supplyChain' && entry.color 
                      ? entry.color 
                      : COLORS[index % COLORS.length]
                  } 
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend />
          </PieChart>
        </div>
      </div>

      {activeView === 'holdings' && (
        <div className="supplier-list">
          <h3 className="card-title">Holdings Breakdown</h3>
          {etf.holdings.map((holding, index) => (
            <div key={index} className="supplier-card">
              <div>
                <h4 style={{ fontWeight: 600 }}>{holding.name}</h4>
                <p className="supplier-product">{holding.percentage}% of fund</p>
              </div>
              <div className="supplier-metrics">
                {holding.supplierId && (
                  <button
                    className="invest-btn"
                    onClick={() => viewSupplyChain(holding.supplierId)}
                  >
                    View Supply Chain
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeView === 'supplyChain' && (
        <div className="supplier-list">
          <h3 className="card-title">Supply Chain Components</h3>
          {supplyChainData.map((component, index) => (
            <div key={index} className="supplier-card" style={{ borderLeft: `4px solid ${component.color}` }}>
              <div>
                <h4 style={{ fontWeight: 600 }}>{component.name}</h4>
                <p className="supplier-product">{component.value}% of supply chain</p>
              </div>
              <div className="supplier-metrics">
                <div style={{ 
                  width: "16px", 
                  height: "16px", 
                  borderRadius: "50%", 
                  backgroundColor: component.color 
                }}></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SupplyChainETFViewer;
