import React, { useState } from 'react';

const LandingPage = ({ onLogin }) => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    setMousePosition({
      x: e.clientX,
      y: e.clientY
    });
  };

  return (
    <div 
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'radial-gradient(circle at top right, #1a1a1a, #0A0A0A 60%, #080808)',
        color: 'white',
        padding: '20px',
        position: 'relative',
        overflow: 'hidden'
      }}
      onMouseMove={handleMouseMove}
    >
      <style>
        {`
          @keyframes gradientSweep {
            0%, 100% {
              background-position: -200% 50%;
            }
            45%, 55% {
              background-position: 0% 50%;
            }
          }

          @keyframes float {
            0%, 100% { transform: translate(0, 0); }
            25% { transform: translate(-10px, 10px); }
            50% { transform: translate(10px, -10px); }
            75% { transform: translate(10px, 10px); }
          }

          .grid-pattern {
            background-image: 
              linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            width: 100%;
            height: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1;
          }
        `}
      </style>

      {/* Grid Pattern */}
      <div className="grid-pattern" />

      {/* Background Orbs */}
      <div style={{
        position: 'fixed',
        top: '10%',
        right: '15%',
        width: '400px',
        height: '400px',
        background: 'radial-gradient(circle at center, rgba(255, 77, 77, 0.03), transparent 70%)',
        borderRadius: '50%',
        animation: 'float 15s ease-in-out infinite',
        zIndex: 1
      }} />
      
      <div style={{
        position: 'fixed',
        bottom: '20%',
        left: '10%',
        width: '300px',
        height: '300px',
        background: 'radial-gradient(circle at center, rgba(249, 203, 40, 0.02), transparent 70%)',
        borderRadius: '50%',
        animation: 'float 12s ease-in-out infinite reverse',
        zIndex: 1
      }} />

      {/* Gradient light following cursor */}
      <div
        style={{
          position: 'fixed',
          background: 'radial-gradient(800px circle at center, rgba(255, 165, 0, 0.15), rgba(255, 77, 77, 0.1), transparent 50%)',
          left: mousePosition.x - 400,
          top: mousePosition.y - 400,
          width: '800px',
          height: '800px',
          pointerEvents: 'none',
          transition: 'all 0.15s linear',
          zIndex: 1,
          mixBlendMode: 'screen'
        }}
      />

      <div style={{
        textAlign: 'center',
        marginBottom: '60px',
        position: 'relative',
        zIndex: 2,
        maxWidth: '1200px'
      }}>
        <h1 style={{
          fontSize: '96px',
          fontWeight: '800',
          marginBottom: '32px',
          background: 'linear-gradient(90deg, #ff4d4d 20%, #f9cb28 50%, #ff4d4d 80%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          letterSpacing: '-2px',
          backgroundSize: '200% 100%',
          animation: 'gradientSweep 8s ease-in-out infinite'
        }}>
          Chain Reaction
        </h1>
        <h2 style={{
          fontSize: '32px',
          color: '#666666',
          fontWeight: '400',
          margin: '0 auto',
          letterSpacing: '-1px',
          lineHeight: '1.4'
        }}>
          Invest in supply chains. Support local businesses.
        </h2>
      </div>
      
      <button
        onClick={onLogin}
        style={{
          background: '#0076BE',
          color: 'white',
          border: 'none',
          padding: '16px 48px',
          borderRadius: '8px',
          fontSize: '24px',
          fontWeight: '600',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          position: 'relative',
          zIndex: 2,
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 6px 12px rgba(0, 118, 190, 0.3)';
          e.currentTarget.style.background = '#005D99';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
          e.currentTarget.style.background = '#0076BE';
        }}
      >
        Login to Nessie API
      </button>
    </div>
  );
};

export default LandingPage;
