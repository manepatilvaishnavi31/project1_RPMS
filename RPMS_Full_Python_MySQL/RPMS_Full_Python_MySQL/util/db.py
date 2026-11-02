import mysql.connector
from config import DB_CONFIG

def connect():
    return mysql.connector.connect(**DB_CONFIG)

def initialize_database():
    server_cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**server_cfg)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
    cur.close()
    conn.close()

    conn = connect()
    cur = conn.cursor()
    statements = [
    """CREATE TABLE IF NOT EXISTS candidates(
        candidate_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(120) NOT NULL UNIQUE,
        mobile VARCHAR(20) NOT NULL UNIQUE,
        qualification VARCHAR(100) NOT NULL,
        percentage DECIMAL(5,2) NOT NULL,
        passing_year INT NOT NULL,
        technology VARCHAR(150) NOT NULL,
        backlog_count INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS companies(
        company_id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(120) NOT NULL UNIQUE,
        location VARCHAR(120),
        contact_email VARCHAR(120)
    )""",
    """CREATE TABLE IF NOT EXISTS jobs(
        job_id INT AUTO_INCREMENT PRIMARY KEY,
        company_id INT NOT NULL,
        title VARCHAR(120) NOT NULL,
        technology VARCHAR(150) NOT NULL,
        openings INT NOT NULL,
        location VARCHAR(120),
        package DECIMAL(12,2) NOT NULL,
        minimum_percentage DECIMAL(5,2) NOT NULL,
        passing_year INT NOT NULL,
        maximum_backlogs INT NOT NULL DEFAULT 0,
        deadline DATE NOT NULL,
        status ENUM('OPEN','CLOSED') NOT NULL DEFAULT 'OPEN',
        FOREIGN KEY(company_id) REFERENCES companies(company_id)
    )""",
    """CREATE TABLE IF NOT EXISTS applications(
        application_id INT AUTO_INCREMENT PRIMARY KEY,
        candidate_id INT NOT NULL,
        job_id INT NOT NULL,
        status ENUM('APPLIED','SHORTLISTED','INTERVIEW','SELECTED','OFFERED','JOINED','REJECTED') NOT NULL DEFAULT 'APPLIED',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uq_candidate_job(candidate_id,job_id),
        FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id),
        FOREIGN KEY(job_id) REFERENCES jobs(job_id)
    )""",
    """CREATE TABLE IF NOT EXISTS interviews(
        interview_id INT AUTO_INCREMENT PRIMARY KEY,
        application_id INT NOT NULL,
        round_name VARCHAR(100) NOT NULL,
        interview_date DATETIME NOT NULL,
        mode VARCHAR(30) NOT NULL,
        interviewer VARCHAR(100) NOT NULL,
        status VARCHAR(30) NOT NULL DEFAULT 'SCHEDULED',
        FOREIGN KEY(application_id) REFERENCES applications(application_id)
    )""",
    """CREATE TABLE IF NOT EXISTS feedback(
        feedback_id INT AUTO_INCREMENT PRIMARY KEY,
        interview_id INT NOT NULL,
        technical_rating INT NOT NULL,
        communication_rating INT NOT NULL,
        remarks TEXT,
        result ENUM('PASS','FAIL','PENDING') NOT NULL DEFAULT 'PENDING',
        FOREIGN KEY(interview_id) REFERENCES interviews(interview_id)
    )""",
    """CREATE TABLE IF NOT EXISTS offers(
        offer_id INT AUTO_INCREMENT PRIMARY KEY,
        application_id INT NOT NULL UNIQUE,
        designation VARCHAR(120) NOT NULL,
        package DECIMAL(12,2) NOT NULL,
        offer_date DATE NOT NULL,
        joining_date DATE NOT NULL,
        status ENUM('PENDING','ACCEPTED','DECLINED') NOT NULL DEFAULT 'PENDING',
        FOREIGN KEY(application_id) REFERENCES applications(application_id)
    )""",
    """CREATE TABLE IF NOT EXISTS placements(
        placement_id INT AUTO_INCREMENT PRIMARY KEY,
        application_id INT NOT NULL UNIQUE,
        company_name VARCHAR(120) NOT NULL,
        designation VARCHAR(120) NOT NULL,
        package DECIMAL(12,2) NOT NULL,
        actual_joining_date DATE,
        joining_status ENUM('PENDING','JOINED','NOT_JOINED') NOT NULL DEFAULT 'PENDING',
        FOREIGN KEY(application_id) REFERENCES applications(application_id)
    )"""
    ]
    for sql in statements:
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
