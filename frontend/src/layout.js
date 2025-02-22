// src/Layout.js
import React from 'react';

const Layout = ({ children }) => {
  return (
    <div>
      <header style={{ padding: '20px', background: 'rgba(0,0,0,0.4)', textAlign: 'center' }}>
        <h1>Azure Billing App</h1>
      </header>
      <main>{children}</main>
      <footer style={{ padding: '10px', background: 'rgba(0,0,0,0.4)', textAlign: 'center', fontSize: '0.9em' }}>
        &copy; 2025 Azure Billing App. All Rights Reserved.
      </footer>
    </div>
  );
};

export default Layout;
