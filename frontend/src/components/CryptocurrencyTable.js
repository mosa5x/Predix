import React from 'react';

const CryptocurrencyTable = ({ tableData }) => {
  if (!tableData || !tableData.translated || !Array.isArray(tableData.translated) || tableData.translated.length === 0) {
    return <p>No table data available</p>;
  }

  const headers = tableData.translated[0];
  const rows = tableData.translated.slice(1);

  return (
    <table className="cryptocurrency-table">
      <thead>
        <tr>
          {headers.map((header, index) => (
            <th key={index}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {row.map((cell, cellIndex) => (
              <td key={cellIndex}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CryptocurrencyTable;
