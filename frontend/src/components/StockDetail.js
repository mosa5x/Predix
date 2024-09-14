import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import StockTable from './StockTable';
import '../css/UnifiedDetail.css';
import StockList from './StockList';
import CommodityList from './CommodityList';
import CryptocurrencyList from './CryptocurrencyList';
import '../css/StockList.css';
import '../css/CommodityList.css';
import '../css/CryptocurrencyList.css';

const ARABIC_STOCK_NAMES = {
  'amazon': 'أمازون',
  'microsoft': 'مايكروسوفت',
  'facebook': 'فيسبوك',
  'netflix': 'نتفليكس',
  'nokia': 'نوكيا',
  'nvidia': 'إنفيديا',
  'paypal': 'باي بال',
  'pinterest': 'بينتيريست',
  'tesla': 'تسلا',
  'amd': 'إيه إم دي',
  'alibaba': 'علي بابا',
  'boeing': 'بوينغ',
  'disney': 'ديزني',
  'ibm': 'آي بي إم',
  'aramco': 'أرامكو',
  'v-stock': 'فيزا',
  'uber-stock': 'أوبر',
  'spot-stock': 'سبوتيفاي',
  'lcid-stock': 'لوسيد',
  'intc-stock': 'إنتل',
  'dell-stock': 'ديل',
  'adbe-stock': 'أدوبي',
  'abnb-stock': 'إير بي إن بي',
  'apple': 'آبل',

};

const StockDetail = () => {
  const { stockId } = useParams();
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://157.175.165.180:8000/api/stocks/${stockId}/`);
        setStockData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching stock data:', error);
        setError('Error fetching stock data. Please try again later.');
        setLoading(false);
      }
    };
    fetchStockData();
  }, [stockId]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!stockData) return <div className="error">No data available</div>;

  const getClassNameForKey = (key) => {
    const classMap = {
      title_element: 'stock-title',
      date: 'stock-date',
      closed_the_previous: 'stock-previous-close',
      'Stock Price By Day': 'stock-price-by-day',
      p1: 'stock-forecast-week-1',
      p2: 'stock-forecast-week-2',
      p3: 'stock-forecast-week-3',
      p4: 'stock-forecast-week-4',
      p5: 'stock-forecast-week-5',
      p6: 'stock-forecast-long-term',
    };
    return classMap[key] || 'stock-detail-item';
  };

  const arabicStockName = ARABIC_STOCK_NAMES[stockId] || stockId;

  const renderContent = () => {
    return Object.entries(stockData).map(([key, value]) => {
      if (key === 'table') {
        return (
          <React.Fragment key={key}>
            <h2 className="stock-price-by-day">توقعات أسعار سهم {arabicStockName} للأيام المقبلة</h2>
            <StockTable tableData={value} />
          </React.Fragment>
        );
      } else {
        return (
          <div key={key} className={getClassNameForKey(key)}>
            {key === 'title_element' ? (
              <h1>{value.translated}</h1>
            ) : key === 'date' ? (
              <p className="stock-date">{value.translated}</p>
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
        <div className="stock-detail">
          <h2 className="stock-main-title">توقعات أسعار سهم {arabicStockName} غدا وهذا الأسبوع وهذا الشهر</h2>
          {renderContent()}
        </div>

    </div>

  );
};

export default StockDetail;