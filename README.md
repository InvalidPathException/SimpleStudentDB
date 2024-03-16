## COMP3005 A3Q1
Zhenxuan Ding 101269248

## Database setup
1. Open pgAdmin4 and create a new database
2. Run the scripts under `SQL Scripts` directory in the PSQL tool (`DDL.sql` then `DML.sql`)

## Running the program
1. To run the program, open the terminal and run: ```pip install psycopg``` (not psycopg2) and ```pip install prettytable```
2. Execute ```main.py``` in any way you want, but the environment must support console input
3. Assuming you have kept the default settings for PostgreSQL, enter the database name and your ```postgres``` user password
4. If you have altered the settings, edit the first lines of ```main.py``` to modify the username, host and port
5. After you successfully connect to the database, try each function out by entering 1, 2, 3, 4, or exit by entering 5