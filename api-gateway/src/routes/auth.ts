import { Router, Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import { pool } from '../services/database';
import { generateToken } from '../middleware/auth';

const router = Router();

router.post('/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        success: false,
        error: { code: 'MISSING_FIELDS', message: 'Email and password required' }
      });
    }

    console.log('Attempting login for:', email);

    const result = await pool.query(
      `SELECT u.*, r.name as role_name, r.permissions 
       FROM users u 
       JOIN roles r ON u.role_id = r.id 
       WHERE u.email = $1 AND u.is_active = true`,
      [email]
    );

    if (result.rows.length === 0) {
      console.log('User not found:', email);
      return res.status(401).json({
        success: false,
        error: { code: 'INVALID_CREDENTIALS', message: 'Invalid email or password' }
      });
    }

    const user = result.rows[0];
    console.log('User found:', user.email);

    const isValid = await bcrypt.compare(password, user.password_hash);
    if (!isValid) {
      console.log('Invalid password for:', email);
      return res.status(401).json({
        success: false,
        error: { code: 'INVALID_CREDENTIALS', message: 'Invalid email or password' }
      });
    }

    const token = generateToken({
      userId: user.id,
      email: user.email,
      role: user.role_name,
      department: user.department,
      permissions: user.permissions || []
    });

    await pool.query('UPDATE users SET last_login = NOW() WHERE id = $1', [user.id]);

    console.log('Login successful for:', email);

    res.json({
      success: true,
      data: {
        access_token: token,
        expires_in: 900,
        user: {
          id: user.id,
          email: user.email,
          name: user.full_name,
          role: user.role_name
        }
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      error: { code: 'SERVER_ERROR', message: 'Internal server error' }
    });
  }
});

export default router;