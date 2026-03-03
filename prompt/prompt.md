# Prompt Tracking & Version Control

**Date**: 2026-03-03

1. Table name: User_Login. 
    -   User_login table should contain below columns
        - user_id - this should be the email id value. this value should match the email id column value in user_master table
        - password should be hashed and fetching/inserting/updating should follow hash standards
        - mobile number - should be integer 10 digits and should match the mobile number in user_master table against the email id row
        - is_Active - if the status of user in user_master is 'active' then only this flag should be set to 'Y'. Otherwise this flag should be 'N'
        - lAST_LOGIN - this is the system timestamp. for first time login this column will have the system timestamp. 
        - created_date - this value should be system timestamp for the first time user login was created
        - updated_Date - this value should be same as created date for first time. whenever password is changed then only this value should get updated

    - APIs will be created for both Select and CRUD operation (no Delete operation required)
        - Select API should be able to fetch data based on following inputs
           -   email id or mobile phone number. it should fetch the password, unhash it and provide as output. it should provide the value of is_Active flag in the output.
        -   PUT and POST APIs should be able to
            -   Insert a new user login row, email id should be validated against the email id in user_master, mobile number should be validated against the mobile number column of same row of email id provided. if password field is empty then default password 'Medostel@AI2026' should be hashed and inserted. last_login, created_date and updated_date should be the system timestamp values
            -   Update API can be for a 
                -   password change - in this case change the password, hash it and store. created_Date remains unchanged. last_login and updated_Date values are current system_Date
                - last_login - whenever a select api is successful this update api should be triggered to update the row with last_login column update with current system timestamp. all other column values remain unchanged.
                - is_Active flag status can be changed to 'Y' or 'N'. in this case only updated_Date should be changed along with is_Active flag value
                
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
