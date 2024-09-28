import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../css/CryptocurrencyList.css';
import CryptocurrencyTable from './CryptocurrencyTable';

const CryptocurrencyList = () => {
  const [cryptocurrencies, setCryptocurrencies] = useState([]);
  const [arabicNames, setArabicNames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCrypto, setSelectedCrypto] = useState(null);
  const [cryptoData, setCryptoData] = useState(null);

  useEffect(() => {
    const fetchCryptocurrencies = async () => {
      try {
        setLoading(true);
        const response = await axios.get('https://predix.site/api/cryptocurrencylist/');
        console.log('API Response:', response.data); // Debugging line
        setCryptocurrencies(response.data.cryptocurrencies);
        setArabicNames(response.data.arabic_names);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching cryptocurrencies:', error);
        setError('Error fetching cryptocurrencies. Please try again later.');
        setLoading(false);
      }
    };

    fetchCryptocurrencies();
  }, []);

  const fetchCryptoData = async (crypto) => {
    try {
      const response = await axios.get(`ec2-157-175-209-23.me-south-1.compute.amazonaws.com/api/cryptocurrencies/${crypto}/`);
      setCryptoData(response.data);
      setSelectedCrypto(crypto);
    } catch (error) {
      console.error('Error fetching cryptocurrency data:', error);
      setError('Error fetching cryptocurrency data. Please try again later.');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="cryptocurrency-list">
      <h2 className='cryptocurrency_name_header'>العملات الرقمية</h2>
      <ul className='cryptocurrency_name_list'>
        {cryptocurrencies.map((crypto, index) => (
          <li key={crypto} className="cryptocurrency-item">
            <Link to={`/cryptocurrency/${crypto}`}>
              {arabicNames[index] || crypto}
            </Link>
          </li>
        ))}
      </ul>
      {selectedCrypto && cryptoData && (
        <div className="cryptocurrency-details">
          <h3>{arabicNames[cryptocurrencies.indexOf(selectedCrypto)] || selectedCrypto}</h3>
          <p>{cryptoData.date.translated}</p>
          <p>{cryptoData.intro.translated}</p>
          <CryptocurrencyTable tableData={cryptoData.table} />
          <p>{cryptoData.p1.translated}</p>
          <p>{cryptoData.p2.translated}</p>
          <p>{cryptoData.p3.translated}</p>
          <p>{cryptoData.p4.translated}</p>
          <p>{cryptoData.p5.translated}</p>
        </div>
      )}
    </div>
  );
};

export default CryptocurrencyList;
