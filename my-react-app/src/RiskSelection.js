import React from 'react';

const RiskSelection = ({ onSelectRisk }) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-6">Select Your Risk Level</h2>
        <p className="text-gray-300 text-xl mb-12">Choose your investment risk tolerance</p>
      </div>
      
      <div className="flex flex-col gap-6 w-full max-w-md px-4">
        <button
          onClick={() => onSelectRisk(1)}
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-6 px-8 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 text-xl"
        >
          Low Risk
        </button>
        
        <button
          onClick={() => onSelectRisk(2)}
          className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-6 px-8 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 text-xl"
        >
          Medium Risk
        </button>
        
        <button
          onClick={() => onSelectRisk(3)}
          className="bg-red-600 hover:bg-red-700 text-white font-bold py-6 px-8 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 text-xl"
        >
          High Risk
        </button>
      </div>
    </div>
  );
};

export default RiskSelection; 