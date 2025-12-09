import React, { useState } from "react";

// 1. Data
const rfps = [
  { name: "Metro 11kV Cable RFP", file: "/rfps/rfp_01.pdf" },
  { name: "Urban LT Substation RFP", file: "/rfps/rfp_02.pdf" },
  { name: "Industrial HV Cable RFP", file: "/rfps/rfp_03.pdf" },
  { name: "Fire Survival Tunnel RFP", file: "/rfps/rfp_04.pdf" },
  { name: "Solar Park DC Cable RFP", file: "/rfps/rfp_05.pdf" },
  { name: "Marine Cable RFP", file: "/rfps/rfp_06.pdf" },
  { name: "Oil & Gas Cable RFP", file: "/rfps/rfp_07.pdf" },
  { name: "Mixed Infrastructure RFP", file: "/rfps/rfp_08.pdf" }
];

// 2. Helper Component for individual cards
const RfpCard = ({ rfp }) => {
  const [isHovered, setIsHovered] = useState(false);

  const styles = {
    card: {
      backgroundColor: "white",
      borderRadius: "12px",
      padding: "24px",
      boxShadow: isHovered 
        ? "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)" 
        : "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
      transform: isHovered ? "translateY(-5px)" : "translateY(0)",
      transition: "all 0.3s ease",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      height: "100%",
      border: "1px solid #f0f0f0",
        margin:"5px 0px 4px 0px"
    },
    iconContainer: {
      marginBottom: "16px",
      color: "#ef4444", // Red for PDF
    },
    title: {
      fontSize: "18px",
      fontWeight: "600",
      color: "#1f2937",
      marginBottom: "20px",
      fontFamily: "'Segoe UI', sans-serif",
    },
    button: {
      marginTop: "auto",
      padding: "10px 0",
      textAlign: "center",
      backgroundColor: isHovered ? "#2563eb" : "#eff6ff",
      color: isHovered ? "white" : "#2563eb",
      borderRadius: "8px",
      fontWeight: "600",
      textDecoration: "none",
      transition: "all 0.3s ease",
      display: "block",
    }
  };

  return (
    <div 
      style={styles.card}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div style={styles.iconContainer}>
        {/* Simple inline SVG for PDF Icon */}
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
      </div>
      <h3 style={styles.title}>{rfp.name}</h3>
      <a 
        href={rfp.file} 
        target="_blank" 
        rel="noopener noreferrer" 
        style={styles.button}
      >
        View Document
      </a>
    </div>
  );
};

// 3. Main Page Component
const RfpPage = () => {
  const styles = {
    container: {
      padding: "40px",
      backgroundColor: "#f9fafb", // Very light grey bg
      minHeight: "100vh",
    },
    header: {
      fontSize: "32px",
      fontWeight: "700",
      color: "#111827",
      marginBottom: "8px",
      textAlign: "center",
      fontFamily: "'Segoe UI', sans-serif",
    },
    subHeader: {
      textAlign: "center",
      color: "#6b7280",
      marginBottom: "40px",
      fontSize: "16px",
    },
    grid: {
      display: "grid",
      // Responsive grid: fit as many 280px cards as possible
      gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
      gap: "24px",
      maxWidth: "1200px",
      margin: "0 auto",
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Tender Documentation</h2>
      <p style={styles.subHeader}>Access the latest Requests for Proposal (RFP) below.</p>

      <div style={styles.grid}>
        {rfps.map((rfp, index) => (
          <RfpCard key={index} rfp={rfp} />
        ))}
      </div>
    </div>
  );
};

export default RfpPage;