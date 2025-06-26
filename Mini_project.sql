USE voting;

CREATE TABLE users (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Full_name VARCHAR(100) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Date_of_birth DATE NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Aadhaar VARCHAR(100) NOT NULL,
    voter_id VARCHAR(100) UNIQUE,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM voters;
DROP TABLE IF EXISTS voters;
RENAME TABLE users TO voters;
ALTER TABLE voters
Modify Voter_id VARCHAR(100) UNIQUE;
ALTER TABLE voters
DROP COLUMN Username,
DROP COLUMN Password;
ALTER TABLE voters
ADD CONSTRAINT uc UNIQUE KEY(Aadhaar,Date_of_birth);
SELECT * FROM voters;
TRUNCATE TABLE voters;
SHOW TABLES;

CREATE TABLE Admins(
Id INT PRIMARY KEY AUTO_INCREMENT,
Username VARCHAR(100) UNIQUE,
Password VARCHAR(500) UNIQUE);

INSERT INTO Admins(Username, Password) VALUES('Abc','bcd');
SELECT * FROM Admins;

USE test;
SHOW TABLES;
SELECT * FROM admins;
SELECT * FROM voters;

CREATE TABLE candidates (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Full_name VARCHAR(100) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Date_of_birth DATE NOT NULL UNIQUE,
    Gender VARCHAR(10) NOT NULL,
    Party VARCHAR(25) NOT NULL,
    Vote_count INT NOT NULL DEFAULT 0
);
SELECT * FROM candidates;
ALTER TABLE candidates
MODIFY Gender VARCHAR(100) NOT NULL;
CREATE TABLE votes(
ID INT PRIMARY KEY AUTO_INCREMENT,
Voter_id VARCHAR(100) NOT NULL UNIQUE,
Candidate_id VARCHAR(100) NOT NULL);

ALTER TABLE votes
Modify Candidate_id INT NOT NULL;
ALTER TABLE votes
ADD CONSTRAINT fk1 FOREIGN KEY(Voter_id) REFERENCES voters(Voter_id),
ADD CONSTRAINT fk2 FOREIGN KEY(Candidate_id) REFERENCES candidates(ID);
SELECT * FROM votes;

DELETE FROM candidates WHERE ID = 2 OR ID = 5 OR ID = 6;


update candidates SET Full_name = 'Krishna', Party = 'D', Vote_count = 4 WHERE ID = 8;


