// src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      <h2>Welcome to the Azure Billing App</h2>
      <p>Your one‑stop solution for managing Azure billing and subscriptions seamlessly.</p>
      <Link to="/login" style={{ padding: '12px 25px', background: '#4e54c8', color: '#fff', textDecoration: 'none', borderRadius: '5px' }}>
        Sign In
      </Link>
    </div>
  );
};

export default Home;