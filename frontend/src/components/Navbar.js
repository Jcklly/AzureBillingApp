import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ padding: '1rem', background: '#ccc' }}>
      <Link to="/">Login</Link> |{' '}
      <Link to="/register">Register</Link> |{' '}
      <Link to="/dashboard">Dashboard</Link>
    </nav>
  );
}

export default Navbar;
