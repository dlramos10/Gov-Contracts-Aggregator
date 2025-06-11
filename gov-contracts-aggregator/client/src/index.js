import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [keyword, setKeyword] = useState('');
  const [naics, setNaics] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [results, setResults] = useState([]);

  const search = async () => {
    const params = new URLSearchParams();
    if (keyword) params.append('keyword', keyword);
    if (naics) params.append('naics', naics);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    const res = await fetch(`/api/contracts?${params.toString()}`);
    const data = await res.json();
    const combined = [...(data.federal || []), ...(data.state || [])];
    setResults(combined);
  };

  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>Gov Contracts Aggregator</h1>
      <div style={{ marginBottom: '1rem' }}>
        <input
          placeholder="Keyword"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />{' '}
        <input
          placeholder="NAICS"
          value={naics}
          onChange={(e) => setNaics(e.target.value)}
        />{' '}
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />{' '}
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />{' '}
        <button onClick={search}>Search</button>
      </div>
      <ul>
        {results.map((item, idx) => (
          <li key={idx}>{item.title || item.description || 'Result'}</li>
        ))}
      </ul>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
