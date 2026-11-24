INSERT INTO Users
(
    FullName,
    Email,
    Phone,
    City,
    Password,
    Role
)
SELECT
    'Aarav Patil',
    'aarav@gmail.com',
    '9000000001',
    'Pune',
    Password,
    'Citizen'
FROM Users
WHERE UserID = 1;

INSERT INTO Users
(
    FullName,
    Email,
    Phone,
    City,
    Password,
    Role
)
SELECT
    'Sneha Joshi',
    'sneha@gmail.com',
    '9000000002',
    'Pune',
    Password,
    'Citizen'
FROM Users
WHERE UserID = 1;

INSERT INTO Users
(
    FullName,
    Email,
    Phone,
    City,
    Password,
    Role
)
SELECT
    'Rohan Kulkarni',
    'rohan@gmail.com',
    '9000000003',
    'Pune',
    Password,
    'Citizen'
FROM Users
WHERE UserID = 1;

INSERT INTO Users
(
    FullName,
    Email,
    Phone,
    City,
    Password,
    Role
)
SELECT
    'Ananya Deshmukh',
    'ananya@gmail.com',
    '9000000004',
    'Pune',
    Password,
    'Citizen'
FROM Users
WHERE UserID = 1;

SELECT UserID, FullName, Role
FROM Users;

