--Creating a seperate table for all the attribitue related to location
CREATE TABLE location (
ID INT PRIMARY KEY NOT NULL auto_increment,
location VARCHAR(100),
district VARCHAR(40),
community_area VARCHAR(40),
X_COORDS int,
Y_COORDS int,
latitude DECIMAL(10, 8),
longitude DECIMAL(10, 8),
geo_point varchar(30)
);

--Creating a table for crimes
CREATE TABLE crime (
ID INT PRIMARY KEY NOT NULL auto_increment,
type VARCHAR(50),
description VARCHAR(50)
);

--Populating the location and crime table with data
INSERT INTO location (location, district, community_area, X_COORDS, Y_COORDS, latitude, longitude, geo_point)
SELECT loc_deescrip, district, community_area, X_COORD, Y_COORD, latitude, longitude, location 
FROM incident;

INSERT INTO crime (type, description)
SELECT primary_type, descrip
FROM incident;

--Creating relationships between tables
ALTER TABLE incident
add column ID INT PRIMARY KEY NOT NULL auto_increment first,
ADD COLUMN location_ID INT,
ADD COLUMN crime_ID INT,
ADD CONSTRAINT fk_location_ID
FOREIGN KEY (location_ID)
REFERENCES location (ID),
ADD CONSTRAINT fk_crime_ID
FOREIGN KEY (crime_ID)
REFERENCES crime (ID),
DROP COLUMN primary_type,
DROP COLUMN descrip,
DROP COLUMN LOC_DEESCrip,
DROP COLUMN location,
DROP COLUMN district,
DROP COLUMN community_area,
DROP COLUMN X_COORD,
DROP COLUMN Y_COORD,
DROP COLUMN latitude,
DROP COLUMN longitude;

ALTER TABLE location
ADD COLUMN crime_ID INT,
add constraint fk_crime_incident
foreign key (crime_id)
references crime(id);