# Prompt Tracking & Version Control

**Date**: 2026-03-03

1. Table name: new_User_request. 
    -  this table should have following columns
        - Request ID (PK) - numeric and starts from 1. Incremented for every new row added with max(requestid) + 1	
        - User id - will be the email id and should be validated for email id  
        - First Name	- character
        - Last Name	    - character
        - Current Role (FK)	- role name from user_role_master
        - Status	- default status should be pending
        - Organization	
        - Mobile	- 10 digit numeric
        - City_name (FK)	- should always be validated against the city name FROM STATE_CITY_PINCODE_MASTER
        - district_name (FK) - should always be validated against the DISTRICT name FROM STATE_CITY_PINCODE_MASTER
        - PINCODE (FK) - should always be validated against the PINCODE FROM STATE_CITY_PINCODE_MASTER
        - State_name (FK) - should always be validated against the STATE name FROM STATE_CITY_PINCODE_MASTER
        - created_Date - system timestamp
        - updated_Date - system timestamp

    - APIs will be created for both Select and CRUD operation (no Delete operation required)
        - Select API should be able to fetch data based on following inputs
           -   status as input and entire row all attributes should be fetched as output
        -   PUT and POST APIs should be able to
            -   Insert a new user request row, entire row should be added. Default status is pending when the row is inserted for first time
            -   Update API can be for a 
                -   status change - valid status to update is 'active' ' rejected' or 'pending'.
                - updated timestamp should be updated with system timestamp
        
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
