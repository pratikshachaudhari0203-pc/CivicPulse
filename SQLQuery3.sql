INSERT INTO Complaints
(
    UserID,
    CategoryID,
    Description,
    Location,
    Priority,
    Status,
    OfficerID,
    CreatedAt,
    ResolvedAt
)
VALUES

-- Pratiksha (UserID 1)
(1, 1, 'Large pothole causing problems for vehicles.', 'Shivaji Nagar', 'High', 'Resolved', 2, DATEADD(DAY,-30,GETDATE()), DATEADD(DAY,-24,GETDATE())),
(1, 3, 'Garbage has not been collected for several days.', 'Viman Nagar', 'High', 'In Progress', 2, DATEADD(DAY,-12,GETDATE()), NULL),
(1, 4, 'Street light is not working at night.', 'Camp', 'Medium', 'Pending', NULL, DATEADD(DAY,-5,GETDATE()), NULL),
(1, 2, 'Water pressure is very low in the area.', 'Aundh', 'Medium', 'Resolved', 2, DATEADD(DAY,-20,GETDATE()), DATEADD(DAY,-14,GETDATE())),

-- Aarav (UserID 3)
(3, 5, 'Drain is blocked and dirty water is collecting.', 'Kothrud', 'High', 'Resolved', 2, DATEADD(DAY,-28,GETDATE()), DATEADD(DAY,-20,GETDATE())),
(3, 1, 'Road surface is badly damaged near the junction.', 'Karve Road', 'Medium', 'In Progress', 2, DATEADD(DAY,-15,GETDATE()), NULL),
(3, 6, 'Public park needs cleaning and maintenance.', 'Model Colony', 'Low', 'Pending', NULL, DATEADD(DAY,-4,GETDATE()), NULL),
(3, 3, 'Overflowing garbage bins are creating a bad smell.', 'Hadapsar', 'Medium', 'Resolved', 2, DATEADD(DAY,-22,GETDATE()), DATEADD(DAY,-16,GETDATE())),

-- Sneha (UserID 4)
(4, 2, 'No water supply since yesterday morning.', 'Baner', 'High', 'In Progress', 2, DATEADD(DAY,-10,GETDATE()), NULL),
(4, 4, 'Several street lights are not working.', 'Wakad', 'High', 'Resolved', 2, DATEADD(DAY,-25,GETDATE()), DATEADD(DAY,-18,GETDATE())),
(4, 1, 'Multiple potholes are present on the main road.', 'Deccan', 'High', 'Pending', NULL, DATEADD(DAY,-3,GETDATE()), NULL),
(4, 5, 'Sewage water is overflowing onto the road.', 'Dhanori', 'High', 'In Progress', 2, DATEADD(DAY,-8,GETDATE()), NULL),

-- Rohan (UserID 5)
(5, 3, 'Waste is being dumped on the roadside.', 'Wadgaon', 'Medium', 'Pending', NULL, DATEADD(DAY,-6,GETDATE()), NULL),
(5, 6, 'Park benches are damaged and need repair.', 'Koregaon Park', 'Low', 'Resolved', 2, DATEADD(DAY,-27,GETDATE()), DATEADD(DAY,-19,GETDATE())),
(5, 1, 'Broken road patch is causing traffic problems.', 'Pashan', 'Medium', 'Resolved', 2, DATEADD(DAY,-21,GETDATE()), DATEADD(DAY,-13,GETDATE())),
(5, 4, 'Street light pole is damaged.', 'Katraj', 'Low', 'Pending', NULL, DATEADD(DAY,-2,GETDATE()), NULL),

-- Ananya (UserID 6)
(6, 5, 'Drainage cover is broken near the footpath.', 'Bibwewadi', 'Medium', 'Pending', NULL, DATEADD(DAY,-7,GETDATE()), NULL),
(6, 2, 'Water pipeline appears to be leaking.', 'Pashan', 'High', 'Resolved', 2, DATEADD(DAY,-29,GETDATE()), DATEADD(DAY,-21,GETDATE())),
(6, 3, 'Garbage collection vehicle has not arrived.', 'Kharadi', 'Medium', 'In Progress', 2, DATEADD(DAY,-11,GETDATE()), NULL),
(6, 6, 'Public garden area needs cleaning.', 'Aundh', 'Low', 'Resolved', 2, DATEADD(DAY,-17,GETDATE()), DATEADD(DAY,-10,GETDATE()));

SELECT COUNT(*) AS TotalComplaints
FROM Complaints;


SELECT
    u.FullName,
    COUNT(*) AS ComplaintCount
FROM Complaints c
JOIN Users u ON c.UserID = u.UserID
GROUP BY u.FullName
ORDER BY ComplaintCount DESC;

SELECT
    Status,
    COUNT(*) AS Total
FROM Complaints
GROUP BY Status;


SELECT
    cat.CategoryName,
    COUNT(*) AS Total
FROM Complaints c
JOIN Categories cat
    ON c.CategoryID = cat.CategoryID
GROUP BY cat.CategoryName
ORDER BY Total DESC;

SELECT
    Priority,
    COUNT(*) AS Total
FROM Complaints
GROUP BY Priority;