from dao.candidate_dao import CandidateDAO
from model.entities import Candidate
from exception.errors import ValidationError

class CandidateService:
    def __init__(self): self.dao=CandidateDAO()
    def _validate(self, data):
        if not data.name.strip() or not data.email.strip() or "@" not in data.email:
            raise ValidationError("Name and valid email are required.")
        if not data.mobile.isdigit() or len(data.mobile) < 10:
            raise ValidationError("Mobile must contain at least 10 digits.")
        if not 0 <= data.percentage <= 100: raise ValidationError("Percentage must be from 0 to 100.")
        if data.backlog_count < 0: raise ValidationError("Backlog count cannot be negative.")
    def add(self, data):
        self._validate(data); cid=self.dao.add(data); log_activity(f"Candidate Created: CAN{cid:04d}"); return cid
    def update(self, cid, data):
        self._validate(data); self.dao.update(cid,data); log_activity(f"Candidate Updated: CAN{cid:04d}")
    def deactivate(self,cid):
        self.dao.deactivate(cid); log_activity(f"Candidate Deactivated: CAN{cid:04d}")
    def all(self): return self.dao.all()
    def search(self,term): return self.dao.search(term)

def log_activity(message):
    from util.logger import log
    log(message)
