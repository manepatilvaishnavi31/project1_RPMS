from dataclasses import dataclass

@dataclass
class Candidate:
    name: str
    email: str
    mobile: str
    qualification: str
    percentage: float
    passing_year: int
    technology: str
    backlog_count: int = 0

@dataclass
class Job:
    company_id: int
    title: str
    technology: str
    openings: int
    location: str
    package: float
    minimum_percentage: float
    passing_year: int
    maximum_backlogs: int
    deadline: str
