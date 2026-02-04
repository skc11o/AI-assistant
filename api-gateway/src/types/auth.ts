import { Request } from 'express';

export interface JWTPayload {
  userId: string;
  email: string;
  role: string;
  department?: string;
  permissions: string[];
  iat?: number;
  exp?: number;
}

export interface UserContext {
  id: string;
  email: string;
  role: string;
  department?: string;
  permissions: string[];
}

export interface AuthenticatedRequest extends Request {
  user?: UserContext;
}