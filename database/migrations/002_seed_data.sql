-- Insert roles
INSERT INTO roles (name, permissions) VALUES
('super_admin', '["*"]'::jsonb),
('admin', '["query", "document.read", "document.create", "audit.read"]'::jsonb),
('user', '["query", "document.read"]'::jsonb);

-- Insert test user (password is: Password123!)
-- This is bcrypt hash of "Password123!"
INSERT INTO users (email, password_hash, full_name, department, role_id) VALUES
('admin@company.com', 
 '$2a$12$E3SU7b/UW7wNWsvVWxHpIefeJq/xGuSUG7BueN9lhcaYs2Rvd4XFy', 
 'Admin User', 
 'IT', 
 1);