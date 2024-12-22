-- 1. What are the most common crime types in each district?
SELECT 
    l.District,
    c.Type,
    COUNT(*) AS TotalIncidents
FROM Incident AS i
JOIN Location AS l ON i.Location_ID = l.ID
JOIN Crime AS c ON i.Crime_ID = c.ID
GROUP BY 
    l.District,
    c.Type
ORDER BY 
    l.District,
    TotalIncidents DESC;

-- 2. What is the average number of incidents per community area for each crime type?
SELECT 
    c.Type,
    l.Community_area,
    COUNT(DISTINCT i.ID) AS TotalIncidents,
    COUNT(DISTINCT l.ID) AS TotalCommunityAreas,
    CAST(COUNT(DISTINCT i.ID) AS REAL) / COUNT(DISTINCT l.ID) AS AvgIncidentsPerCommunityArea
FROM Incident AS i
JOIN Location AS l ON i.Location_ID = l.ID
JOIN Crime AS c ON i.Crime_ID = c.ID
GROUP BY 
    c.Type,
    l.Community_area
ORDER BY 
    c.Type,
    AvgIncidentsPerCommunityArea DESC;

-- 3. What is the distribution of incidents across different years for each crime type?
SELECT
    i.Year,
    c.Type,
    COUNT(*) AS TotalIncidents
FROM Incident AS i
JOIN Crime AS c ON i.Crime_ID = c.ID
GROUP BY
    i.Year,
    c.Type
ORDER BY
    i.Year,
    c.Type;
