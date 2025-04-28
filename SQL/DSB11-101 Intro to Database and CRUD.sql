-- # 101 Intro to Database and CRUD
-- # 1. Create Table
CREATE TABLE employee (
  id INT UNIQUE,
  name TEXT,
  department TEXT,
  position TEXT,
  salary REAL
 );

-- # 2. Insert Data
INSERT INTO employee 
VALUES 
(1, 'A-nan', 'Maomao Company', 'CEO', 100000),
(2, 'Noi', 'Sale & Marketing', 'VP', 200000),
(3, 'Mek', 'IT', 'Employee', 18000);

-- # 3. Select Data
SELECT
	name, department, position, salary
FROM employee
LIMIT 2;

-- # 4. Transform Columns
SELECT
	firstname,
  lastname,
  firstname || ' ' || lastname as fullname,
  LOWER(firstname) || '@gmail.com' as email
FROM customers
LIMIT 15;

SELECT
	name,
    ROUND(milliseconds/60000.0, 2) AS minutes,
    ROUND(bytes/ (1024.0*1024.0), 2) AS mb
FROM tracks;

-- 5. Filter Data
SELECT
	name, department, position, salary
FROM employee
WHERE salary > 15000;

SELECT
	name, department, position, salary
FROM employee
WHERE salary > 15000 AND department = 'IT';

-- 6. Update Data
UPDATE employee
SET salary = 20000
WHERE id = 3;

SELECT * FROM employee;

-- 7. Delete Data
DELETE FROM employee
WHERE name = 'Noi';

SELECT * FROM employee;

-- 8. Alter Table
ALTER TABLE employee 
ADD email TEXT;

SELECT * FROM employee;

-- 9. Copy and Drop Table
CREATE TABLE employee_bu AS
SELECT * FROM employee;

DROP TABLE employee_bu;