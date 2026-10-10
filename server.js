
const express = require('express');
const { Client } = require('pg');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Health endpoint за автоматизираниот тест
app.get('/api/health', async (req, res) => {
  try {
    // Проверка за конекција со PostgreSQL базата
    const client = new Client({ connectionString: process.env.DATABASE_URL });
    await client.connect();
    await client.query('SELECT 1');
    await client.end();
    
    res.status(200).json({ status: "ok", database: "healthy", timestamp: new Date() });
  } catch (err) {
    res.status(500).json({ status: "error", message: "Database connection failed", error: err.message });
  }
});

app.listen(port, () => {
  console.log(`PLUTON Engine running on port ${port}`);
});
