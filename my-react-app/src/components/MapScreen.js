import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import React, { useEffect, useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import businessData from '../data/small_business_data.json';

// Business Details Component
const BusinessDetailsView = ({ business, onBack }) => {
  const [activeView, setActiveView] = useState('overview');
  const [showInvestmentForm, setShowInvestmentForm] = useState(false);
  
  // Mock supply chain data
  const supplyChainData = [
    { name: "Raw Materials", value: 35, color: "#10b981" },
    { name: "Equipment", value: 25, color: "#f59e0b" },
    { name: "Services", value: 30, color: "#8b5cf6" },
    { name: "Distribution", value: 10, color: "#ef4444" }
  ];

  const InvestmentForm = () => (
    <div style={{
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      backgroundColor: 'white',
      padding: '2rem',
      borderRadius: '8px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)',
      width: '90%',
      maxWidth: '500px',
      zIndex: 2000
    }}>
      <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>
        Invest in {business.name}
      </h2>
      
      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ display: 'block', marginBottom: '0.5rem', color: '#4b5563' }}>
          Investment Amount ($)
        </label>
        <input
          type="number"
          defaultValue={Math.round(business.annual_revenue * 0.1)}
          min="100"
          step="100"
          style={{
            width: '100%',
            padding: '0.75rem',
            border: '1px solid #d1d5db',
            borderRadius: '0.375rem',
            fontSize: '1rem'
          }}
        />
      </div>

      <div style={{
        backgroundColor: '#f0f9ff',
        padding: '1rem',
        borderRadius: '0.5rem',
        marginBottom: '1.5rem'
      }}>
        <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem', color: '#0369a1' }}>
          Investment Summary
        </h3>
        <p style={{ color: '#4b5563', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
          Expected Return: 12-15% Annual
        </p>
        <p style={{ color: '#4b5563', fontSize: '0.875rem' }}>
          Term: 24-36 months
        </p>
      </div>

      <div style={{ display: 'flex', gap: '1rem' }}>
        <button
          onClick={() => setShowInvestmentForm(false)}
          style={{
            padding: '0.75rem 1rem',
            borderRadius: '0.375rem',
            border: '1px solid #d1d5db',
            backgroundColor: 'white',
            color: '#4b5563',
            fontWeight: '500',
            cursor: 'pointer',
            flex: 1
          }}
        >
          Cancel
        </button>
        <button
          onClick={() => {
            alert('Investment submitted successfully!');
            setShowInvestmentForm(false);
          }}
          style={{
            padding: '0.75rem 1rem',
            borderRadius: '0.375rem',
            backgroundColor: '#059669',
            color: 'white',
            border: 'none',
            fontWeight: '500',
            cursor: 'pointer',
            flex: 1
          }}
        >
          Confirm Investment
        </button>
      </div>
    </div>
  );

  return (
    <div className="business-details" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'white',
      zIndex: 1000,
      padding: '20px',
      overflow: 'auto'
    }}>
      {showInvestmentForm && <InvestmentForm />}
      
      <button 
        onClick={onBack}
        style={{
          background: 'none',
          border: 'none',
          color: '#2563eb',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          marginBottom: '20px',
          fontSize: '14px'
        }}
      >
        ← Back to Map
      </button>

      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        marginBottom: "1rem",
      }}>
        <div>
          <h2 style={{ 
            fontSize: '24px',
            fontWeight: '600',
            marginBottom: '8px'
          }}>
            {business.name}
          </h2>
          <p style={{ color: '#666', fontSize: '14px' }}>
            {business.business_type} · Established {business.established}
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <p style={{ 
            color: '#059669',
            fontSize: '18px',
            fontWeight: '600'
          }}>
            ${business.annual_revenue.toLocaleString()} Annual Revenue
          </p>
          <p style={{ color: '#6b7280', fontSize: '14px' }}>
            {business.employees} Employees
          </p>
        </div>
      </div>

      <div style={{ 
        display: "flex", 
        gap: "1rem", 
        marginBottom: "1rem",
        background: "#f1f5f9",
        padding: "0.5rem",
        borderRadius: "0.5rem"
      }}>
        <button 
          onClick={() => setActiveView('overview')}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "0.25rem",
            background: activeView === 'overview' ? "#2563eb" : "white",
            color: activeView === 'overview' ? "white" : "#1f2937",
            border: "none",
            fontWeight: "500",
            cursor: "pointer"
          }}
        >
          Business Overview
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
          Supply Chain
        </button>
      </div>

      {activeView === 'overview' ? (
        <div>
          <div className="card" style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '20px'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>
              Business Details
            </h3>
            <div style={{ display: 'grid', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Location</span>
                <span style={{ fontWeight: '500' }}>{business.address}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Neighborhood</span>
                <span style={{ fontWeight: '500' }}>{business.neighborhood}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Square Footage</span>
                <span style={{ fontWeight: '500' }}>{business.sq_footage} sq ft</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Contact</span>
                <span style={{ fontWeight: '500' }}>{business.phone}</span>
              </div>
            </div>
          </div>

          <div className="card" style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>
              Investment Opportunity
            </h3>
            <div style={{ display: 'grid', gap: '12px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Investment Needed</span>
                <span style={{ fontWeight: '600', color: '#059669' }}>
                  ${Math.round(business.annual_revenue * 0.1).toLocaleString()}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Expected Return</span>
                <span style={{ fontWeight: '500', color: '#2563eb' }}>12-15% Annual</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Investment Term</span>
                <span style={{ fontWeight: '500' }}>24-36 months</span>
              </div>
            </div>
            <button
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: '#059669',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onClick={() => setShowInvestmentForm(true)}
              onMouseOver={(e) => {
                e.target.style.transform = 'scale(1.02)';
                e.target.style.filter = 'brightness(1.1)';
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'scale(1)';
                e.target.style.filter = 'brightness(1)';
              }}
            >
              Invest Now
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="card" style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '20px'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>
              Supply Chain Breakdown
            </h3>
            <div style={{ marginBottom: '20px' }}>
              {supplyChainData.map((item, index) => (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '12px',
                    backgroundColor: '#f8f9fa',
                    borderRadius: '6px',
                    marginBottom: '8px',
                    borderLeft: `4px solid ${item.color}`
                  }}
                >
                  <div>
                    <h4 style={{ fontWeight: '600', marginBottom: '4px' }}>{item.name}</h4>
                    <p style={{ color: '#666', fontSize: '14px' }}>{item.value}% of supply chain</p>
                  </div>
                  <div style={{
                    width: '16px',
                    height: '16px',
                    borderRadius: '50%',
                    backgroundColor: item.color
                  }}></div>
                </div>
              ))}
            </div>
            <button
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: '#059669',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s',
                marginTop: '20px'
              }}
              onClick={() => setShowInvestmentForm(true)}
              onMouseOver={(e) => {
                e.target.style.transform = 'scale(1.02)';
                e.target.style.filter = 'brightness(1.1)';
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'scale(1)';
                e.target.style.filter = 'brightness(1)';
              }}
            >
              Invest Now
            </button>
          </div>

          <div className="info-box" style={{
            backgroundColor: '#f0f9ff',
            padding: '20px',
            borderRadius: '8px',
            marginTop: '20px'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>
              Supply Chain Impact
            </h3>
            <p style={{ color: '#4b5563', fontSize: '14px', lineHeight: '1.5' }}>
              Investing in {business.name}'s supply chain helps strengthen local business relationships,
              improve operational efficiency, and support sustainable growth in the Queens community.
              Your investment directly contributes to improving inventory management, reducing costs,
              and creating more jobs in the area.
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
    high: 1500000
  };

  // Color scale from light to dark green
  if (revenue <= thresholds.low) {
    return '#90EE90'; // Light green
  } else if (revenue <= thresholds.medium) {
    return '#32CD32'; // Lime green
  } else if (revenue <= thresholds.high) {
    return '#228B22'; // Forest green
  } else {
    return '#006400'; // Dark green
  }
};

// Custom icon generator
const getBusinessIcon = (business) => {
  const color = getRevenueColor(business.annual_revenue);
  
  return L.divIcon({
    className: 'custom-div-icon',
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
    'ZFSTG': [40.7352, -73.8208], // 157 Union St
    'MST': [40.7358, -73.8208],   // 182 Union St
    'FARS': [40.7355, -73.8208],  // 177 Union St
    
    // Main St locations
    'ANDA': [40.7336, -73.8147],  // 103 Main St
    
    // Parsons Blvd locations
    'AS': [40.7332, -73.8178],    // 80 Parsons Blvd
    
    // 150th St locations
    'TSB': [40.7329, -73.8219],   // 57 150th St
    
    // Melbourne Ave locations
    'OTNPP': [40.7329, -73.8239], // 59 Melbourne Ave
    
    // Horace Harding Expy locations
    'ARONS': [40.7352, -73.8208]  // 81 Horace Harding Expy
  };

  useEffect(() => {
    const fetchBusinesses = async () => {
      try {
        // Convert the object of businesses into an array
        const businessArray = Object.entries(businessData).map(([id, business]) => {
          // Get coordinates for the business or use random coordinates as fallback
          const coordinates = businessCoordinates[id] || [
            center[0] + (Math.random() - 0.5) * 0.005,
            center[1] + (Math.random() - 0.5) * 0.005
          ];
          
          return {
            ...business,
            business_id: id,
            coordinates,
            investment_needed: Math.round(business.annual_revenue * 0.1)
          };
        });
        
        setBusinesses(businessArray);
        setLoading(false);
      } catch (error) {
        console.error('Error processing business data:', error);
        setLoading(false);
      }
    };

    fetchBusinesses();
  }, []);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: 'white'
      }}>
        Loading map data...
      </div>
    );
  }

  return (
    <div style={{
      padding: "20px",
      backgroundColor: "#000000",
      minHeight: "100vh",
      position: "relative"
    }}>
      {showBusinessDetails && selectedBusiness && (
        <BusinessDetailsView 
          business={selectedBusiness}
          onBack={() => {
            setShowBusinessDetails(false);
            setSelectedBusiness(null);
          }}
        />
      )}

      <h1 style={{ 
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
        textShadow: "0 2px 4px rgba(0,0,0,0.1)"
      }}>
        Local Business Investment Opportunities
      </h1>
      <div style={{ 
        fontSize: "20px", 
        fontWeight: "600",
        textAlign: "center",
        marginBottom: "20px",
        background: "linear-gradient(135deg, #ef4444, #f59e0b)",
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
        backgroundClip: "text",
        display: "inline-block",
        width: "100%"
      }}>
        Available Investment Budget: ${budget.toLocaleString()}
      </div>

      {/* Legend */}
      {!showBusinessDetails && (
        <div style={{
          position: 'absolute',
          top: '100px',
          right: '20px',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: '15px',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
          zIndex: 1000,
          border: '1px solid #333'
        }}>
          <h3 style={{ marginBottom: '10px', fontSize: '14px', color: '#ffffff' }}>Annual Revenue</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', backgroundColor: '#90EE90', borderRadius: '50%' }}></div>
              <span style={{ fontSize: '12px', color: '#ffffff' }}>Under $500K</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', backgroundColor: '#32CD32', borderRadius: '50%' }}></div>
              <span style={{ fontSize: '12px', color: '#ffffff' }}>$500K - $1M</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', backgroundColor: '#228B22', borderRadius: '50%' }}></div>
              <span style={{ fontSize: '12px', color: '#ffffff' }}>$1M - $1.5M</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', backgroundColor: '#006400', borderRadius: '50%' }}></div>
              <span style={{ fontSize: '12px', color: '#ffffff' }}>Over $1.5M</span>
            </div>
          </div>
        </div>
      )}
      
      <div style={{ height: "85vh", width: "100%" }}>
        <style>
          {`
            ${showBusinessDetails ? '.leaflet-control-zoom { display: none !important; }' : ''}
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
          {businesses.map(business => (
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
                <div style={{ 
                  padding: "12px", 
                  maxWidth: "200px",
                  textAlign: "center"
                }}>
                  <h3 style={{ 
                    marginBottom: "8px", 
                    color: "#000000",
                    fontSize: "16px",
                    fontWeight: "600"
                  }}>{business.name}</h3>
                  <p style={{
                    color: "#666666",
                    fontSize: "14px",
                    marginBottom: "12px"
                  }}>{business.address}</p>
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
                      fontSize: "14px"
                    }}
                    onClick={() => {
                      setShowBusinessDetails(true);
                    }}
                    onMouseOver={(e) => {
                      e.target.style.transform = 'scale(1.02)';
                      e.target.style.filter = 'brightness(1.1)';
                    }}
                    onMouseOut={(e) => {
                      e.target.style.transform = 'scale(1)';
                      e.target.style.filter = 'brightness(1)';
                    }}
                  >
                    Invest Now
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