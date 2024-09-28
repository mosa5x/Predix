import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import StockList from './components/StockList';
import StockDetail from './components/StockDetail';
import CommodityList from './components/CommodityList';
import CommodityDetail from './components/CommodityDetail';
import CryptocurrencyList from './components/CryptocurrencyList';
import CryptocurrencyDetail from './components/CryptocurrencyDetail';
import ArabicLandingPage from './components/ArabicLandingPage';

const App = () => {
  const [isHomeVisible, setHomeVisible] = useState(true);

  const toggleHomeVisibility = (isVisible) => {
    setHomeVisible(!isVisible);
  };

  return (
    <Router>
      <div className="App">
        <Header toggleHomeVisibility={toggleHomeVisibility} />
        <main className={`container mx-auto mt-4 ${isHomeVisible ? '' : 'hidden'}`}>
          <Routes>
            <Route path="/" element={<ArabicLandingPage />} />
            <Route path="/stock/:stockId" element={<StockDetail />} />
            <Route path="/commodities" element={<CommodityList />} />
            <Route path="/commodity/:commodityId" element={<CommodityDetail />} />
            <Route path="/cryptocurrencies" element={<CryptocurrencyList />} />
            <Route path="/cryptocurrency/:cryptoId" element={<CryptocurrencyDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;