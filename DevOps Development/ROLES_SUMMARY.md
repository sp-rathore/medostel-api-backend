# Medostel Database - Roles & Users Summary

## Quick Reference

### Admin User
- **Username**: `medostel_admin_user`
- **Password**: `AdminSecure2024!`
- **Role**: `medostel_admin`
- **Privileges**: SUPERUSER, CREATEDB, CREATEROLE
- **Use Case**: Database administration, schema migrations, user management

### API User
- **Username**: `medostel_api_user`
- **Password**: `ApiSecure2024!`
- **Role**: `medostel_api`
- **Privileges**: SELECT, INSERT, UPDATE, DELETE (tables only)
- **Use Case**: Application API access, data operations only

---

## Connection Examples

### Quick Connect (Python)
```python
import psycopg2

# API Access
conn = psycopg2.connect(
    host="35.200.195.16",
    user="medostel_api_user",
    password="ApiSecure2024!",
    database="Medostel"
)
```

### Quick Connect (Node.js)
```javascript
const { Client } = require('pg');

const client = new Client({
    host: '35.200.195.16',
    user: 'medostel_api_user',
    password: 'ApiSecure2024!',
    database: 'Medostel'
});
client.connect();
```

### Quick Connect (bash/psql)
```bash
psql -h 35.200.195.16 -U medostel_api_user -d Medostel
```

---

## Permissions Matrix

| Operation | Admin | API |
|-----------|-------|-----|
| **SELECT** | ✓ | ✓ |
| **INSERT** | ✓ | ✓ |
| **UPDATE** | ✓ | ✓ |
| **DELETE** | ✓ | ✓ |
| **CREATE TABLE** | ✓ | ✗ |
| **DROP TABLE** | ✓ | ✗ |
| **CREATE SCHEMA** | ✓ | ✗ |
| **CREATE USER** | ✓ | ✗ |
| **GRANT PRIVILEGES** | ✓ | ✗ |
| **ALTER DATABASE** | ✓ | ✗ |

---

## Setup Instructions

### Step 1: Execute SQL Setup Script
```bash
cd /Users/shishupals/Documents/Claude/projects/Medostel\ project/

# Connect to the instance and execute the setup
gcloud sql connect medostel-ai-assistant-pgdev-instance \
  --user=postgres \
  --project=gen-lang-client-0064186167 < medostel_roles_setup.sql
```

### Step 2: Verify Users Were Created
```bash
psql -h 35.200.195.16 -U medostel_admin_user -d Medostel -c "\du"
```

### Step 3: Test API User Access
```bash
psql -h 35.200.195.16 -U medostel_api_user -d Medostel -c "SELECT now();"
```

---

## Security Checklist

- [ ] Change `AdminSecure2024!` to a strong password
- [ ] Change `ApiSecure2024!` to a strong password
- [ ] Enable SSL/TLS connections (currently: Encrypted Only)
- [ ] Whitelist IP addresses (currently: 0.0.0.0/0)
- [ ] Enable query logging for audit trail
- [ ] Set up automated backups
- [ ] Enable deletion protection (currently: enabled)
- [ ] Configure point-in-time recovery
- [ ] Monitor failed login attempts
- [ ] Rotate credentials every 90 days

---

## Database Info
- **Project**: gen-lang-client-0064186167
- **Instance**: medostel-ai-assistant-pgdev-instance
- **Database**: Medostel
- **Engine**: PostgreSQL 18
- **Region**: asia-south1
- **Public IP**: 35.200.195.16
- **Private IP**: 10.10.240.8
- **Port**: 5432

---

## Files in This Project
1. **medostel_roles_setup.sql** - SQL script to create roles and users
2. **API_ACCESS_GUIDE.md** - Comprehensive API access guide with examples
3. **ROLES_SUMMARY.md** - This quick reference document

---

## Next Steps
1. Run the SQL setup script
2. Verify users are created
3. Test connections with both users
4. Change passwords in production
5. Configure application to use API credentials
6. Set up monitoring and logging
