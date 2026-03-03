# Medostel Database - API Access Guide

## Overview

The Medostel database has been configured with two distinct access levels:
1. **Admin Access** - Full database administration privileges
2. **API Access** - Limited read/write permissions for applications

---

## Credentials

### Admin User (Full Database Control)
```
Username: medostel_admin_user
Password: AdminSecure2024!
Role: medostel_admin
Privileges: Full CREATEDB, CREATEROLE, SUPERUSER
```

### API User (Application Access)
```
Username: medostel_api_user
Password: ApiSecure2024!
Role: medostel_api
Privileges: SELECT, INSERT, UPDATE, DELETE only
```

⚠️ **SECURITY WARNING**: Change these passwords immediately in a production environment!

---

## Database Connection Details

### Instance Information
- **Project**: gen-lang-client-0064186167 (Medostel - AI Assistant)
- **Instance**: medostel-ai-assistant-pgdev-instance
- **Database**: Medostel
- **Region**: asia-south1
- **Zone**: asia-south1-c

### Network Information
- **Public IP**: 35.200.195.16
- **Private IP**: 10.10.240.8
- **Port**: 5432
- **SSL/TLS**: Encrypted Only

---

## Method 1: Direct Connection (Public IP)

### Using psql (PostgreSQL CLI)

**Admin Connection:**
```bash
psql -h 35.200.195.16 -U medostel_admin_user -d Medostel
# When prompted, enter password: AdminSecure2024!
```

**API Connection:**
```bash
psql -h 35.200.195.16 -U medostel_api_user -d Medostel
# When prompted, enter password: ApiSecure2024!
```

### Using Python (psycopg2)

**Installation:**
```bash
pip install psycopg2-binary
```

**Admin Connection:**
```python
import psycopg2

conn = psycopg2.connect(
    host="35.200.195.16",
    port=5432,
    database="Medostel",
    user="medostel_admin_user",
    password="AdminSecure2024!"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
cursor.close()
conn.close()
```

**API Connection:**
```python
import psycopg2

conn = psycopg2.connect(
    host="35.200.195.16",
    port=5432,
    database="Medostel",
    user="medostel_api_user",
    password="ApiSecure2024!"
)

cursor = conn.cursor()
# Only SELECT, INSERT, UPDATE, DELETE queries work
cursor.execute("SELECT * FROM your_table;")
results = cursor.fetchall()
cursor.close()
conn.close()
```

### Using Node.js (pg library)

**Installation:**
```bash
npm install pg
```

**Admin Connection:**
```javascript
const { Client } = require('pg');

const client = new Client({
  host: '35.200.195.16',
  port: 5432,
  database: 'Medostel',
  user: 'medostel_admin_user',
  password: 'AdminSecure2024!'
});

client.connect();
client.query('SELECT NOW()', (err, res) => {
  console.log(res.rows[0]);
  client.end();
});
```

**API Connection:**
```javascript
const { Client } = require('pg');

const client = new Client({
  host: '35.200.195.16',
  port: 5432,
  database: 'Medostel',
  user: 'medostel_api_user',
  password: 'ApiSecure2024!'
});

client.connect();
client.query('SELECT * FROM your_table', (err, res) => {
  console.log(res.rows);
  client.end();
});
```

### Using Go

**Installation:**
```bash
go get github.com/lib/pq
```

**Code Example:**
```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/lib/pq"
)

func main() {
    connStr := "user=medostel_api_user password=ApiSecure2024! host=35.200.195.16 port=5432 dbname=Medostel sslmode=require"
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    var version string
    db.QueryRow("SELECT version()").Scan(&version)
    fmt.Println(version)
}
```

---

## Method 2: Cloud SQL Proxy (Recommended for GCP)

### Installation

**Using gcloud:**
```bash
gcloud components install cloud-sql-proxy
```

**Or download directly:**
https://github.com/GoogleCloudSQLProxy/cloud-sql-proxy/releases

### Using Proxy with Public IP

**Start the proxy:**
```bash
cloud-sql-proxy gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance
```

**Connect in another terminal:**
```bash
# Admin access
psql -h 127.0.0.1 -U medostel_admin_user -d Medostel

# API access
psql -h 127.0.0.1 -U medostel_api_user -d Medostel
```

### Using Proxy with Private IP

**Start the proxy with private IP:**
```bash
cloud-sql-proxy \
  --private-ip \
  gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance
```

**Connect from the same VPC:**
```bash
psql -h 127.0.0.1 -U medostel_api_user -d Medostel
```

### Python with Cloud SQL Proxy

```python
import psycopg2
from sshtunnel import SSHTunnelForwarder
import time
import subprocess
import os
import signal

# Start cloud-sql-proxy
proxy_process = subprocess.Popen([
    "cloud-sql-proxy",
    "gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance"
])

time.sleep(2)  # Wait for proxy to start

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="Medostel",
        user="medostel_api_user",
        password="ApiSecure2024!"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM your_table;")
    count = cursor.fetchone()[0]
    print(f"Rows in table: {count}")

    cursor.close()
    conn.close()
finally:
    proxy_process.terminate()
```

---

## Method 3: Connection Pooling (For High-Traffic APIs)

### Using PgBouncer (Recommended)

**Configuration file (pgbouncer.ini):**
```ini
[databases]
medostel = host=35.200.195.16 port=5432 dbname=Medostel

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 10
```

**Start PgBouncer:**
```bash
pgbouncer -d pgbouncer.ini
```

**Connect to pooled connection:**
```bash
psql -h localhost -p 6432 -U medostel_api_user -d medostel
```

### Using Python with SQLAlchemy (Connection Pooling)

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://medostel_api_user:ApiSecure2024!@35.200.195.16:5432/Medostel',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    echo=False
)

# Use the engine
with engine.connect() as connection:
    result = connection.execute("SELECT COUNT(*) FROM your_table;")
    print(result.fetchall())
```

---

## API Security Best Practices

### 1. **Environment Variables** (Never hardcode credentials)

```bash
# .env file
DB_HOST=35.200.195.16
DB_PORT=5432
DB_NAME=Medostel
DB_USER=medostel_api_user
DB_PASSWORD=ApiSecure2024!
```

**Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
```

### 2. **Rotate Passwords Regularly**

```sql
-- Change API user password
ALTER USER medostel_api_user WITH PASSWORD 'NewSecurePassword123!';

-- Change admin password
ALTER USER medostel_admin_user WITH PASSWORD 'NewAdminPassword456!';
```

### 3. **Monitor Access**

```sql
-- View recent connections and queries
SELECT
    pid,
    usename,
    application_name,
    state,
    query,
    state_change
FROM pg_stat_activity
WHERE datname = 'Medostel'
ORDER BY state_change DESC;

-- Log all queries (admin only)
ALTER DATABASE "Medostel" SET log_statement = 'all';
```

### 4. **Restrict API Role (Don't use for schema changes)**

API users cannot:
- ✗ CREATE/DROP tables
- ✗ CREATE/DROP schemas
- ✗ CREATE/DROP users/roles
- ✗ GRANT/REVOKE permissions
- ✗ Modify table structures
- ✓ SELECT data
- ✓ INSERT data
- ✓ UPDATE data
- ✓ DELETE data

---

## Connection String Examples

### Connection String Format
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Admin (Direct):**
```
postgresql://medostel_admin_user:AdminSecure2024!@35.200.195.16:5432/Medostel
```

**API (Direct):**
```
postgresql://medostel_api_user:ApiSecure2024!@35.200.195.16:5432/Medostel
```

**API (Via Proxy):**
```
postgresql://medostel_api_user:ApiSecure2024!@localhost:5432/Medostel
```

**API (Connection Pooled):**
```
postgresql://medostel_api_user:ApiSecure2024!@localhost:6432/medostel
```

---

## Troubleshooting

### Connection Refused
- Verify instance is RUNNABLE: `gcloud sql instances list`
- Check IP whitelisting: `gcloud sql instances describe medostel-ai-assistant-pgdev-instance`
- Verify Cloud SQL Admin API is enabled

### Authentication Failed
- Check username and password
- Verify user is created: `\du` in psql
- Check if user is locked (shouldn't happen)

### Permission Denied
- API user cannot CREATE/DROP tables (expected)
- Only admin can run DDL statements
- Check role membership: `\du+`

### Connection Timeout
- Check firewall rules
- Verify network connectivity
- Use Cloud SQL Proxy if behind firewall
- Check instance status

---

## Next Steps

1. **Execute the SQL setup script** to create roles:
   ```bash
   gcloud sql connect medostel-ai-assistant-pgdev-instance \
     --user=postgres --project=gen-lang-client-0064186167 < medostel_roles_setup.sql
   ```

2. **Test the connections** using the examples above

3. **Change the default passwords** immediately in production

4. **Set up backups** and monitoring

5. **Implement connection pooling** for production APIs

---

## Support Resources

- [Google Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Cloud SQL Proxy Documentation](https://cloud.google.com/sql/docs/postgres/sql-proxy)
- [PostgreSQL Security Best Practices](https://www.postgresql.org/docs/current/sql-syntax.html)
