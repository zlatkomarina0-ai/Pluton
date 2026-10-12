export default function HomePage() {
  return (
    <main style={{
      minHeight: '100vh',
      display: 'grid',
      placeItems: 'center',
      background: 'linear-gradient(135deg, #08131f 0%, #0d1c2d 100%)',
      color: '#edf4ff',
      fontFamily: 'Segoe UI, sans-serif'
    }}>
      <div style={{
        width: 'min(1100px, calc(100% - 32px))',
        background: 'rgba(17, 27, 40, 0.8)',
        border: '1px solid rgba(148, 176, 219, 0.18)',
        borderRadius: '22px',
        padding: '32px',
        boxShadow: '0 18px 50px rgba(8, 19, 31, 0.45)'
      }}>
        <p style={{ letterSpacing: '0.14em', textTransform: 'uppercase', color: '#7ef0c4', marginBottom: '12px' }}>
          PLUTON Phase 3
        </p>
        <h1 style={{ fontSize: 'clamp(2.2rem, 4vw, 4rem)', margin: '0 0 12px' }}>
          Intelligent system platform is live
        </h1>
        <p style={{ color: '#9bb0c8', maxWidth: '760px', lineHeight: 1.7 }}>
          The backend API is running, the frontend shell is prepared, and the sync engine scaffold is in place.
          This baseline is ready for the next stage of product logic and data integration.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginTop: '26px' }}>
          {[
            ['API', 'FastAPI /health endpoint'],
            ['Database', 'PostgreSQL ready'],
            ['Frontend', 'Next.js shell'],
            ['Sync', 'Phase 3 engine scaffold']
          ].map(([label, value]) => (
            <div key={label} style={{ padding: '18px', borderRadius: '16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ color: '#64e0ff', fontWeight: 700, marginBottom: '4px' }}>{label}</div>
              <div style={{ color: '#edf4ff' }}>{value}</div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
