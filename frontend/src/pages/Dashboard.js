import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [resources, setResources] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResources = async () => {
      try {
        // Replace '/api/check-resources' with your actual backend endpoint
        const response = await axios.get('/api/check-resources');
        setResources(response.data.resources);
      } catch (err) {
        setError('Failed to load resources.');
      }
    };
    fetchResources();
  }, []);

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Dashboard</h2>
      {error && <p style={{color:'red'}}>{error}</p>}
      <pre>{JSON.stringify(resources, null, 2)}</pre>
    </div>
  );
}

export default Dashboard;
