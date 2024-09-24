import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../css/CommodityList.css';

const CommodityList = () => {
  const [commodities, setCommodities] = useState([]);
  const [arabicNames, setArabicNames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCommodities = async () => {
      try {
        setLoading(true);
        const response = await axios.get('ec2-157-175-209-23.me-south-1.compute.amazonaws.com/api/commoditylist/');
        setCommodities(response.data.commodities);
        setArabicNames(response.data.arabic_names);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching commodities:', error);
        setError('Error fetching commodities. Please try again later.');
        setLoading(false);
      }
    };

    fetchCommodities();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="commodity-list">
      <h2 className='commodity_name_header'>السلع</h2>
      <ul className='commodity_name_list'>
        {commodities.map((commodity, index) => (
          <li key={commodity} className="commodity-item">
            <Link to={`/commodity/${commodity}`}>
              {arabicNames[index] || commodity}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CommodityList;