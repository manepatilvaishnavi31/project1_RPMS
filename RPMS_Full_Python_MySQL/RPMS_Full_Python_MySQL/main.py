from util.db import initialize_database
from model.entities import Candidate, Job
from service.candidate_service import CandidateService
from service.job_service import JobService
from service.application_service import ApplicationService
from service.report_service import ReportService
from exception.errors import *
from util.logger import log

cs=CandidateService(); js=JobService(); aps=ApplicationService(); rs=ReportService()

def integer(prompt, minimum=0):
    while True:
        try:
            n=int(input(prompt))
            if n < minimum: print(f"Enter a value >= {minimum}."); continue
            return n
        except ValueError: print("Enter a whole number.")

def number(prompt, minimum=0):
    while True:
        try:
            n=float(input(prompt))
            if n < minimum: print(f"Enter a value >= {minimum}."); continue
            return n
        except ValueError: print("Enter a valid number.")

def display(rows):
    if not rows: print("No records found."); return
    for row in rows:
        print("-"*60)
        for k,v in row.items(): print(f"{k}: {v}")

def candidate_menu():
    print("1 Add  2 Update  3 Search  4 View All  5 Deactivate")
    ch=input("Choice: ").strip()
    if ch in {"1","2"}:
        cid=integer("Candidate ID (only for update, enter 0 for add): ")
        data=Candidate(input("Name: ").strip(),input("Email: ").strip(),input("Mobile: ").strip(),
            input("Qualification: ").strip(),number("Percentage: ",0),integer("Passing year: ",2000),
            input("Technology (e.g. Python): ").strip(),integer("Backlog count: "))
        if ch=="1": print("Created Candidate ID:",cs.add(data))
        else: cs.update(cid,data); print("Candidate updated.")
    elif ch=="3": display(cs.search(input("Search name/technology/qualification: ")))
    elif ch=="4": display(cs.all())
    elif ch=="5": cs.deactivate(integer("Candidate ID: ",1)); print("Candidate deactivated.")
    else: print("Invalid choice.")

def job_menu():
    print("1 Add Company  2 List Companies  3 Create Job  4 Update Job  5 View Open Jobs  6 Search Jobs  7 Close Job  8 View All Jobs")
    ch=input("Choice: ").strip()
    if ch=="1":
        print("Company ID:",js.add_company(input("Company name: "),input("Location: "),input("Contact email: ")))
    elif ch=="2": display(js.companies_list())
    elif ch in {"3","4"}:
        jid=integer("Job ID (only for update, enter 0 for create): ")
        j=Job(integer("Company ID: ",1),input("Job title: "),input("Technology: "),
            integer("Openings: ",1),input("Location: "),number("Package: ",0.01),
            number("Minimum percentage: ",0),integer("Eligible passing year: ",2000),
            integer("Maximum backlogs: "),input("Deadline (YYYY-MM-DD): "))
        if ch=="3": print("Created Job ID:",js.add(j))
        else: js.update(jid,j); print("Job updated.")
    elif ch=="5": display(js.all(open_only=True))
    elif ch=="6": display(js.all(term=input("Search term: ")))
    elif ch=="7": js.close(integer("Job ID: ",1)); print("Job closed.")
    elif ch=="8": display(js.all())
    else: print("Invalid choice.")

def application_menu():
    print("1 Apply  2 View All  3 Filter by Status  4 Update Workflow Status")
    print("5 Schedule Interview  6 Add Interview Feedback  7 Create Offer  8 Record Placement")
    ch=input("Choice: ").strip()
    if ch=="1": print("Application ID:",aps.apply(integer("Candidate ID: ",1),integer("Job ID: ",1)))
    elif ch=="2": display(aps.all())
    elif ch=="3": display(aps.all(input("Status (APPLIED/SHORTLISTED/INTERVIEW/SELECTED/OFFERED/JOINED/REJECTED): ").upper()))
    elif ch=="4":
        aid=integer("Application ID: ",1); status=input("New status: ").upper()
        aps.transition(aid,status); print("Status updated.")
    elif ch=="5":
        aid=integer("Application ID (must be SHORTLISTED): ",1)
        iid=aps.interview(aid,input("Round name: "),input("Date/time YYYY-MM-DD HH:MM:SS: "),
            input("Mode (Online/Offline): "),input("Interviewer name: "))
        print("Interview ID:",iid)
    elif ch=="6":
        aps.feedback(integer("Interview ID: ",1),integer("Technical rating 1-5: ",1),
            integer("Communication rating 1-5: ",1),input("Remarks: "),input("Result PASS/FAIL/PENDING: ").upper())
        print("Feedback saved.")
    elif ch=="7":
        aps.offer(integer("Application ID (must be SELECTED): ",1),input("Designation: "),
            number("Package: ",0.01),input("Offer date YYYY-MM-DD: "),input("Joining date YYYY-MM-DD: "))
        print("Offer saved.")
    elif ch=="8":
        aps.placement(integer("Application ID: ",1),input("Company: "),input("Designation: "),
            number("Package: ",0.01),input("Actual joining date YYYY-MM-DD (blank if pending): ") or None,
            input("Joining status PENDING/JOINED/NOT_JOINED: ").upper())
        print("Placement saved.")
    else: print("Invalid choice.")

def report_menu():
    print("1 Candidates by Technology  2 Open Jobs  3 Applications by Status")
    print("4 Company-wise Placements  5 Placed Candidates  6 Unplaced Candidates")
    ch=input("Choice: ").strip()
    funcs={"1":rs.candidates_by_technology,"2":rs.open_jobs,"3":rs.applications_by_status,
           "4":rs.company_placements,"5":rs.placed_candidates,"6":rs.unplaced_candidates}
    if ch in funcs: display(funcs[ch]())
    else: print("Invalid choice.")

def main():
    initialize_database()
    print("\\n================================")
    print(" RECRUITMENT & PLACEMENT SYSTEM")
    print("================================")
    while True:
        print("\\n1 Candidates\\n2 Companies / Jobs\\n3 Applications / Interviews / Offers / Placements\\n4 Reports\\n5 Exit")
        ch=input("Select menu: ").strip()
        try:
            if ch=="1": candidate_menu()
            elif ch=="2": job_menu()
            elif ch=="3": application_menu()
            elif ch=="4": report_menu()
            elif ch=="5": print("Thank you!"); break
            else: print("Invalid menu option.")
        except (CandidateNotFoundError,JobNotFoundError,ApplicationNotFoundError,
                DuplicateApplicationError,CandidateNotEligibleError,ValidationError,
                InvalidStatusTransitionError) as e:
            print("ERROR:",e); log(f"ERROR: {e}")
        except Exception as e:
            print("Operation failed:",e); log(f"UNEXPECTED ERROR: {e}")

if __name__=="__main__":
    try: main()
    except Exception as e:
        print("Could not start. Check MySQL service, config.py password, and database permissions.")
        print("Details:",e)
