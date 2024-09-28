import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import CryptocurrencyTable from './CryptocurrencyTable';
import '../css/UnifiedDetail.css';
import StockList from './StockList';
import CommodityList from './CommodityList';
import CryptocurrencyList from './CryptocurrencyList';
import '../css/StockList.css';
import '../css/CommodityList.css';
import '../css/CryptocurrencyList.css';

const ARABIC_CRYPTOCURRENCY_NAMES = {
  'btc': 'بيتكوين',
};

const CryptocurrencyDetail = () => {
  const { cryptoId } = useParams();
  const [cryptoData, setCryptoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCryptoData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`https://predix.site/api/cryptocurrencies/${cryptoId}/`);
        setCryptoData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching cryptocurrency data:', error);
        setError('Error fetching cryptocurrency data. Please try again later.');
        setLoading(false);
      }
    };
    fetchCryptoData();
  }, [cryptoId]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!cryptoData) return <div className="error">No data available</div>;

  const getClassNameForKey = (key) => {
    const classMap = {
      title: 'Crypto-title',
      intro: 'Crypto-intro',
      'Price By Day': 'Crypto-price-by-day',
      p1: 'Crypto-forecast-1',
      p2: 'Crypto-forecast-2',
      p3: 'Crypto-forecast-3',
      p4: 'Crypto-forecast-4',
      p5: 'Crypto-forecast-5',
    };
    return classMap[key] || 'Crypto-detail-item';
  };

  const arabicCryptoName = ARABIC_CRYPTOCURRENCY_NAMES[cryptoId] || cryptoId;

  const renderContent = () => {
    return Object.entries(cryptoData).map(([key, value]) => {
      if (key === 'table') {
        return (
          <React.Fragment key={key}>
            <h2 className="Crypto-price-by-day">توقعات أسعار {arabicCryptoName} للأيام المقبلة</h2>
            <CryptocurrencyTable tableData={value} />
          </React.Fragment>
        );
      } else {
        return (
          <div key={key} className={getClassNameForKey(key)}>
            {key === 'title_element' ? (
              <h1>{value.translated}</h1>
            ) : key === 'date' ? (
              <p className="Crypto-date">{value.translated}</p>
            ) : (
              <p>{value.translated}</p>
            )}
          </div>
        );
      }
    });
  };

  return (

    <div className='detail-container'>
      <div className='detail-list'>
        <StockList />
        <CommodityList />
        <CryptocurrencyList />

      </div>
      <div className="cryptocurrency-detail">
        <h2 className="cryptocurrency-title">توقعات أسعار {arabicCryptoName} غدا وهذا الأسبوع وهذا الشهر</h2>
        {renderContent()}
      </div>

    </div>

  );
};

export default CryptocurrencyDetail;