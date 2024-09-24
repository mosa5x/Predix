import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../css/StockList.css';

const StockList = () => {
  const [stocks, setStocks] = useState([]);
  const [arabicNames, setArabicNames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://157.175.209.23/api/stocklist/');
        setStocks(response.data.stocks);
        setArabicNames(response.data.arabic_names);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching stocks:', error);
        setError('Error fetching stocks. Please try again later.');
        setLoading(false);
      }
    };

    fetchStocks();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="stock-list">
      <h2 className='stock_name_header'>جميع الأسهم</h2>
      <ul className='stock_name_list'>
        {stocks.map((stock, index) => (
          <li key={stock} className="stock-item">
            <Link to={`/stock/${stock}`}>
              {arabicNames[index] || stock}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StockList;