# Medostel Database - Credentials

⚠️ **SECURITY WARNING**: Store this file securely. Never commit to git or share publicly.

## Created: 2026-02-28

---

## Database Connection Details

| Property | Value |
|----------|-------|
| **Project** | gen-lang-client-0064186167 |
| **Instance** | medostel-ai-assistant-pgdev-instance |
| **Database** | Medostel |
| **Host** | 35.200.195.16 |
| **Private IP** | 10.10.240.8 |
| **Port** | 5432 |
| **Engine** | PostgreSQL 18 |
| **Region** | asia-south1 |

---

## Google Cloud Proxy string:
Prompt: Initiate Google Cloud SQL proxy using admin user credentials from Credentials.md file in DevOps folder. Use asia-south1 as the region

use the below string to set the connection:
cloud-sql-proxy gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance --port=5432              

   Start Cloud SQL Proxy connection to medostel-ai-assistant-pgdev-instance

## Admin User Credentials

```
Username: medostel_admin_user
Password: Iag2bMi@0@6aA
Role: medostel_admin
Privileges: SUPERUSER, CREATEDB, CREATEROLE
```

**Use Case**: Database administration, schema migrations, user management

**Connection String**:
```
postgresql://medostel_admin_user:Iag2bMi@0@6aA@35.200.195.16:5432/Medostel
```

---

## API User Credentials

```
Username: medostel_api_user
Password: Iag2bMi@0@6aD
Role: medostel_api
Privileges: SELECT, INSERT, UPDATE, DELETE (tables only)
```

**Use Case**: Application API access with limited permissions

**Connection String**:
```
postgresql://medostel_api_user:Iag2bMi@0@6aD@35.200.195.16:5432/Medostel
```

---

## Environment Variables

Store these in your `.env` file (never commit to git):

```bash
# Admin Access
MEDOSTEL_ADMIN_HOST=35.200.195.16
MEDOSTEL_ADMIN_PORT=5432
MEDOSTEL_ADMIN_USER=medostel_admin_user
MEDOSTEL_ADMIN_PASSWORD=Iag2bMi@0@6aA
MEDOSTEL_ADMIN_DB=Medostel

# API Access
MEDOSTEL_API_HOST=35.200.195.16
MEDOSTEL_API_PORT=5432
MEDOSTEL_API_USER=medostel_api_user
MEDOSTEL_API_PASSWORD=Iag2bMi@0@6aD
MEDOSTEL_API_DB=Medostel
```

---

## Quick Connection Tests

### Test Admin Access (Python)
```python
import psycopg2

conn = psycopg2.connect(
    host="35.200.195.16",
    port=5432,
    database="Medostel",
    user="medostel_admin_user",
    password="Iag2bMi@0@6aA"
)
print("Admin connection successful!")
conn.close()
```

### Test API Access (Python)
```python
import psycopg2

conn = psycopg2.connect(
    host="35.200.195.16",
    port=5432,
    database="Medostel",
    user="medostel_api_user",
    password="Iag2bMi@0@6aD"
)
print("API connection successful!")
conn.close()
```

### Test with psql
```bash
# Admin
psql -h 35.200.195.16 -U medostel_admin_user -d Medostel

# API
psql -h 35.200.195.16 -U medostel_api_user -d Medostel
```

---

## Security Checklist

- [x] Roles created
- [x] Users created with strong passwords
- [x] Permissions configured
- [ ] Passwords stored in secure location
- [ ] Credentials in `.env` file (not in git)
- [ ] First test connection completed
- [ ] Applications configured with credentials
- [ ] Rotation schedule set (every 90 days)
- [ ] Access logging enabled
- [ ] Monitoring configured

---

## Credentials Management

### Storing in Environment Variables
```bash
export MEDOSTEL_API_PASSWORD='Iag2bMi@0@6aD'
export MEDOSTEL_ADMIN_PASSWORD='Iag2bMi@0@6aA'
```

### Using with Docker
```dockerfile
FROM python:3.11
ENV MEDOSTEL_API_USER=medostel_api_user
ENV MEDOSTEL_API_PASSWORD=Iag2bMi@0@6aD
ENV MEDOSTEL_API_HOST=35.200.195.16
```

### Using with Kubernetes Secrets
```bash
kubectl create secret generic medostel-db-credentials \
  --from-literal=api-user=medostel_api_user \
  --from-literal=api-password=Iag2bMi@0@6aD \
  --from-literal=admin-user=medostel_admin_user \
  --from-literal=admin-password=Iag2bMi@0@6aA
```

---

## Password Rotation

Change passwords every 90 days using:
```sql
ALTER USER medostel_api_user WITH PASSWORD 'NewPassword';
ALTER USER medostel_admin_user WITH PASSWORD 'NewPassword';
```

Update this file after each rotation.

---

## Important Notes

1. **Never share** these credentials publicly
2. **Always use** HTTPS/SSL for connections
3. **Rotate** passwords every 90 days
4. **Monitor** failed login attempts
5. **Use** different passwords for different environments (dev/staging/prod)
6. **Store** in secure vault (AWS Secrets Manager, Google Secret Manager, etc.)
7. **Audit** all administrative changes
