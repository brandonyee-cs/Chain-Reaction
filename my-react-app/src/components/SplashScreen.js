import React from 'react';

const SplashScreen = () => {
  return (
    <div className="splash-screen">
      <style>
        {`
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
            width: 200px;
            height: 200px;
            position: relative;
            animation: fadeIn 0.5s ease-out;
          }

          .cr-logo::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(255, 215, 181, 0.1), transparent 70%);
            animation: pulse 2s ease-in-out infinite;
          }

          .cr-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
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

          @keyframes pulse {
            0%, 100% {
              transform: scale(1);
              opacity: 0.5;
            }
            50% {
              transform: scale(1.2);
              opacity: 0.8;
            }
          }
        `}
      </style>
      <div className="logo-container">
        <div className="cr-logo">
          <img src="/cr.png" alt="Chain Reaction Logo" />
        </div>
        <div className="loading-bar">
          <div className="loading-progress"></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen; 