import React, { useState, useEffect } from "react";
import { checkRfps, analyzeTechnically, calculatePricing } from "../service/rfpApi";



/* ---------------------------------------------
   AI LOADING MESSAGES
--------------------------------------------- */
const loadingSteps = [
  "Scanning government portals…",
  "Extracting tender documents…",
  "Analyzing project value…",
  "Evaluating deadlines…",
  "Ranking opportunities…",
];

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [data, setData] = useState(null);
  const [showOthers, setShowOthers] = useState(false);
  const [particles, setParticles] = useState([]);
  const [pricingData, setPricingData] = useState(null);
const [pricingLoading, setPricingLoading] = useState(false);


  /* Generate 3D sphere particles */
  useEffect(() => {
    const generateParticles = () => {
      const pts = [];
      const count = 80;
      for (let i = 0; i < count; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        pts.push({
          id: i,
          theta,
          phi,
          delay: Math.random() * 2,
        });
      }
      setParticles(pts);
    };
    generateParticles();
  }, []);

  /* Animate loading text */
  useEffect(() => {
    if (!loading) return;
    const timer = setInterval(
      () => setStep((s) => (s + 1) % loadingSteps.length),
      1200
    );
    return () => clearInterval(timer);
  }, [loading]);

  const handleCheck = async () => {
    setLoading(true);
    setData(null);
    try {
      const res = await checkRfps();
      setData(res);
    } catch {
      alert("Backend not reachable");
    } finally {
      setLoading(false);
    }
  };

  /* Resolve correct PDF path */
  const resolvePdfUrl = (file) => {
    if (file.toLowerCase().startsWith("rfp_")) {
      return `http://127.0.0.1:8000/files/website_rfp/${file}`;
    }
    return `http://127.0.0.1:8000/files/email_rfp/${file}`;
  };

  const handleTechAnalyze = async (fileName) => {
  try {
    setPricingData(null);
    setPricingLoading(true);

    console.log("⚙️ Running Tech Agent for:", fileName);

    // 1️⃣ Run Tech Agent
    const techRes = await analyzeTechnically(fileName);
    console.log("✅ Tech Agent Result:", techRes);

    // 2️⃣ Run Pricing Agent using FINAL TECH OUTPUT
    console.log("💰 Running Pricing Agent...");
    const pricingRes = await calculatePricing(
      techRes.final_recommendation
    );

    console.log("✅ Pricing Result:", pricingRes);

    setPricingData(pricingRes.pricing_summary);

  } catch (err) {
    console.error("❌ Agent chain failed:", err);
    alert("Tech / Pricing analysis failed");
  } finally {
    setPricingLoading(false);
  }
};



  return (
    <div style={styles.page}>
      {/* ---------------- LOADING SCREEN WITH 3D SPHERE ---------------- */}
      {loading && (
        <div style={styles.loading}>
          <div style={styles.sphereContainer}>
            {particles.map((p) => {
              const radius = 150;
              const x = radius * Math.sin(p.phi) * Math.cos(p.theta);
              const y = radius * Math.sin(p.phi) * Math.sin(p.theta);
              const z = radius * Math.cos(p.phi);
              
              return (
                <div
                  key={p.id}
                  style={{
                    ...styles.particle,
                    left: `calc(50% + ${x}px)`,
                    top: `calc(50% + ${y}px)`,
                    transform: `translateZ(${z}px) scale(${1 + z / 300})`,
                    opacity: 0.3 + (z + radius) / (2 * radius) * 0.7,
                    animationDelay: `${p.delay}s`,
                  }}
                />
              );
            })}
            <div style={styles.sphereGlow}></div>
          </div>
          <h2 style={styles.loadingText}>{loadingSteps[step]}</h2>
          <p style={styles.loadingSub}>RFP Intelligence Engine</p>
          <div style={styles.progressBar}>
            <div style={{
              ...styles.progressFill,
              width: `${((step + 1) / loadingSteps.length) * 100}%`
            }}></div>
          </div>
        </div>
      )}

      {/* ---------------- HERO ---------------- */}
      {!data && !loading && (
        <div style={styles.hero}>
          <div style={styles.heroGlow}></div>
          <div style={styles.heroContent}>
            <div style={styles.badge}>AI-POWERED INTELLIGENCE</div>
            <h1 style={styles.title}>
              RFP Intelligence<br/>Engine
            </h1>
            <p style={styles.subtitle}>
              Discover and rank business-critical opportunities with<br/>
              cutting-edge AI analysis
            </p>
            <button style={styles.cta} onClick={handleCheck}>
              <span style={styles.ctaText}>Analyze RFPs Now</span>
              <span style={styles.ctaIcon}>→</span>
            </button>
            <div style={styles.features}>
              <div style={styles.feature}>⚡ Instant Analysis</div>
              <div style={styles.feature}>🎯 Smart Ranking</div>
              <div style={styles.feature}>📊 Real-time Data</div>
            </div>
          </div>
        </div>
      )}

      {/* ---------------- RESULTS ---------------- */}
      {data && !loading && (
        <div style={styles.results}>
          <div style={styles.resultsHeader}>
            <h2 style={styles.sectionTitle}>
              <span style={styles.trophy}>🏆</span>
              Top Priority Opportunities
            </h2>
            <button style={styles.refreshBtn} onClick={handleCheck}>
              ↻ Refresh
            </button>
          </div>

          {/* TOP 3 PODIUM */}
          <div style={styles.podium}>
            {/* 2nd Place */}
            {data.top_3[1] && (
              <div style={{...styles.podiumCard, ...styles.secondPlace}}>
                <div style={styles.podiumRank}>
                  <div style={styles.silverMedal}>🥈</div>
                  <div style={styles.rankNumber}>#2</div>
                </div>
                <div style={styles.cardContent}>
                  <h3 style={styles.cardOrg}>{data.top_3[1].organization}</h3>
                  <div style={styles.cardScore}>
                    <span style={styles.scoreLabel}>Score</span>
                    <span style={styles.scoreValue}>{data.top_3[1].total_score}</span>
                  </div>
                  <div style={styles.cardMeta}>
                    <div style={styles.metaItem}>
                      <span style={styles.metaIcon}>📋</span>
                      <span>{data.top_3[1].status}</span>
                    </div>
                    <div style={styles.metaItem}>
                      <span style={styles.metaIcon}>🛠️</span>
                      <span>{data.top_3[1].equipment.slice(0, 2).join(", ")}</span>
                    </div>
                  </div>
                  <div style={styles.deadline}>
                    <span style={styles.deadlineIcon}>⏰</span>
                    {data.top_3[1].submission_deadline}
                  </div>
                  <a
                    href={resolvePdfUrl(data.top_3[1].file_name)}
                    target="_blank"
                    rel="noreferrer"
                    style={styles.viewDoc}
                  >
                    View Document →
                  </a>
                  

                </div>
              </div>
            )}

            {/* 1st Place */}
            {data.top_3[0] && (
              <div style={{...styles.podiumCard, ...styles.firstPlace}}>
                <div style={styles.crownContainer}>
                  <div style={styles.crown}>👑</div>
                </div>
                <div style={styles.podiumRank}>
                  <div style={styles.goldMedal}>🥇</div>
                  <div style={styles.rankNumber}>#1</div>
                </div>
                <div style={styles.cardContent}>
                  <h3 style={styles.cardOrg}>{data.top_3[0].organization}</h3>
                  <div style={styles.cardScore}>
                    <span style={styles.scoreLabel}>Score</span>
                    <span style={{...styles.scoreValue, fontSize: "48px"}}>{data.top_3[0].total_score}</span>
                  </div>
                  <div style={styles.cardMeta}>
                    <div style={styles.metaItem}>
                      <span style={styles.metaIcon}>📋</span>
                      <span>{data.top_3[0].status}</span>
                    </div>
                    <div style={styles.metaItem}>
                      <span style={styles.metaIcon}>🛠️</span>
                      <span>{data.top_3[0].equipment.slice(0, 2).join(", ")}</span>
                    </div>
                  </div>
                  <div style={styles.deadline}>
                    <span style={styles.deadlineIcon}>⏰</span>
                    {data.top_3[0].submission_deadline}
                  </div>
                  <a
                    href={resolvePdfUrl(data.top_3[0].file_name)}
                    target="_blank"
                    rel="noreferrer"
                    style={{...styles.viewDoc, ...styles.viewDocFirst}}
                  >
                    View Document →
                  </a>
                </div>
              </div>
            )}

            {/* 3rd Place */}
            {data.top_3[2] && (
              <div style={{...styles.podiumCard, ...styles.thirdPlace}}>
                <div style={styles.podiumRank}>
                  <div style={styles.bronzeMedal}>🥉</div>
                  <div style={styles.rankNumber}>#3</div>
                </div>
                <div style={styles.cardContent}>
                  <h3 style={styles.cardOrg}>{data.top_3[2].organization}</h3>
                  <div style={styles.cardScore}>
                    <span style={styles.scoreLabel}>Score</span>
                    <span style={styles.scoreValue}>{data.top_3[2].total_score}</span>
                  </div>
                  <div style={styles.cardMeta}>
                    <div style={styles.metaItem}>
                      <span style={styles.metaIcon}>📋</span>
                      <span>{data.top_3[2].status}</span>
                    </div>
                    <div style={styles.metaItem}>
                      <span style={styles.metaIcon}>🛠️</span>
                      <span>{data.top_3[2].equipment.slice(0, 2).join(", ")}</span>
                    </div>
                  </div>
                  <div style={styles.deadline}>
                    <span style={styles.deadlineIcon}>⏰</span>
                    {data.top_3[2].submission_deadline}
                  </div>
                  <a
                    href={resolvePdfUrl(data.top_3[2].file_name)}
                    target="_blank"
                    rel="noreferrer"
                    style={styles.viewDoc}
                  >
                    View Document →
                  </a>
                </div>
              </div>
            )}
          </div>

          {/* FULL LEADERBOARD TOGGLE */}
          <div style={styles.toggleContainer}>
            <button
              style={styles.toggleBtn}
              onClick={() => setShowOthers(!showOthers)}
            >
              {showOthers ? "Hide Full Leaderboard" : "View Full Leaderboard"}
              <span style={styles.toggleIcon}>{showOthers ? "▲" : "▼"}</span>
            </button>
          </div>

          {/* LEADERBOARD */}
          {showOthers && (
            <div style={styles.leaderboard}>
              <h3 style={styles.leaderTitle}>
                <span style={styles.leaderIcon}>📊</span>
                Complete Rankings
              </h3>
              <div style={styles.leaderboardGrid}>
                {data.others.map((r, idx) => (
                  <div key={idx} style={styles.leaderRow} className="leaderRow">
                    <div style={styles.leaderRank}>
                      <span style={styles.rankBadge}>#{idx + 4}</span>
                    </div>
                    <div style={styles.leaderInfo}>
                      <div style={styles.leaderOrg}>{r.organization}</div>
                      <div style={styles.leaderMeta}>
                        {r.status} • {r.equipment[0]}
                      </div>
                    </div>
                    <div style={styles.leaderScore}>
                      <div style={styles.scoreNum}>{r.total_score}</div>
                      <div style={styles.scoreText}>points</div>
                    </div>
                    <div style={styles.leaderAction}>
                      <a
                        href={resolvePdfUrl(r.file_name)}
                        target="_blank"
                        rel="noreferrer"
                        style={styles.leaderLink}
                      >
                        View Doc →
                      </a>
                      <button
                        style={styles.techBtn}
                        onClick={() => handleTechAnalyze(data.top_3[0].file_name)}
                      >
                        Analyze Technically ⚙️
                      </button>

                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {pricingLoading && (
  <div style={{ textAlign: "center", marginTop: "40px" }}>
    <h3>💰 Calculating Optimal Price...</h3>
  </div>
)}

{pricingData && (
  <div style={{
    marginTop: "60px",
    padding: "30px",
    borderRadius: "20px",
    background: "rgba(0,245,255,0.08)",
    border: "1px solid rgba(0,245,255,0.3)"
  }}>
    <h2 style={{ marginBottom: "20px" }}>
      💰 Pricing Recommendation
    </h2>

    <p><b>SKU:</b> {pricingData.sku}</p>
    <p><b>Quantity:</b> {pricingData.quantity} {pricingData.uom}</p>
    <p><b>Material Cost:</b> ₹{pricingData.material_cost.toLocaleString()}</p>
    <p><b>Testing Cost:</b> ₹{pricingData.testing_cost.toLocaleString()}</p>
    <p><b>Packing Cost:</b> ₹{pricingData.packing_cost.toLocaleString()}</p>
    <p><b>Transport Cost:</b> ₹{pricingData.transport_cost.toLocaleString()}</p>

    <hr style={{ margin: "20px 0", opacity: 0.3 }} />

    <h3>
      ✅ Total Cost: ₹{pricingData.total_cost.toLocaleString()}
    </h3>
  </div>
)}

        </div>
      )}
    </div>
  );
};

/* ---------------------------------------------
   STYLES
--------------------------------------------- */

const styles = {
  page: {
    minHeight: "100vh",
    width: "100%",
    background: "linear-gradient(135deg, #0a0118 0%, #1a0b2e 50%, #16001e 100%)",
    color: "#ffffff",
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    overflow: "auto",
  },

  /* ============ LOADING (3D SPHERE) ============ */
  loading: {
    position: "fixed",
    inset: 0,
    background: "radial-gradient(circle at center, #1a0b2e 0%, #000000 100%)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 9999,
    perspective: "1000px",
  },
  sphereContainer: {
    position: "relative",
    width: "400px",
    height: "400px",
    transformStyle: "preserve-3d",
    animation: "rotate3d 20s linear infinite",
  },
  particle: {
    position: "absolute",
    width: "12px",
    height: "12px",
    background: "radial-gradient(circle, #00f5ff 0%, #7b2cbf 100%)",
    borderRadius: "50%",
    boxShadow: "0 0 20px #00f5ff, 0 0 40px #7b2cbf",
    animation: "pulse 2s ease-in-out infinite",
  },
  sphereGlow: {
    position: "absolute",
    top: "50%",
    left: "50%",
    width: "200px",
    height: "200px",
    transform: "translate(-50%, -50%)",
    background: "radial-gradient(circle, rgba(0,245,255,0.3) 0%, transparent 70%)",
    borderRadius: "50%",
    animation: "glow 3s ease-in-out infinite",
  },
  loadingText: {
    marginTop: "80px",
    fontSize: "28px",
    fontWeight: 700,
    background: "linear-gradient(90deg, #00f5ff, #7b2cbf, #ff006e)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundSize: "200% auto",
    animation: "shimmer 3s linear infinite",
  },
  loadingSub: {
    marginTop: "12px",
    fontSize: "16px",
    opacity: 0.6,
    letterSpacing: "2px",
  },
  progressBar: {
    marginTop: "40px",
    width: "300px",
    height: "4px",
    background: "rgba(255,255,255,0.1)",
    borderRadius: "10px",
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    background: "linear-gradient(90deg, #00f5ff, #7b2cbf)",
    transition: "width 1.2s ease",
    boxShadow: "0 0 20px #00f5ff",
  },

  /* ============ HERO ============ */
  hero: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
    position: "relative",
    overflow: "hidden",
  },
  heroGlow: {
    position: "absolute",
    top: "-50%",
    left: "50%",
    width: "800px",
    height: "800px",
    transform: "translateX(-50%)",
    background: "radial-gradient(circle, rgba(123,44,191,0.3) 0%, transparent 70%)",
    animation: "float 8s ease-in-out infinite",
  },
  heroContent: {
    position: "relative",
    zIndex: 1,
  },
  badge: {
    display: "inline-block",
    padding: "8px 20px",
    background: "rgba(0,245,255,0.1)",
    border: "1px solid rgba(0,245,255,0.3)",
    borderRadius: "999px",
    fontSize: "12px",
    fontWeight: 600,
    letterSpacing: "2px",
    color: "#00f5ff",
    marginBottom: "30px",
  },
  title: {
    fontSize: "72px",
    fontWeight: 900,
    lineHeight: 1.1,
    background: "linear-gradient(135deg, #00f5ff 0%, #7b2cbf 50%, #ff006e 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    marginBottom: "20px",
    letterSpacing: "-2px",
  },
  subtitle: {
    fontSize: "18px",
    color: "rgba(255,255,255,0.7)",
    lineHeight: 1.6,
    maxWidth: "600px",
    marginBottom: "50px",
  },
  cta: {
    position: "relative",
    padding: "20px 50px",
    fontSize: "18px",
    fontWeight: 700,
    border: "none",
    borderRadius: "999px",
    background: "linear-gradient(135deg, #00f5ff, #7b2cbf)",
    color: "white",
    cursor: "pointer",
    boxShadow: "0 20px 60px rgba(0,245,255,0.4), 0 0 40px rgba(123,44,191,0.3)",
    transition: "all 0.3s ease",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    overflow: "hidden",
  },
  ctaText: {
    position: "relative",
    zIndex: 1,
  },
  ctaIcon: {
    fontSize: "24px",
    transition: "transform 0.3s ease",
  },
  features: {
    display: "flex",
    gap: "30px",
    marginTop: "60px",
    justifyContent: "center",
  },
  feature: {
    fontSize: "14px",
    opacity: 0.7,
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },

  /* ============ RESULTS ============ */
  results: {
    minHeight: "100vh",
    padding: "80px 60px",
    width: "100%",
    boxSizing: "border-box",
  },
  resultsHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "60px",
  },
  sectionTitle: {
    fontSize: "42px",
    fontWeight: 800,
    display: "flex",
    alignItems: "center",
    gap: "15px",
  },
  trophy: {
    fontSize: "48px",
  },
  refreshBtn: {
    padding: "12px 28px",
    background: "rgba(255,255,255,0.05)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "12px",
    color: "white",
    fontSize: "14px",
    fontWeight: 600,
    cursor: "pointer",
    transition: "all 0.3s ease",
  },

  /* ============ PODIUM (Top 3) ============ */
  podium: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr 1fr",
    gap: "30px",
    alignItems: "end",
    marginBottom: "80px",
    maxWidth: "1400px",
    margin: "0 auto 80px",
  },
  podiumCard: {
    position: "relative",
    background: "linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)",
    backdropFilter: "blur(20px)",
    borderRadius: "24px",
    padding: "40px 30px",
    border: "1px solid rgba(255,255,255,0.1)",
    transition: "all 0.4s ease",
  },
  firstPlace: {
    transform: "scale(1.08) translateY(-20px)",
    background: "linear-gradient(135deg, rgba(0,245,255,0.15) 0%, rgba(123,44,191,0.15) 100%)",
    border: "2px solid rgba(0,245,255,0.3)",
    boxShadow: "0 40px 100px rgba(0,245,255,0.3), 0 0 80px rgba(123,44,191,0.2)",
  },
  secondPlace: {
    background: "linear-gradient(135deg, rgba(192,192,192,0.1) 0%, rgba(255,255,255,0.05) 100%)",
    border: "1px solid rgba(192,192,192,0.3)",
    boxShadow: "0 20px 60px rgba(192,192,192,0.2)",
  },
  thirdPlace: {
    background: "linear-gradient(135deg, rgba(205,127,50,0.1) 0%, rgba(255,255,255,0.05) 100%)",
    border: "1px solid rgba(205,127,50,0.3)",
    boxShadow: "0 20px 60px rgba(205,127,50,0.2)",
  },
  crownContainer: {
    position: "absolute",
    top: "-30px",
    left: "50%",
    transform: "translateX(-50%)",
  },
  crown: {
    fontSize: "48px",
    animation: "bounce 2s ease-in-out infinite",
  },
  podiumRank: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    marginBottom: "20px",
  },
  goldMedal: {
    fontSize: "40px",
  },
  silverMedal: {
    fontSize: "40px",
  },
  bronzeMedal: {
    fontSize: "40px",
  },
  rankNumber: {
    fontSize: "24px",
    fontWeight: 800,
    opacity: 0.5,
  },
  cardContent: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  cardOrg: {
    fontSize: "20px",
    fontWeight: 700,
    lineHeight: 1.3,
    minHeight: "60px",
  },
  cardScore: {
    display: "flex",
    flexDirection: "column",
    gap: "5px",
    padding: "20px 0",
    borderTop: "1px solid rgba(255,255,255,0.1)",
    borderBottom: "1px solid rgba(255,255,255,0.1)",
  },
  scoreLabel: {
    fontSize: "12px",
    opacity: 0.6,
    textTransform: "uppercase",
    letterSpacing: "1px",
  },
  scoreValue: {
    fontSize: "42px",
    fontWeight: 900,
    background: "linear-gradient(135deg, #00f5ff, #7b2cbf)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  cardMeta: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  metaItem: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "13px",
    opacity: 0.8,
  },
  metaIcon: {
    fontSize: "16px",
  },
  deadline: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "14px",
    padding: "12px",
    background: "rgba(255,0,110,0.1)",
    borderRadius: "10px",
    border: "1px solid rgba(255,0,110,0.2)",
  },
  deadlineIcon: {
    fontSize: "16px",
  },
  viewDoc: {
    display: "inline-block",
    width: "100%",
    padding: "16px",
    marginTop: "10px",
    background: "rgba(255,255,255,0.05)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "12px",
    color: "#00f5ff",
    textDecoration: "none",
    textAlign: "center",
    fontSize: "14px",
    fontWeight: 600,
    transition: "all 0.3s ease",
  },
  viewDocFirst: {
    background: "linear-gradient(135deg, rgba(0,245,255,0.2), rgba(123,44,191,0.2))",
    border: "1px solid rgba(0,245,255,0.3)",
  },

  /* ============ LEADERBOARD TOGGLE ============ */
  toggleContainer: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "60px",
  },
  toggleBtn: {
    padding: "16px 40px",
    background: "rgba(255,255,255,0.05)",
    border: "1px solid rgba(0,245,255,0.3)",
    borderRadius: "999px",
    color: "#00f5ff",
    fontSize: "16px",
    fontWeight: 600,
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    transition: "all 0.3s ease",
  },
  toggleIcon: {
    fontSize: "14px",
  },

  /* ============ LEADERBOARD ============ */
  leaderboard: {
    maxWidth: "1200px",
    margin: "0 auto",
  },
  leaderTitle: {
    fontSize: "32px",
    fontWeight: 800,
    marginBottom: "30px",
    display: "flex",
    alignItems: "center",
    gap: "15px",
  },
  leaderIcon: {
    fontSize: "36px",
  },
  leaderboardGrid: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  leaderRow: {
    display: "grid",
    gridTemplateColumns: "80px 1fr 120px 150px",
    alignItems: "center",
    gap: "20px",
    padding: "20px 25px",
    background: "rgba(255,255,255,0.03)",
    backdropFilter: "blur(10px)",
    borderRadius: "16px",
    border: "1px solid rgba(255,255,255,0.08)",
    transition: "all 0.3s ease",
  },
  leaderRank: {
    display: "flex",
    alignItems: "center",
  },
  rankBadge: {
    padding: "8px 16px",
    background: "rgba(255,255,255,0.1)",
    borderRadius: "8px",
    fontSize: "16px",
    fontWeight: 700,
    color: "rgba(255,255,255,0.6)",
  },
  leaderInfo: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },
  leaderOrg: {
    fontSize: "16px",
    fontWeight: 600,
  },
  leaderMeta: {
    fontSize: "13px",
    opacity: 0.6,
  },
  leaderScore: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  scoreNum: {
    fontSize: "28px",
    fontWeight: 800,
    background: "linear-gradient(135deg, #00f5ff, #7b2cbf)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  scoreText: {
    fontSize: "11px",
    opacity: 0.5,
    textTransform: "uppercase",
  },
  leaderAction: {
    display: "flex",
    justifyContent: "flex-end",
  },
  leaderLink: {
    padding: "10px 24px",
    background: "rgba(0,245,255,0.1)",
    border: "1px solid rgba(0,245,255,0.3)",
    borderRadius: "8px",
    color: "#00f5ff",
    textDecoration: "none",
    fontSize: "14px",
    fontWeight: 600,
    transition: "all 0.3s ease",
  },
  techBtn: {
  marginTop: "10px",
  padding: "14px",
  width: "100%",
  borderRadius: "12px",
  border: "1px solid rgba(0,245,255,0.3)",
  background: "rgba(0,245,255,0.08)",
  color: "#00f5ff",
  fontSize: "14px",
  fontWeight: 600,
  cursor: "pointer",
  transition: "all 0.3s ease",
},

};

export default Home;

/* ============================================
   CSS ANIMATIONS - Injected into document
============================================ */
const styleSheet = document.createElement("style");
styleSheet.textContent = `
  @keyframes rotate3d {
    0% { transform: rotateX(0deg) rotateY(0deg); }
    100% { transform: rotateX(360deg) rotateY(360deg); }
  }
  
    @keyframes pulse {
    0% {
      transform: scale(0.6);
      opacity: 0.4;
    }
    50% {
      transform: scale(1.2);
      opacity: 1;
    }
    100% {
      transform: scale(0.6);
      opacity: 0.4;
    }
  }

  @keyframes glow {
    0% {
      opacity: 0.3;
      transform: translate(-50%, -50%) scale(1);
    }
    50% {
      opacity: 0.6;
      transform: translate(-50%, -50%) scale(1.2);
    }
    100% {
      opacity: 0.3;
      transform: translate(-50%, -50%) scale(1);
    }
  }

  @keyframes shimmer {
    0% {
      background-position: 0% center;
    }
    100% {
      background-position: 200% center;
    }
  }

  @keyframes float {
    0% {
      transform: translateX(-50%) translateY(0);
    }
    50% {
      transform: translateX(-50%) translateY(40px);
    }
    100% {
      transform: translateX(-50%) translateY(0);
    }
  }

  @keyframes bounce {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-12px);
    }
  }
`;
document.head.appendChild(styleSheet);
