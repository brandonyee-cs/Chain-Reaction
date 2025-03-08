import React from "react";
import SupplyChainETFViewer from "./SupplyChainETFViewer";

const ETFDetail = ({ etf, onBack, onViewSupplyChain }) => {
  if (!etf) {
    return <div>No ETF data available</div>;
  }
  return (
    <SupplyChainETFViewer etf={etf} onBack={onBack} onViewSupplyChain={onViewSupplyChain} />
  );
};

export default ETFDetail;
