import React from 'react';

const StockTable = ({ tableData }) => {
  console.log('Received tableData:', tableData);

  if (!tableData || !tableData.translated || !Array.isArray(tableData.translated) || tableData.translated.length === 0) {
    console.log('No table data available');
    return <p>No table data available</p>;
  }

  const headers = Array.isArray(tableData.translated[0]) ? tableData.translated[0] : [];
  const rows = tableData.translated.slice(1);

  console.log('Headers:', headers);
  console.log('Rows:', rows);

  return (
    <table className="stock-table">
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
            {Array.isArray(row) ? row.map((cell, cellIndex) => (
              <td key={cellIndex}>{cell}</td>
            )) : null}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default StockTable;