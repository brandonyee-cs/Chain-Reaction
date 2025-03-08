/*
  How run the frontend code:
  cd my-react-app
  npm i
  npm start
  */
import {
  BarChart2,
  DollarSign,
  Info,
  MapPin,
  Package,
  TrendingUp,
} from "lucide-react";
import React, { useEffect, useRef, useState } from "react";
import ETFDetail from "./ETFDetail";
import ETFPieChart from "./ETFPieChart";
import LandingPage from "./LandingPage";

const styles = `
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }

  body {
    background-color: #f1f5f9;
  }

  .app {
    min-height: 100vh;
  }

  header {
    background-color: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .header-content {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1d4ed8;
  }

  .new-investment-btn {
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .new-investment-btn:hover {
    background-color: #1d4ed8;
  }

  main {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
  }

  .nav-tabs {
    background-color: white;
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    position: relative; // added this for blue indicator transition
  }

  .nav-tab {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    cursor: pointer;
    color: #4b5563;
    border: none;
    background: none;
    font-size: 0.875rem;
    position: relative; // added this for blue indicator transition
    z-index: 1; // added this for blue indicator transition
    transition: color 0.3s ease; // added this for blue indicator transition
  }

  .nav-tab:hover {
    background-color: transparent; // added this for blue indicator transition
    color: #1d4ed8; // modified this from background-color to color
  }

  .nav-tab.active {
    background-color: transparent; // removed background
    color: #1d4ed8;
    font-weight: 500;
  }

  /* This is the sliding indicator */
  .tab-indicator {
    position: absolute;
    height: calc(100% - 1rem);
    background-color: #dbeafe;
    border-radius: 0.25rem;
    transition: left 0.3s ease, width 0.3s ease;
    z-index: 0;
    top: 0.5rem;
  }

  .investment-page {
    background-color: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .investment-header {
    margin-bottom: 1.5rem;
  }

  .filter-section {
    background-color: #f8fafc;
    padding: 1rem;
    border-radius: 0.25rem;
    margin-bottom: 1.5rem;
  }

  .filter-controls {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
  }

  .filter-dropdown {
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.25rem;
    background-color: white;
    font-size: 0.875rem;
  }

  .supplier-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    width: 100%;
  }

  .supplier-grid.centered-investment {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .supplier-grid.centered-investment .investment-card {
    width: 100%;
    max-width: 500px;
  }

  .investment-card {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  }

  .investment-card-header {
    background-color: #f8fafc;
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .risk-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .risk-low {
    background-color: #dcfce7;
    color: #166534;
  }

  .risk-medium {
    background-color: #fef3c7;
    color: #92400e;
  }

  .risk-mediumhigh {
    background-color: #fee2e2;
    color: #b91c1c;
  }

  .investment-card-details {
    padding: 1rem;
  }

  .detail-item {
    margin-bottom: 0.5rem;
    display: flex;
  }

  .detail-label {
    width: 40%;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .detail-value {
    font-weight: 500;
  }

  .investment-form {
    padding: 1rem;
    border-top: 1px solid #e5e7eb;
    background-color: #f9fafb;
  }

  .amount-input {
    margin-bottom: 1rem;
  }

  .amount-input label {
    display: block;
    margin-bottom: 0.25rem;
    font-size: 0.875rem;
    color: #4b5563;
  }

  .amount-input input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.25rem;
    font-size: 1rem;
  }

  .investment-projections {
    margin-bottom: 1rem;
    padding: 0.5rem;
    background-color: #eff6ff;
    border-radius: 0.25rem;
    font-size: 0.875rem;
  }

  .invest-confirm-btn {
    width: 100%;
    background-color: #059669;
    color: white;
    border: none;
    padding: 0.75rem;
    border-radius: 0.25rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .invest-confirm-btn:hover {
    background-color: #047857;
  }

  .card {
    background-color: white;
    border-radius: 0.5rem;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
  }

  .card-header {
    margin-bottom: 1rem;
  }

  .card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .stat-card {
    background-color: white;
    padding: 1rem;
    border-radius: 0.25rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .stat-label {
    color: #6b7280;
    font-size: 0.875rem;
    margin-bottom: 0.25rem;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: 700;
  }

  .stat-value.blue {
    color: #2563eb;
  }

  .stat-value.green {
    color: #059669;
  }

  .stat-value.purple {
    color: #7c3aed;
  }

  .business-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
  }

  .business-card {
    background-color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    border-left: 4px solid #3b82f6;
    transition: background-color 0.2s;
  }

  .business-card:hover {
    background-color: #eff6ff;
  }

  .business-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .business-name {
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .business-type {
    color: #6b7280;
    font-size: 0.875rem;
  }

  .business-address {
    color: #9ca3af;
    font-size: 0.75rem;
  }

  .impact-badge {
    background-color: #dbeafe;
    color: #1e40af;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
  }

  .supplier-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .supplier-card {
    background-color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
  }

  .supplier-info h3 {
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .supplier-product {
    color: #6b7280;
    font-size: 0.875rem;
  }

  .supplier-clients {
    color: #9ca3af;
    font-size: 0.75rem;
  }

  .supplier-metrics {
    text-align: right;
  }

  .etf-section {
    margin-top: 1.5rem;
  }

  .etf-chart-container {
    height: 300px;
    position: relative;
    margin-bottom: 1rem;
  }

  .etf-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }

  .etf-card {
    background-color: white;
    border-radius: 0.5rem;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .etf-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .etf-ticker {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .etf-value {
    font-weight: 600;
    margin-top: 0.5rem;
  }

  .etf-return {
    color: #059669;
    font-size: 0.875rem;
  }

  .etf-holdings-chart {
    margin: 1rem 0;
  }

  .holding-item {
    padding: 0.75rem;
    border-radius: 0.25rem;
    margin-bottom: 0.5rem;
    background-color: #f9fafb;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .holding-name {
    font-weight: 500;
  }

  .holding-percent {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .return-rate {
    color: #059669;
    font-weight: 600;
  }

  .risk-level {
    color: #6b7280;
    font-size: 0.75rem;
  }

  .invest-btn {
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 0.25rem 0.75rem;
    border-radius: 0.25rem;
    margin-top: 0.5rem;
    cursor: pointer;
    font-size: 0.875rem;
  }

  .invest-btn:hover {
    background-color: #1d4ed8;
  }

  .invest-btn.green {
    background-color: #059669;
  }

  .invest-btn.green:hover {
    background-color: #047857;
  }

  .back-link {
    color: #2563eb;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    margin-bottom: 1rem;
    cursor: pointer;
  }

  .back-link:hover {
    // text-decoration: underline;
  }

  .info-box {
    background-color: #eff6ff;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-top: 1.5rem;
  }

  .info-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .info-text {
    color: #4b5563;
    font-size: 0.875rem;
  }

  footer {
    border-top: 1px solid #e5e7eb;
    padding: 1rem;
    margin-top: 2rem;
    text-align: center;
  }

  .footer-text {
    color: #6b7280;
    font-size: 0.875rem;
  }

  .logout-btn {
    background-color: #ef4444;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
    margin-left: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .logout-btn:hover {
    background-color: #dc2626;
  }
  
  .header-buttons {
    display: flex;
    align-items: center;
  }
`;

// Mock data for our application
const mockLocalBusinesses = [
  {
    id: 1,
    name: "Joe's Coffee",
    type: "Cafe",
    address: "123 Main St",
    impact: 85,
  },
  {
    id: 2,
    name: "Fresh Goods Market",
    type: "Grocery",
    address: "456 Oak Ave",
    impact: 72,
  },
  {
    id: 3,
    name: "Bookworm Books",
    type: "Retail",
    address: "789 Pine Rd",
    impact: 64,
  },
  {
    id: 4,
    name: "Tech Repair Shop",
    type: "Service",
    address: "101 Elm St",
    impact: 78,
  },
];

const mockSuppliers = [
  {
    id: 1,
    name: "Bean Distributors Inc.",
    product: "Coffee Beans",
    clientIds: [1],
    returnRate: 4.2,
    riskLevel: "Low",
  },
  {
    id: 2,
    name: "Organic Produce Co.",
    product: "Fresh Produce",
    clientIds: [2],
    returnRate: 5.1,
    riskLevel: "Medium",
  },
  {
    id: 3,
    name: "Paper Products Ltd.",
    product: "Books & Stationery",
    clientIds: [3],
    returnRate: 3.8,
    riskLevel: "Low",
  },
  {
    id: 4,
    name: "Electronics Parts Supply",
    product: "Tech Components",
    clientIds: [4],
    returnRate: 6.3,
    riskLevel: "Medium-High",
  },
  {
    id: 5,
    name: "Regional Food Distributors",
    product: "Various Foods",
    clientIds: [1, 2],
    returnRate: 4.7,
    riskLevel: "Medium",
  },
];

const mockInvestments = [
  { id: 1, supplierId: 1, amount: 75, date: "2025-02-15", growth: 2.3 },
  { id: 2, supplierId: 5, amount: 150, date: "2025-01-20", growth: 4.1 },
];

const mockETFs = [
  {
    id: 1,
    name: "Local Supply Chain ETF",
    ticker: "LSCX",
    value: 250,
    allocation: 0.35,
    returnRate: 5.2,
    risk: "Medium",
    color: "#3b82f6", // blue
    holdings: [
      { name: "Bean Distributors Inc.", percentage: 25, supplierId: 1 },
      { name: "Regional Food Distributors", percentage: 20, supplierId: 5 },
      { name: "Organic Produce Co.", percentage: 18, supplierId: 2 },
      { name: "Paper Products Ltd.", percentage: 15, supplierId: 3 },
      { name: "Electronics Parts Supply", percentage: 12, supplierId: 4 },
      { name: "Other Holdings", percentage: 10, supplierId: null },
    ],
    // The supply chain data is now handled in the SupplyChainETFViewer component
  },
  // Other ETFs remain the same...
];


const App = () => {
  const [showLandingPage, setShowLandingPage] = useState(true);
  const [showInvestPage, setShowInvestPage] = useState(false);
  const [selectedSupplier, setSelectedSupplier] = useState(null);
  const [selectedETF, setSelectedETF] = useState(null);
  const [currentTab, setCurrentTab] = useState("dashboard");
  const [indicatorStyle, setIndicatorStyle] = useState({});
  const [selectedBusiness, setSelectedBusiness] = useState(null);

  const dashboardRef = useRef(null);
  const exploreRef = useRef(null);
  const portfolioRef = useRef(null);
  const learnRef = useRef(null);

  const handleLogin = () => {
    setShowLandingPage(false);
  };

  const handleOpenInvestPage = (supplier = null) => {
    setSelectedSupplier(supplier);
    setShowInvestPage(true);
  };

  // Update the indicator position when tab changes
  useEffect(() => {
    let activeTabRef;

    switch (currentTab) {
      case "dashboard":
        activeTabRef = dashboardRef;
        break;
      case "explore":
        activeTabRef = exploreRef;
        break;
      case "portfolio":
        activeTabRef = portfolioRef;
        break;
      case "learn":
        activeTabRef = learnRef;
        break;
      default:
        activeTabRef = dashboardRef;
    }
    if (activeTabRef && activeTabRef.current) {
      const { offsetLeft, offsetWidth } = activeTabRef.current;
      setIndicatorStyle({
        left: `${offsetLeft}px`,
        width: `${offsetWidth}px`,
      });
    }
  }, [currentTab]); // Only currentTab as dependency

  // Calculate total investment and impact
  const totalInvested = mockInvestments.reduce(
    (sum, inv) => sum + inv.amount,
    0,
  );
  const investmentGrowth = mockInvestments.reduce(
    (sum, inv) => sum + (inv.amount * inv.growth) / 100,
    0,
  );
  const businessesImpacted = [
    ...new Set(
      mockInvestments.flatMap(
        (inv) =>
          mockSuppliers.find((s) => s.id === inv.supplierId)?.clientIds || [],
      ),
    ),
  ].length;

  // Get details for business view
  const getBusinessSuppliers = (businessId) => {
    return mockSuppliers.filter((supplier) =>
      supplier.clientIds.includes(businessId),
    );
  };

  const handleBusinessClick = (business) => {
    setSelectedBusiness(business);
    setCurrentTab("businessDetail");
  };

  if (showLandingPage) {
    return <LandingPage onLogin={handleLogin} />;
  }

  const renderDashboard = () => (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Your Investment Impact</h2>
        </div>
        <div className="stats-grid">
          <div className="stat-card">
            <p className="stat-label">Total Invested</p>
            <p className="stat-value blue">${totalInvested}</p>
          </div>
          <div className="stat-card">
            <p className="stat-label">Current Returns</p>
            <p className="stat-value green">
              <TrendingUp
                size={16}
                style={{ verticalAlign: "middle", marginRight: "4px" }}
              />{" "}
              +${investmentGrowth.toFixed(2)}
            </p>
          </div>
          <div className="stat-card">
            <p className="stat-label">Businesses Impacted</p>
            <p className="stat-value purple">{businessesImpacted}</p>
          </div>
        </div>
      </div>

      <div>
        <h2 className="card-title">Local Businesses</h2>
        <div className="business-grid">
          {mockLocalBusinesses.map((business) => (
            <div
              key={business.id}
              className="business-card"
              onClick={() => handleBusinessClick(business)}
            >
              <div className="business-header">
                <div>
                  <h3 className="business-name">{business.name}</h3>
                  <p className="business-type">{business.type}</p>
                  <p className="business-address">{business.address}</p>
                </div>
                <div className="impact-badge">{business.impact}% Impact</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card" style={{ marginTop: "1.5rem" }}>
        <h2 className="card-title">Investment Opportunities</h2>
        <div className="supplier-list">
          {mockSuppliers.map((supplier) => (
            <div key={supplier.id} className="supplier-card">
              <div className="supplier-info">
                <h3>
                  <Package
                    size={16}
                    style={{ verticalAlign: "middle", marginRight: "8px" }}
                  />{" "}
                  {supplier.name}
                </h3>
                <p className="supplier-product">Supplies: {supplier.product}</p>
                <p className="supplier-clients">
                  Serves:{" "}
                  {supplier.clientIds
                    .map(
                      (id) =>
                        mockLocalBusinesses.find((b) => b.id === id)?.name,
                    )
                    .join(", ")}
                </p>
              </div>
              <div className="supplier-metrics">
                <p className="return-rate">
                  {supplier.returnRate}% Est. Return
                </p>
                <p className="risk-level">{supplier.riskLevel} Risk</p>
                <button
                  className="invest-btn"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent other click events
                    handleOpenInvestPage(supplier);
                  }}
                >
                  Invest Now
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderInvestmentPage = () => {
    return (
      <div className="investment-page">
        <div className="investment-header">
          <button
            onClick={() => setShowInvestPage(false)}
            className="back-link"
          >
            ← Back to Dashboard
          </button>
          <h2 className="card-title">
            {selectedSupplier
              ? `Invest in ${selectedSupplier.name}`
              : "New Investment Opportunity"}
          </h2>
        </div>

        <div className="investment-options">
          {!selectedSupplier && (
            <div className="filter-section">
              <p>Filter by:</p>
              <div className="filter-controls">
                <select className="filter-dropdown">
                  <option value="">All Risk Levels</option>
                  <option value="Low">Low Risk</option>
                  <option value="Medium">Medium Risk</option>
                  <option value="Medium-High">Medium-High Risk</option>
                </select>

                <select className="filter-dropdown">
                  <option value="">All Product Types</option>
                  <option value="Food">Food & Beverages</option>
                  <option value="Tech">Technology</option>
                  <option value="Paper">Paper Products</option>
                </select>
              </div>
            </div>
          )}

          <div
            className={`supplier-grid ${selectedSupplier ? "centered-investment" : ""}`}
          >
            {(selectedSupplier ? [selectedSupplier] : mockSuppliers).map(
              (supplier) => (
                <div key={supplier.id} className="investment-card">
                  <div className="investment-card-header">
                    <h3>{supplier.name}</h3>
                    <span
                      className={`risk-badge risk-${supplier.riskLevel.toLowerCase().replace("-", "")}`}
                    >
                      {supplier.riskLevel} Risk
                    </span>
                  </div>

                  <div className="investment-card-details">
                    <div className="detail-item">
                      <span className="detail-label">Product:</span>
                      <span className="detail-value">{supplier.product}</span>
                    </div>

                    <div className="detail-item">
                      <span className="detail-label">Clients:</span>
                      <span className="detail-value">
                        {supplier.clientIds
                          .map(
                            (id) =>
                              mockLocalBusinesses.find((b) => b.id === id)
                                ?.name,
                          )
                          .join(", ")}
                      </span>
                    </div>

                    <div className="detail-item">
                      <span className="detail-label">Est. Return:</span>
                      <span className="detail-value return-rate">
                        {supplier.returnRate}%
                      </span>
                    </div>
                  </div>

                  <div className="investment-form">
                    <div className="amount-input">
                      <label htmlFor={`amount-${supplier.id}`}>
                        Investment Amount ($):
                      </label>
                      <input
                        type="number"
                        id={`amount-${supplier.id}`}
                        min="10"
                        step="5"
                        defaultValue={selectedSupplier ? "100" : "50"}
                      />
                    </div>

                    <div className="investment-projections">
                      <p>
                        Projected 1-year return:{" "}
                        <strong>
                          ${((50 * supplier.returnRate) / 100).toFixed(2)}
                        </strong>
                      </p>
                    </div>

                    <button className="invest-confirm-btn">
                      Confirm Investment
                    </button>
                  </div>
                </div>
              ),
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderBusinessDetail = () => {
    if (!selectedBusiness) return null;

    const suppliers = getBusinessSuppliers(selectedBusiness.id);

    return (
      <div>
        <button onClick={() => setCurrentTab("dashboard")} className="back-link">
          ← Back to Dashboard
        </button>

        <div className="card">
          <h2 className="card-title">{selectedBusiness.name}</h2>
          <p className="business-type">
            {selectedBusiness.type} • {selectedBusiness.address}
          </p>

          <div
            style={{
              marginTop: "1rem",
              padding: "0.75rem",
              backgroundColor: "#eff6ff",
              borderRadius: "0.25rem",
            }}
          >
            <p style={{ fontSize: "0.875rem", color: "#1e40af" }}>
              Community Impact Score:{" "}
              <strong>{selectedBusiness.impact}%</strong>
            </p>
          </div>
        </div>

        <div style={{ marginTop: "1.5rem" }}>
          <h3 className="card-title">Supply Chain</h3>
          {suppliers.length > 0 ? (
            <div className="supplier-list">
              {suppliers.map((supplier) => (
                <div
                  key={supplier.id}
                  className="supplier-card"
                  style={{ borderLeft: "4px solid #059669" }}
                >
                  <div>
                    <h4 style={{ fontWeight: 600 }}>{supplier.name}</h4>
                    <p className="supplier-product">
                      Supplies: {supplier.product}
                    </p>
                  </div>
                  <div className="supplier-metrics">
                    <p className="return-rate">
                      {supplier.returnRate}% Est. Return
                    </p>
                    <button
                      className="invest-btn green"
                      onClick={(e) => {
                        e.stopPropagation(); // Prevent other click events
                        handleOpenInvestPage(supplier);
                      }}
                    >
                      Invest
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: "#6b7280", fontStyle: "italic" }}>
              No supplier data available
            </p>
          )}
        </div>

        <div className="info-box">
          <h3 className="info-title">How Your Investment Helps</h3>
          <p className="info-text">
            Investing in suppliers for {selectedBusiness.name} helps them secure
            inventory at better rates, improves supply chain reliability, and
            contributes to local economic growth.
          </p>
        </div>
      </div>
    );
  };

  const renderPortfolio = () => {
    // Calculate values
    const totalETFValue = mockETFs.reduce((sum, etf) => sum + etf.value, 0);
    const totalPortfolioValue = totalInvested + totalETFValue;

    return (
      <div>
        {selectedETF ? (
          <div className="card">
            <ETFDetail
              etf={selectedETF}
              onBack={() => setSelectedETF(null)}
              onViewSupplyChain={(supplierId) => {
                // Find the supplier
                const supplier = mockSuppliers.find((s) => s.id === supplierId);
                if (supplier) {
                  handleOpenInvestPage(supplier);
                }
              }}
            />
          </div>
        ) : (
          <>
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">Your Portfolio</h2>
              </div>
              <div className="stats-grid">
                <div className="stat-card">
                  <p className="stat-label">Total Invested</p>
                  <p className="stat-value blue">
                    ${totalPortfolioValue.toFixed(2)}
                  </p>
                </div>
                <div className="stat-card">
                  <p className="stat-label">Current Value</p>
                  <p className="stat-value green">
                    ${(totalPortfolioValue + investmentGrowth).toFixed(2)}
                  </p>
                </div>
                <div className="stat-card">
                  <p className="stat-label">Total Return</p>
                  <p className="stat-value purple">
                    +
                    {((investmentGrowth / totalPortfolioValue) * 100).toFixed(
                      1,
                    )}
                    %
                  </p>
                </div>
              </div>
            </div>

            <div className="card" style={{ marginTop: "1.5rem" }}>
              <h2 className="card-title">ETF Allocation</h2>
              <p
                style={{
                  marginBottom: "1rem",
                  color: "#6b7280",
                  fontSize: "0.875rem",
                }}
              >
                Click on a segment to view ETF details and holdings
              </p>
              <ETFPieChart etfs={mockETFs} onSelectETF={setSelectedETF} />
            </div>

            <div style={{ marginTop: "1.5rem" }}>
              <h2 className="card-title">Direct Investments</h2>
              {mockInvestments.length > 0 ? (
                <div className="supplier-list">
                  {mockInvestments.map((investment) => {
                    const supplier = mockSuppliers.find(
                      (s) => s.id === investment.supplierId,
                    );
                    return (
                      <div
                        key={investment.id}
                        className="supplier-card"
                        style={{ borderLeft: "4px solid #059669" }}
                      >
                        <div>
                          <h3 style={{ fontWeight: 600 }}>{supplier?.name}</h3>
                          <p className="supplier-product">
                            Invested: ${investment.amount}
                          </p>
                          <p className="supplier-clients">
                            Date: {investment.date}
                          </p>
                        </div>
                        <div className="supplier-metrics">
                          <p className="return-rate">
                            +$
                            {(
                              (investment.amount * investment.growth) /
                              100
                            ).toFixed(2)}
                          </p>
                          <p className="risk-level">
                            +{investment.growth}% Growth
                          </p>
                          <button className="invest-btn">Add More</button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p style={{ color: "#6b7280", fontStyle: "italic" }}>
                  No direct investments yet
                </p>
              )}
            </div>
          </>
        )}
      </div>
    );
  };

  const renderExplore = () => (
    <div>
      <div
        style={{
          backgroundColor: "#f8fafc",
          padding: "1rem",
          borderRadius: "0.5rem",
        }}
      >
        <h2 className="card-title">Explore Supply Chains</h2>
        <p style={{ color: "#4b5563", marginBottom: "1rem" }}>
          Discover how local businesses are connected to their suppliers and
          make strategic investments that strengthen the entire supply chain
          ecosystem.
        </p>

        <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
          <select
            style={{
              border: "1px solid #d1d5db",
              borderRadius: "0.25rem",
              padding: "0.5rem",
              fontSize: "0.875rem",
            }}
          >
            <option>All Industries</option>
            <option>Food & Beverage</option>
            <option>Retail</option>
            <option>Services</option>
          </select>

          <select
            style={{
              border: "1px solid #d1d5db",
              borderRadius: "0.25rem",
              padding: "0.5rem",
              fontSize: "0.875rem",
            }}
          >
            <option>Sort by Impact</option>
            <option>Sort by Return</option>
            <option>Sort by Risk</option>
          </select>
        </div>
      </div>

      <div className="card" style={{ marginTop: "1.5rem" }}>
        <h3
          style={{
            fontSize: "1.125rem",
            fontWeight: "600",
            marginBottom: "0.75rem",
          }}
        >
          Supply Chain Map
        </h3>
        <div
          style={{
            height: "16rem",
            backgroundColor: "#eff6ff",
            borderRadius: "0.25rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <p style={{ color: "#6b7280" }}>
            Interactive supply chain map visualization would appear here
          </p>
        </div>
      </div>

      <div style={{ marginTop: "1.5rem" }}>
        <h3
          style={{
            fontSize: "1.125rem",
            fontWeight: "600",
            marginBottom: "0.75rem",
          }}
        >
          Top Investment Opportunities
        </h3>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
            gap: "1rem",
          }}
        >
          {mockSuppliers.slice(0, 4).map((supplier) => (
            <div key={supplier.id} className="business-card">
              <h4 style={{ fontWeight: "600" }}>{supplier.name}</h4>
              <p className="business-type">Supplies: {supplier.product}</p>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "0.5rem",
                }}
              >
                <span style={{ color: "#2563eb", fontSize: "0.875rem" }}>
                  {supplier.returnRate}% Return
                </span>
                <span style={{ color: "#6b7280", fontSize: "0.875rem" }}>
                  {supplier.riskLevel} Risk
                </span>
              </div>
              <button
                className="invest-btn"
                style={{
                  width: "100%",
                  marginTop: "0.75rem",
                  padding: "0.25rem 0",
                }}
              >
                View Details
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="app">
      <style>{styles}</style>
      <header>
        <div className="header-content">
          <h1 className="logo">Supply Chain Invest App</h1>
          <div className="header-buttons">
            <button
              className="new-investment-btn"
              onClick={() => handleOpenInvestPage()}
            >
              + New Investment
            </button>
            <button
              className="logout-btn"
              onClick={() => setShowLandingPage(true)}
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main>
        {showInvestPage ? (
          renderInvestmentPage()
        ) : currentTab === "businessDetail" ? (
          renderBusinessDetail()
        ) : (
          <>
            <nav className="nav-tabs">
              {/* This is the sliding indicator */}
              <div className="tab-indicator" style={indicatorStyle} />

              <button
                ref={dashboardRef}
                onClick={() => setCurrentTab("dashboard")}
                className={`nav-tab ${currentTab === "dashboard" ? "active" : ""}`}
              >
                <BarChart2 size={18} />
                <span>Dashboard</span>
              </button>
              <button
                ref={exploreRef}
                onClick={() => setCurrentTab("explore")}
                className={`nav-tab ${currentTab === "explore" ? "active" : ""}`}
              >
                <MapPin size={18} />
                <span>Explore</span>
              </button>
              <button
                ref={portfolioRef}
                onClick={() => setCurrentTab("portfolio")}
                className={`nav-tab ${currentTab === "portfolio" ? "active" : ""}`}
              >
                <DollarSign size={18} />
                <span>Portfolio</span>
              </button>
              <button
                ref={learnRef}
                onClick={() => setCurrentTab("learn")}
                className={`nav-tab ${currentTab === "learn" ? "active" : ""}`}
              >
                <Info size={18} />
                <span>Learn</span>
              </button>
            </nav>

            {currentTab === "dashboard" && renderDashboard()}
            {currentTab === "portfolio" && renderPortfolio()}
            {currentTab === "explore" && renderExplore()}
            {currentTab === "learn" && (
              <div className="card">
                <h2 className="card-title">How It Works</h2>
                <p style={{ color: "#4b5563", marginBottom: "1rem" }}>
                  Learn about how your investments in supply chains can make a
                  difference for local businesses.
                </p>
                <p style={{ color: "#6b7280", fontStyle: "italic" }}>
                  Educational content would go here
                </p>
              </div>
            )}
          </>
        )}
      </main>

      <footer>
        <div className="footer-text">
          © 2025 SupplyChain Invest - A Capital One Hackathon Project
        </div>
      </footer>
    </div>
  );
};

export default App;
