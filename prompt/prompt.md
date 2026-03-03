# Prompt Tracking & Version Control

**Date**: 2026-03-03

1. Table name: User_master. Current schema of the table is below

    Column    │     Type     │ Nullable │      Default      │                                                        
  ├──────────────┼──────────────┼──────────┼───────────────────┤                                                        
  │ userid       │ varchar(100) │ NOT NULL │ -                 │                                                        
  ├──────────────┼──────────────┼──────────┼───────────────────┤                                                        
  │ firstname    │ varchar(50)  │ NOT NULL │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ lastname     │ varchar(50)  │ NOT NULL │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ currentrole  │ integer      │ NOT NULL │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ organisation │ varchar(100) │ YES      │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ emailid      │ varchar(100) │ NOT NULL │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ mobilenumber │ varchar(15)  │ NOT NULL │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ address1     │ varchar(255) │ YES      │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ address2     │ varchar(255) │ YES      │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ statename    │ varchar(100) │ YES      │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ cityname     │ varchar(100) │ YES      │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ pincode      │ varchar(10)  │ YES      │ -                 │
  ├──────────────┼──────────────┼──────────┼───────────────────┤
  │ status       │ varchar(20)  │ NOT NULL │ 'Active'  

    -   create a sql query script to drop the current table and create a new table of the same name with below query
        CREATE TABLE IF NOT EXISTS user_master (
            userId VARCHAR(100) PRIMARY KEY,
            firstName VARCHAR(50) NOT NULL,
            lastName VARCHAR(50) NOT NULL,
            currentRole VARCHAR(50) NOT NULL,
            emailId VARCHAR(255) NOT NULL UNIQUE CHECK (emailId ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
            mobileNumber NUMERIC(10) NOT NULL UNIQUE CHECK (mobileNumber >= 1000000000 AND mobileNumber <= 9999999999),
            organisation VARCHAR(255),
            address1 VARCHAR(255),
            address2 VARCHAR(255),
            stateId INTEGER,
            stateName VARCHAR(100),
            districtId INTEGER,
            cityId INTEGER,
            cityName VARCHAR(100),
            pinCode INTEGER,
            status VARCHAR(50) DEFAULT 'Active',
            createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (currentRole) REFERENCES user_role_master(roleId),
            FOREIGN KEY (stateId) REFERENCES state_city_pincode_master(stateId),
            FOREIGN KEY (districtId) REFERENCES state_city_pincode_master(districtId),
            FOREIGN KEY (cityId) REFERENCES state_city_pincode_master(cityId),
            FOREIGN KEY (pinCode) REFERENCES state_city_pincode_master(pinCode)
            );
        -   emailid and mobile number combination should be unique for each row. there cannot be duplicate rows in the table having a duplicate combination of email id and mobile number
        -   add a column for comment log VARCHAR(255) which will mention the most recent change done
        -  ensure that indexes are created as mentioned for this table in Agents/DB Dev Agent.md
    - APIs will be created for both Select and CRUD operation (no Delete operation required)
        - Select API should be able to fetch data based on following inputs
           -   email id or mobile phone number. it should fetch the unique row all columns from the table
           -   for email id or mobile number as input,  it should be able to provide a value already exist flag as ouput
           -   valud status are 'active' 'pending' 'deceased' 'inactive'
        -   PUT and POST APIs should be able to
            -   Insert a new user row, all column values need to be mandatorily provided except userid. userid should be an auto increment - max(userid) + 1. Both createdDate and updatedDate should be the system date
            -   Update API can be for a 
                -   status change (valid status are 'active' 'pending' 'deceased' 'inactive')
                -   first name, last name, organization, city, state, pincode, address1, address2, mobile number or email number. request can be to change one value or all values. in all scenarios userid remains the same.
                -   for any update request createdDate should not be changed and updatedDate should be the system date when the update operation is executed 
                - for all update requests comment log column should have valid comments
    
    - Create an overall plan and rewrite the Plan/API Development Plan.md that should comprise of updating
        - Agents/DB Dev Agent.md
        - Agents/API Dev Agent.md
        - Agents/API Unit Testing Agent.md
        - Agents/DBA Agent.md
        - DevOps/DBA/Databasespecs.md
        - DevOps/DBA/DEPLOYMENT_GUIDE.md
        - README.md
        - src/SQL files/create_Tables.sql
        - src/schemas/user_role.py
        - src/routes/v1/roles.py
    - Ensure that all respective dependent .md files and code is regenerated for this change.

*Last Updated: 2026-03-03*
