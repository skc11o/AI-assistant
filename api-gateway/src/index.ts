import dotenv from 'dotenv';
import Server from './app';
import { config } from './config';

// Load environment variables
dotenv.config({ path: '../.env' });

// Start server
const server = new Server();
server.start(config.port as number);