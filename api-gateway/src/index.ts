import dotenv from 'dotenv';
import path from 'path';
import Server from './app';
import { config } from './config';

// Load environment variables from root .env file
const envPath = path.resolve(__dirname, '../../.env');
console.log('Loading .env from:', envPath);
dotenv.config({ path: envPath });

// Verify DATABASE_URL is loaded
console.log('DATABASE_URL:', process.env.DATABASE_URL ? 'Loaded' : 'NOT LOADED');

// Start server
const server = new Server();
server.start(config.port as number);
