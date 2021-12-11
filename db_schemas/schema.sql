CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    hiredate DATE DEFAULT CURRENT_DATE,
    is_manager BIT DEFAULT 0,
    date_created DATE DEFAULT CURRENT_DATE,
    active BIT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Competencies (
    competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    date_created DATE DEFAULT CURRENT_DATE,
    active BIT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competency_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    date_created DATE DEFAULT CURRENT_DATE,
    active BIT DEFAULT 1,
    FOREIGN KEY (competency_id) REFERENCES Competencies (competency_id)
);

CREATE TABLE IF NOT EXISTS Results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    date_taken DATE DEFAULT CURRENT_DATE,
    active BIT DEFAULT 1,
    FOREIGN KEY (assessment_id) REFERENCES Assessments (assessment_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);