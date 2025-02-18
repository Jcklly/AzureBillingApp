import React, { useEffect, useState } from 'react';

function Dashboard() {
  const [resources, setResources] = useState(null);
  const [error, setError] = useState(null);

  // Use an environment variable for the API base URL.
  // For development, set REACT_APP_API_URL to "http://localhost:8000"
  // For production, set it to the actual backend URL.
  const API_URL = process.env.REACT_APP_API_URL || "";

  useEffect(() => {
    fetch(`${API_URL}/check-resources`)
      .then((response) => {
         if (!response.ok) {
             throw new Error(`HTTP error! Status: ${response.status}`);
         }
         return response.json();
      })
      .then((data) => setResources(data))
      .catch((err) => setError(err.toString()));
  }, [API_URL]);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      {resources ? (
        <pre>{JSON.stringify(resources, null, 2)}</pre>
      ) : (
        <div>Loading resources...</div>
      )}
    </div>
  );
}

export default Dashboard;
