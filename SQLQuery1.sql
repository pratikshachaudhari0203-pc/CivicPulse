USE CivicPulseDB;
GO

------------------------------------------------------------
-- 1. INSERT 6 NEW CITIZENS
------------------------------------------------------------

INSERT INTO Users
    (FullName, Email, Phone, City, Password, Role, CreatedAt)
VALUES
('Kabir Jadhav', 'kabir.jadhav@civicpulse.demo', '9000000011',
 'Pune', 'Citizen@123', 'Citizen', '2026-09-15 09:00:00'),

('Meera Bhosale', 'meera.bhosale@civicpulse.demo', '9000000012',
 'Pune', 'Citizen@123', 'Citizen', '2026-09-16 09:30:00'),

('Aditya More', 'aditya.more@civicpulse.demo', '9000000013',
 'Pune', 'Citizen@123', 'Citizen', '2026-09-17 10:00:00'),

('Riya Pawar', 'riya.pawar@civicpulse.demo', '9000000014',
 'Pune', 'Citizen@123', 'Citizen', '2026-09-18 10:30:00'),

('Omkar Shinde', 'omkar.shinde@civicpulse.demo', '9000000015',
 'Pune', 'Citizen@123', 'Citizen', '2026-09-19 11:00:00'),

('Neha Sawant', 'neha.sawant@civicpulse.demo', '9000000016',
 'Pune', 'Citizen@123', 'Citizen', '2026-09-20 11:30:00');

------------------------------------------------------------
-- 2. INSERT 24 COMPLAINTS
------------------------------------------------------------

INSERT INTO Complaints
(
    UserID,
    CategoryID,
    Description,
    Location,
    Priority,
    Status,
    ImagePath,
    OfficerID,
    CreatedAt,
    ResolvedAt
)
VALUES

-- KABIR JADHAV

(
 (SELECT UserID FROM Users WHERE Email='kabir.jadhav@civicpulse.demo'),
 1,
 'A large pothole has developed near the roadside and is creating difficulty for vehicles, especially two-wheelers.',
 'Bavdhan - Chandni Chowk Road',
 'High',
 'Resolved',
 NULL,
 2,
 '2026-09-18 09:15:00',
 '2026-09-21 15:30:00'
),

(
 (SELECT UserID FROM Users WHERE Email='kabir.jadhav@civicpulse.demo'),
 4,
 'The street light near the junction is not functioning properly and the area becomes poorly lit after evening.',
 'Camp - MG Road near the junction',
 'Medium',
 'In Progress',
 NULL,
 2,
 '2026-09-21 18:20:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='kabir.jadhav@civicpulse.demo'),
 3,
 'Garbage has been left near the roadside for several days and requires regular collection.',
 'Katraj - Market Road',
 'Medium',
 'Pending',
 NULL,
 NULL,
 '2026-09-24 11:10:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='kabir.jadhav@civicpulse.demo'),
 5,
 'Water is collecting near the roadside due to a drainage problem and is causing inconvenience to pedestrians.',
 'Dhayari - Narhe Road',
 'High',
 'Resolved',
 NULL,
 2,
 '2026-09-27 14:45:00',
 '2026-09-30 12:00:00'
),

-- MEERA BHOSALE

(
 (SELECT UserID FROM Users WHERE Email='meera.bhosale@civicpulse.demo'),
 6,
 'The public seating area requires cleaning and basic maintenance.',
 'Warje - Malwadi Road',
 'Low',
 'Pending',
 NULL,
 NULL,
 '2026-09-20 10:20:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='meera.bhosale@civicpulse.demo'),
 2,
 'Residents are experiencing reduced water supply and low water pressure in the area.',
 'Pashan - Sus Road',
 'High',
 'Resolved',
 NULL,
 2,
 '2026-09-23 09:30:00',
 '2026-09-26 16:00:00'
),

(
 (SELECT UserID FROM Users WHERE Email='meera.bhosale@civicpulse.demo'),
 1,
 'Several potholes have developed on the road and are affecting smooth movement of vehicles.',
 'Kondhwa - Khadi Machine Road',
 'Medium',
 'In Progress',
 NULL,
 2,
 '2026-09-29 13:10:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='meera.bhosale@civicpulse.demo'),
 4,
 'Street lighting is insufficient on this road and one of the lights is not working.',
 'Bibwewadi - Upper Indira Nagar Road',
 'Medium',
 'Pending',
 NULL,
 NULL,
 '2026-10-01 19:00:00',
 NULL
),

-- ADITYA MORE

(
 (SELECT UserID FROM Users WHERE Email='aditya.more@civicpulse.demo'),
 3,
 'Waste has accumulated near the roadside and is attracting stray animals. The area needs cleaning.',
 'Yerawada - Nagar Road junction',
 'High',
 'Resolved',
 NULL,
 2,
 '2026-09-22 10:00:00',
 '2026-09-25 15:00:00'
),

(
 (SELECT UserID FROM Users WHERE Email='aditya.more@civicpulse.demo'),
 5,
 'Drainage water is collecting along the roadside and creating an unpleasant smell.',
 'Swargate - Tilak Road',
 'Medium',
 'Pending',
 NULL,
 NULL,
 '2026-09-26 16:20:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='aditya.more@civicpulse.demo'),
 6,
 'The public area near the footpath needs cleaning and general maintenance.',
 'Deccan - Prabhat Road',
 'Low',
 'In Progress',
 NULL,
 2,
 '2026-10-02 09:25:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='aditya.more@civicpulse.demo'),
 1,
 'A pothole has developed near the junction and is creating difficulty for passing vehicles.',
 'Aundh - ITI Road',
 'High',
 'Pending',
 NULL,
 NULL,
 '2026-10-04 16:20:00',
 NULL
),

-- RIYA PAWAR

(
 (SELECT UserID FROM Users WHERE Email='riya.pawar@civicpulse.demo'),
 2,
 'Water pressure has been unusually low in the area and residents are facing difficulty with daily requirements.',
 'Kharadi - EON Road junction',
 'High',
 'Resolved',
 NULL,
 2,
 '2026-09-19 08:30:00',
 '2026-09-22 14:30:00'
),

(
 (SELECT UserID FROM Users WHERE Email='riya.pawar@civicpulse.demo'),
 4,
 'A street light along the road is not functioning and the area becomes dark after sunset.',
 'Viman Nagar - Airport Road',
 'Medium',
 'In Progress',
 NULL,
 2,
 '2026-09-25 19:15:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='riya.pawar@civicpulse.demo'),
 3,
 'Waste bins near the roadside are overflowing and require collection.',
 'Hadapsar - Gadital Road',
 'Low',
 'Pending',
 NULL,
 NULL,
 '2026-09-30 11:40:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='riya.pawar@civicpulse.demo'),
 5,
 'Drainage water is overflowing near the roadside and making the footpath difficult to use.',
 'Wakad - Datta Mandir Chowk',
 'High',
 'Resolved',
 NULL,
 2,
 '2026-10-03 13:00:00',
 '2026-10-06 17:20:00'
),

-- OMKAR SHINDE

(
 (SELECT UserID FROM Users WHERE Email='omkar.shinde@civicpulse.demo'),
 1,
 'The road surface has several damaged patches and potholes that are affecting traffic movement.',
 'Baner - Balewadi High Street Road',
 'Medium',
 'Resolved',
 NULL,
 2,
 '2026-09-17 09:40:00',
 '2026-09-20 16:30:00'
),

(
 (SELECT UserID FROM Users WHERE Email='omkar.shinde@civicpulse.demo'),
 6,
 'The public sitting area near the footpath needs cleaning and maintenance.',
 'Shivajinagar - FC Road junction',
 'Low',
 'Pending',
 NULL,
 NULL,
 '2026-09-28 12:15:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='omkar.shinde@civicpulse.demo'),
 2,
 'Residents have reported irregular water supply during the morning hours.',
 'Kothrud - Ideal Colony Road',
 'Medium',
 'In Progress',
 NULL,
 2,
 '2026-10-05 08:50:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='omkar.shinde@civicpulse.demo'),
 4,
 'Multiple street lights are not working and the road is poorly illuminated at night.',
 'Sinhagad Road - Anand Nagar',
 'High',
 'Pending',
 NULL,
 NULL,
 '2026-10-07 20:00:00',
 NULL
),

-- NEHA SAWANT

(
 (SELECT UserID FROM Users WHERE Email='neha.sawant@civicpulse.demo'),
 5,
 'Wastewater is collecting near the roadside because of a drainage issue.',
 'Kothrud - Dahanukar Colony Road',
 'Medium',
 'Resolved',
 NULL,
 2,
 '2026-09-16 10:30:00',
 '2026-09-19 15:45:00'
),

(
 (SELECT UserID FROM Users WHERE Email='neha.sawant@civicpulse.demo'),
 3,
 'Garbage has accumulated near the roadside and needs regular collection.',
 'Aundh - Parihar Chowk',
 'Medium',
 'In Progress',
 NULL,
 2,
 '2026-09-23 14:10:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='neha.sawant@civicpulse.demo'),
 6,
 'The public area near the footpath requires cleaning and maintenance.',
 'Camp - East Street',
 'Low',
 'Pending',
 NULL,
 NULL,
 '2026-10-06 15:10:00',
 NULL
),

(
 (SELECT UserID FROM Users WHERE Email='neha.sawant@civicpulse.demo'),
 1,
 'A large pothole near the roadside is causing difficulty for vehicles and may be unsafe for two-wheelers.',
 'Katraj - Pune-Satara Road',
 'High',
 'Pending',
 NULL,
 NULL,
 '2026-10-08 18:00:00',
 NULL
);

GO