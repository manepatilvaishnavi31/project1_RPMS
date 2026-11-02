from dao.job_dao import JobDAO
from dao.company_dao import CompanyDAO
from model.entities import Job
from exception.errors import ValidationError
from util.logger import log

class JobService:
    def __init__(self): self.dao=JobDAO(); self.companies=CompanyDAO()
    def add_company(self,name,location,email):
        if not name.strip(): raise ValidationError("Company name is required.")
        cid=self.companies.add(name,location,email); log(f"Company Created: COM{cid:04d}"); return cid
    def companies_list(self): return self.companies.all()
    def add(self,j):
        if j.openings < 1 or j.package <= 0: raise ValidationError("Openings and package must be positive.")
        if not 0 <= j.minimum_percentage <= 100: raise ValidationError("Minimum percentage must be 0-100.")
        if j.maximum_backlogs < 0: raise ValidationError("Backlogs cannot be negative.")
        jid=self.dao.add(j); log(f"Job Created: JOB{jid:04d}"); return jid
    def all(self,open_only=False,term=None): return self.dao.all(open_only,term)
    def close(self,jid): self.dao.close(jid); log(f"Job Closed: JOB{jid:04d}")
    def update(self,jid,j): self.dao.update(jid,j); log(f"Job Updated: JOB{jid:04d}")
