from dao.application_dao import ApplicationDAO
from dao.candidate_dao import CandidateDAO
from dao.job_dao import JobDAO
from dao.people_dao import PeopleDAO
from exception.errors import CandidateNotEligibleError, ValidationError, InvalidStatusTransitionError
from datetime import date
from util.logger import log

ALLOWED = {
    "APPLIED": {"SHORTLISTED", "REJECTED"},
    "SHORTLISTED": {"INTERVIEW", "REJECTED"},
    "INTERVIEW": {"SELECTED", "REJECTED"},
    "SELECTED": {"OFFERED", "REJECTED"},
    "OFFERED": {"JOINED", "REJECTED"},
    "JOINED": set(),
    "REJECTED": set()
}

class ApplicationService:
    def __init__(self):
        self.dao=ApplicationDAO(); self.candidates=CandidateDAO(); self.jobs=JobDAO(); self.people=PeopleDAO()

    def check_eligibility(self,candidate,job):
        reasons=[]
        if not candidate["is_active"]: reasons.append("Candidate is inactive.")
        if job["status"] != "OPEN": reasons.append("Job is not open.")
        if str(job["deadline"]) < str(date.today()): reasons.append("Application deadline has passed.")
        if float(candidate["percentage"]) < float(job["minimum_percentage"]): reasons.append("Percentage criteria not satisfied.")
        if int(candidate["passing_year"]) != int(job["passing_year"]): reasons.append("Passing year criteria not satisfied.")
        if int(candidate["backlog_count"]) > int(job["maximum_backlogs"]): reasons.append("Backlog criteria not satisfied.")
        if candidate["technology"].strip().lower() != job["technology"].strip().lower(): reasons.append("Required technology does not match.")
        return not reasons, reasons

    def apply(self,cid,jid):
        c=self.candidates.get(cid); j=self.jobs.get(jid)
        eligible,reasons=self.check_eligibility(c,j)
        if not eligible: raise CandidateNotEligibleError("NOT ELIGIBLE: "+" ".join(reasons))
        aid=self.dao.apply(cid,jid); log(f"Application Created: APP{aid:04d}"); return aid

    def all(self,status=None): return self.dao.all(status)

    def transition(self,aid,new_status):
        app=self.dao.get(aid); old=app["status"]; new_status=new_status.upper()
        if new_status not in ALLOWED.get(old,set()):
            raise InvalidStatusTransitionError(f"Invalid workflow transition: {old} -> {new_status}")
        self.dao.set_status(aid,new_status); log(f"Application {aid} status: {old} -> {new_status}")

    def interview(self,aid,round_name,dt,mode,interviewer):
        app=self.dao.get(aid)
        if app["status"] != "SHORTLISTED": raise InvalidStatusTransitionError("Only SHORTLISTED candidates can be scheduled for interview.")
        iid=self.people.add_interview(aid,round_name,dt,mode,interviewer)
        self.transition(aid,"INTERVIEW"); log(f"Interview Scheduled: INT{iid:04d}"); return iid

    def feedback(self,iid,technical,communication,remarks,result):
        if not 1 <= technical <= 5 or not 1 <= communication <= 5:
            raise ValidationError("Ratings must be between 1 and 5.")
        if result not in {"PASS","FAIL","PENDING"}: raise ValidationError("Result must be PASS, FAIL or PENDING.")
        self.people.add_feedback(iid,technical,communication,remarks,result)

    def offer(self,aid,designation,package,offer_date,joining_date):
        app=self.dao.get(aid)
        if app["status"] != "SELECTED": raise InvalidStatusTransitionError("Candidate must be SELECTED before offer creation.")
        if package <= 0: raise ValidationError("Package must be positive.")
        self.people.add_offer(aid,designation,package,offer_date,joining_date)
        log(f"Offer Created for Application: {aid}")

    def placement(self,aid,company,designation,package,joining_date,joining_status):
        app=self.dao.get(aid)
        if app["status"] not in {"OFFERED","JOINED"}: raise InvalidStatusTransitionError("Only offered/joined candidates can be placed.")
        if joining_status not in {"PENDING","JOINED","NOT_JOINED"}: raise ValidationError("Invalid joining status.")
        self.people.add_placement(aid,company,designation,package,joining_date,joining_status)
        if joining_status == "JOINED" and app["status"] == "OFFERED":
            self.transition(aid,"JOINED")
        log(f"Placement Recorded for Application: {aid}")
