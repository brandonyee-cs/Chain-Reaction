import React from 'react';

const LandingPage = ({ onLogin }) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="text-center mb-16">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 text-transparent bg-clip-text">
          Chain Reaction
        </h1>
        <h2 className="text-2xl text-gray-300">
          Micro-Investment Platform for Small Business Supply Chains
        </h2>
      </div>
      
      <button
        onClick={onLogin}
        className="bg-[#1a365d] hover:bg-[#2c5282] text-white font-semibold py-4 px-12 rounded-lg shadow-lg transition-all duration-300 transform hover:scale-105 text-xl hover:shadow-blue-900/30 hover:shadow-2xl"
      >
        Login to Nessie API
      </button>
    </div>
  );
};

export default LandingPage;
