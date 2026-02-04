import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { ApiError } from '../types/errors';
import { AuthenticatedRequest, JWTPayload } from '../types/auth';

export const authMiddleware = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new ApiError(401, 'UNAUTHORIZED', 'No token provided');
    }

    const token = authHeader.substring(7);

    const decoded = jwt.verify(token, config.jwt.secret) as JWTPayload;

    (req as AuthenticatedRequest).user = {
      id: decoded.userId,
      email: decoded.email,
      role: decoded.role,
      department: decoded.department,
      permissions: decoded.permissions || [],
    };

    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      res.status(401).json({
        success: false,
        error: { code: 'TOKEN_EXPIRED', message: 'Token has expired' }
      });
    } else {
      res.status(401).json({
        success: false,
        error: { code: 'INVALID_TOKEN', message: 'Invalid token' }
      });
    }
  }
};

export const generateToken = (payload: Omit<JWTPayload, 'iat' | 'exp'>): string => {
  const token = jwt.sign(
    payload,
    config.jwt.secret,
    {
      expiresIn: '15m',
      issuer: 'ai-assistant',
    } as jwt.SignOptions
  );
  
  return token;
};
