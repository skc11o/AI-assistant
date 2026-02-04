import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import { config } from './config';
import { authMiddleware } from './middleware/auth';
import authRoutes from './routes/auth';
import healthRoutes from './routes/health';

class Server {
  public app: Application;

  constructor() {
    this.app = express();
    this.configureMiddleware();
    this.configureRoutes();
  }

  private configureMiddleware(): void {
    this.app.use(helmet());
    this.app.use(cors({ origin: config.cors.allowedOrigins, credentials: true }));
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
    this.app.use(compression());
    this.app.use(morgan('dev'));
  }

  private configureRoutes(): void {
    const apiPrefix = '/api/v1';
    
    this.app.use(`${apiPrefix}/health`, healthRoutes);
    this.app.use(`${apiPrefix}/auth`, authRoutes);

    // Test route (protected)
    this.app.get(`${apiPrefix}/test`, authMiddleware, (req, res) => {
      res.json({ message: 'Protected route works!', user: (req as any).user });
    });

    this.app.use('*', (req, res) => {
      res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Route not found' }
      });
    });
  }

  public start(port: number): void {
    this.app.listen(port, () => {
      console.log(`API Gateway running on port ${port}`);
      console.log(`Health check: http://localhost:${port}/api/v1/health`);
    });
  }
}

export default Server;