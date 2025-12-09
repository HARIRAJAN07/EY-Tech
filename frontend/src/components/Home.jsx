import React, { useState } from 'react';

const Home = () => {
  const [isHovered, setIsHovered] = useState(false);

  const styles = {
    container: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      backgroundColor: '#0f172a', // Dark slate background
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    },
    button: {
      background: isHovered 
        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' // Purple-ish on hover
        : 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)', // Blue-Purple default
      color: 'white',
      border: 'none',
      padding: '16px 32px',
      fontSize: '18px',
      fontWeight: '600',
      borderRadius: '50px', // Pill shape
      cursor: 'pointer',
      boxShadow: isHovered 
        ? '0 10px 25px -5px rgba(168, 85, 247, 0.6)' 
        : '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
      transition: 'all 0.3s ease',
      letterSpacing: '0.5px',
      outline: 'none',
    }
  };

  return (
    <div style={styles.container}>
      <button 
        style={styles.button}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        Check RFP
      </button>
    </div>
  );
};

export default Home;