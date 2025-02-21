import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [resources, setResources] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/check-resources')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (data.status === 'success') {
          setResources(data.resources);
        } else {
          setError(data.message || 'Failed to load resources.');
        }
      })
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={styles.container}>
      <h1>Dashboard</h1>
      {error && <p style={styles.error}>Error: {error}</p>}
      {!error && (
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            {resources.map((resource, index) => (
              <tr key={index}>
                <td>{resource.name || 'N/A'}</td>
                <td>{resource.type || 'N/A'}</td>
                <td>{resource.location || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    maxWidth: '800px',
    margin: '0 auto'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  error: {
    color: 'red'
  }
};

export default Dashboard;