import dotenv from 'dotenv';
import path from 'path';

// Load .env before reading process.env
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

export const config = {
  port: process.env.PORT || 4000,
  env: process.env.NODE_ENV || 'development',
  
  database: {
    url: process.env.DATABASE_URL || 'postgresql://ai_user:assistant123@localhost:5432/ai_assistant'
  },
  
  jwt: {
    secret: process.env.JWT_SECRET || 'your-secret-key-change-this-in-production',
    refreshSecret: process.env.JWT_REFRESH_SECRET || 'your-refresh-secret-change-this',
    expiresIn: '15m',
    refreshExpiresIn: '7d',
    issuer: 'ai-assistant'
  },
  
  services: {
    aiService: process.env.AI_SERVICE_URL || 'http://localhost:8000',
    governanceService: process.env.GOVERNANCE_SERVICE_URL || 'http://localhost:8080'
  },
  
  cors: {
    allowedOrigins: (process.env.CORS_ORIGINS || 'http://localhost:3000').split(',')
  }
};

console.log('Loaded DATABASE_URL:', config.database.url);
