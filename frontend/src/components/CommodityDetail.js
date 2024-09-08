import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import CommodityTable from './CommodityTable';
import '../css/UnifiedDetail.css';
import StockList from './StockList';
import CommodityList from './CommodityList';
import CryptocurrencyList from './CryptocurrencyList';
import '../css/StockList.css';
import '../css/CommodityList.css';
import '../css/CryptocurrencyList.css';

const ARABIC_COMMODITY_NAMES = {
  'gold': 'الذهب',
  'oil': 'النفط',
  'silver': 'الفضة'
};

const CommodityDetail = () => {
  const { commodityId } = useParams();
  const [commodityData, setCommodityData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCommodityData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:8000/api/commodities/${commodityId}/`);
        setCommodityData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching commodity data:', error);
        setError('Error fetching commodity data. Please try again later.');
        setLoading(false);
      }
    };
    fetchCommodityData();
  }, [commodityId]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!commodityData) return <div className="error">No data available</div>;

  const getClassNameForKey = (key) => {
    const classMap = {
      title: 'commodity-title',
      intro: 'commodity-intro',
      'Price By Day': 'commodity-price-by-day',
      p1: 'commodity-forecast-1',
      p2: 'commodity-forecast-2',
      p3: 'commodity-forecast-3',
      p4: 'commodity-forecast-4',
      p5: 'commodity-forecast-5',
    };
    return classMap[key] || 'commodity-detail-item';
  };

  const arabicCommodityName = ARABIC_COMMODITY_NAMES[commodityId] || commodityId;

  const renderContent = () => {
    return Object.entries(commodityData).map(([key, value]) => {
      if (key === 'table') {
        return (
          <React.Fragment key={key}>
            <h2 className="commodity-price-by-day">توقعات أسعار {arabicCommodityName} للأيام المقبلة</h2>
            <CommodityTable tableData={value} />
          </React.Fragment>
        );
      } else {
        return (
          <div key={key} className={getClassNameForKey(key)}>
            {key === 'title_element' ? (
              <h1>{value.translated}</h1>
            ) : key === 'date' ? (
              <p className="commodity-date">{value.translated}</p>
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
      <div className="commodity-detail">
        <h2 className="commodity-main-title">توقعات أسعار {arabicCommodityName} غدا وهذا الأسبوع وهذا الشهر</h2>
        {renderContent()}
      </div>

    </div>
  );
};

export default CommodityDetail;