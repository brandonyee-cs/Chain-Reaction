import React, { useEffect, useState } from 'react';
import SplashScreen from './components/SplashScreen';

const RiskSelection = ({ onSelectRisk }) => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [particles, setParticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [budget, setBudget] = useState(1000);

  const getBudgetColor = (amount) => {
    if (amount < 3000) return '#fbbf24'; // Warm yellow
    if (amount < 7000) return '#15803d'; // Medium green
    return '#064e3b'; // Dark green
  };

  const formatBudget = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    // Initialize particles
    const initParticles = () => {
      const newParticles = [];
      for (let i = 0; i < 20; i++) {
        newParticles.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          size: Math.random() * 3 + 2
        });
      }
      setParticles(newParticles);
    };

    // Animation loop
    let animationFrameId;
    const animate = () => {
      setParticles(prevParticles => {
        return prevParticles.map(particle => {
          let x = particle.x + particle.vx;
          let y = particle.y + particle.vy;

          // Bounce off walls
          if (x < 0 || x > window.innerWidth) particle.vx *= -1;
          if (y < 0 || y > window.innerHeight) particle.vy *= -1;

          return {
            ...particle,
            x: x < 0 ? 0 : x > window.innerWidth ? window.innerWidth : x,
            y: y < 0 ? 0 : y > window.innerHeight ? window.innerHeight : y
          };
        });
      });
      animationFrameId = requestAnimationFrame(animate);
    };

    initParticles();
    animate();

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  const handleMouseMove = (e) => {
    setMousePosition({
      x: e.clientX,
      y: e.clientY
    });
  };

  if (loading) {
    return <SplashScreen />;
  }

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

          .chain-reaction-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
          }

          .particle {
            position: absolute;
            background: radial-gradient(circle at center, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
            border-radius: 50%;
            pointer-events: none;
          }

          .connection {
            position: absolute;
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
            transform-origin: left center;
            pointer-events: none;
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

          .risk-button {
            transition: all 0.3s ease;
            width: 100%;
            padding: 32px;
            border: none;
            border-radius: 12px;
            font-size: 28px;
            font-weight: 600;
            color: white;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
          }

          .risk-button span {
            font-size: 18px;
            opacity: 0.9;
          }

          .risk-button:hover {
            transform: translateY(-2px);
          }

          .risk-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
              90deg,
              transparent,
              rgba(255, 255, 255, 0.2),
              transparent
            );
            transition: 0.5s;
          }

          .risk-button:hover::before {
            left: 100%;
          }

          .splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, #1a1a1a, #0A0A0A 60%, #080808);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
          }

          .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 32px;
            animation: fadeIn 0.5s ease-out;
          }

          .cr-logo {
            font-size: 120px;
            font-weight: 800;
            letter-spacing: -4px;
            position: relative;
          }

          .cr-logo .c {
            color: #ffd7b5;
            margin-right: -10px;
          }

          .cr-logo .r {
            color: #d4d4d4;
          }

          .loading-bar {
            width: 200px;
            height: 3px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
          }

          .loading-progress {
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #ffd7b5, #d4d4d4);
            animation: loading 2s ease-in-out;
            transform-origin: left;
          }

          @keyframes loading {
            0% {
              transform: scaleX(0);
            }
            100% {
              transform: scaleX(1);
            }
          }

          @keyframes fadeIn {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          .budget-slider {
            width: 100%;
            max-width: 500px;
            margin: 40px 0;
            text-align: center;
          }

          .budget-slider input[type="range"] {
            width: 100%;
            height: 8px;
            border-radius: 4px;
            -webkit-appearance: none;
            appearance: none;
            background: rgba(255, 255, 255, 0.1);
            outline: none;
            cursor: pointer;
          }

          .budget-slider input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #fff;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
          }

          .budget-slider input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.1);
          }

          .budget-display {
            font-size: 72px;
            font-weight: 800;
            margin: 20px 0;
            transition: color 0.3s ease;
            text-align: center;
          }

          .budget-label {
            font-size: 18px;
            color: #666;
            margin-bottom: 10px;
          }
        `}
      </style>

      {/* Chain Reaction Background */}
      <div className="chain-reaction-bg">
        {particles.map((particle, i) => (
          <React.Fragment key={i}>
            <div
              className="particle"
              style={{
                left: particle.x,
                top: particle.y,
                width: particle.size,
                height: particle.size
              }}
            />
            {particles.slice(i + 1).map((other, j) => {
              const distance = Math.hypot(other.x - particle.x, other.y - particle.y);
              if (distance < 150) {
                const angle = Math.atan2(other.y - particle.y, other.x - particle.x);
                return (
                  <div
                    key={`${i}-${j}`}
                    className="connection"
                    style={{
                      left: particle.x,
                      top: particle.y,
                      width: distance,
                      height: '1px',
                      transform: `rotate(${angle}rad)`
                    }}
                  />
                );
              }
              return null;
            })}
          </React.Fragment>
        ))}
      </div>

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

      <div style={{
        textAlign: 'center',
        marginBottom: '60px',
        position: 'relative',
        zIndex: 2,
        maxWidth: '1200px'
      }}>
        <h1 style={{
          fontSize: '72px',
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
          Risk Selection
        </h1>
        <h2 style={{
          fontSize: '32px',
          color: '#666666',
          fontWeight: '400',
          margin: '0 auto',
          letterSpacing: '-1px',
          lineHeight: '1.4'
        }}>
          Select your budget for investing
        </h2>
      </div>

      <div className="budget-slider" style={{ position: 'relative', zIndex: 2 }}>
        <div className="budget-display" style={{ color: getBudgetColor(budget) }}>
          {formatBudget(budget)}
        </div>
        <div className="budget-label">Drag the slider to set your investment budget</div>
        <input
          type="range"
          min="1000"
          max="10000"
          value={budget}
          onChange={(e) => {
            const newBudget = parseInt(e.target.value);
            console.log('Budget updated:', newBudget);
            setBudget(newBudget);
          }}
          style={{
            background: `linear-gradient(90deg, ${getBudgetColor(budget)} ${((budget-1000)/9000)*100}%, rgba(255, 255, 255, 0.1) ${((budget-1000)/9000)*100}%)`
          }}
        />
      </div>

      <button
        onClick={(e) => {
          e.preventDefault();
          console.log('Selected investment amount:', formatBudget(budget));
          if (typeof onSelectRisk === 'function') {
            onSelectRisk(budget);
          } else {
            console.error('onSelectRisk is not a function');
          }
        }}
        className="risk-button"
        style={{
          background: `linear-gradient(90deg, ${getBudgetColor(budget)}, ${getBudgetColor(Math.min(budget + 1000, 10000))})`,
          boxShadow: `0 4px 6px ${getBudgetColor(budget)}33`,
          marginTop: '40px',
          width: 'auto',
          padding: '20px 40px',
          position: 'relative',
          zIndex: 10,
          cursor: 'pointer'
        }}
      >
        Continue with {formatBudget(budget)}
      </button>
    </div>
  );
};

export default RiskSelection; 