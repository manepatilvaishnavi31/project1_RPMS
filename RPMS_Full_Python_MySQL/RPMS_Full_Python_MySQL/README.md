# Recruitment & Placement Management System (RPMS)

Python + MySQL console application based on the Kiran Academy technical specification.

## Requirements
- Python 3.10+
- MySQL Server 8+
- VS Code (recommended)

## Setup
1. Install and start MySQL Server.
2. Open `config.py` and replace `your_mysql_password` with your MySQL password.
3. Open a terminal in this project folder:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python main.py
   ```
   On Linux, use `python3` if required.

The app creates `rpms_db` and its tables automatically. The MySQL account needs permission to create a database and tables.

## Project structure
- `model/`: Candidate and Job data classes
- `dao/`: MySQL database access and parameterized SQL
- `service/`: business rules and workflow
- `util/`: database connection and activity logger
- `exception/`: custom application exceptions
- `main.py`: console menu
- `sql/`: SQL reference
- `activity_log.txt`: generated automatically when actions are logged

## Implemented modules
- Candidate add, update, search, view all, deactivate
- Duplicate email/mobile prevention, percentage and backlog validation
- Company add and list
- Job create, update, view open/all, search, close
- Eligibility: active candidate, open job, valid deadline, technology, percentage, passing year and backlog checks
- Duplicate application prevention
- Recruitment workflow with allowed transitions only:
  `APPLIED -> SHORTLISTED -> INTERVIEW -> SELECTED -> OFFERED -> JOINED`
  Rejection can occur from applicable stages; invalid direct jumps are blocked.
- Interview scheduling and feedback ratings
- Offer and placement recording
- Reports: candidates by technology, open jobs, applications by status, company-wise placements, placed and unplaced candidates
- Activity logging

## Important
Use a test database for practice. The program is a console/backend application; the HTML/CSS prototype mentioned in the abstract is not included in this backend ZIP.
