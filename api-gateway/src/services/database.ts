import { Pool } from 'pg';

// Get DATABASE_URL from environment
const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  console.error('DATABASE_URL is not set!');
  console.error('Current env vars:', Object.keys(process.env).filter(k => k.includes('DATA')));
  throw new Error('DATABASE_URL environment variable is required');
}

console.log('Database URL loaded:', databaseUrl.substring(0, 30) + '...');

// Create and export pool
export const pool = new Pool({
  connectionString: databaseUrl,
});

// Test connection
pool.on('connect', () => {
  console.log('Database connected successfully');
});

pool.on('error', (err) => {
  console.error('Database connection error:', err);
});
