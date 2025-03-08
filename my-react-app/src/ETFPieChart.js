import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const ETFPieChart = ({ etfs = [], onSelectETF }) => {
  if (!etfs || etfs.length === 0) {
    return <div>No ETF data available</div>;
  }

  // Format data for Recharts
  const data = etfs.map((etf) => ({
    name: etf.name,
    value: etf.value,
    color: etf.color,
    ...etf, // Pass all ETF properties
  }));

  const handleClick = (entry, index) => {
    if (onSelectETF && index !== undefined) {
      onSelectETF(etfs[index]);
    }
    
  };

  // Custom tooltip
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
            boxShadow: "0 2px 5px rgba(0, 0, 0, 0.15)",
          }}
        >
          <p>
            <strong>{data.name}</strong>
          </p>
          <p>Value: ${data.value}</p>
          <p>Return Rate: {data.returnRate}%</p>
          <p>Risk: {data.risk}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div
      className="etf-pie-chart"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: "100%",
      }}
    >
      <h2 className="card-title">ETF Portfolio Allocation</h2>
      <div style={{ height: "300px", display:'flex', justifyContent:'center' }}>
        <PieChart width={500} height={300}>
          <Pie
            data={data}
            cx={250}
            cy={150}
            labelLine={false}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
            onClick={handleClick}
            cursor="pointer"
          >
            {data &&
              data.map((currentEntry, i) => (
                <Cell
                  key={`cell-${i}`}
                  fill={currentEntry.color || "#8884d8"}
                />
              ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </div>
    </div>
  );
};

export default ETFPieChart;
