from util.db import connect

class ReportService:
    def _query(self,sql,args=()):
        con=connect(); cur=con.cursor(dictionary=True)
        try: cur.execute(sql,args); return cur.fetchall()
        finally: cur.close(); con.close()

    def candidates_by_technology(self):
        return self._query("SELECT technology,COUNT(*) AS candidate_count FROM candidates WHERE is_active=TRUE GROUP BY technology ORDER BY technology")

    def open_jobs(self):
        return self._query("""SELECT j.job_id,j.title,c.company_name,j.technology,j.location,j.package,j.deadline
        FROM jobs j JOIN companies c ON j.company_id=c.company_id WHERE j.status='OPEN' ORDER BY j.deadline""")

    def applications_by_status(self):
        return self._query("SELECT status,COUNT(*) AS total FROM applications GROUP BY status ORDER BY status")

    def company_placements(self):
        return self._query("""SELECT company_name,COUNT(*) AS placed_candidates
        FROM placements WHERE joining_status='JOINED' GROUP BY company_name ORDER BY company_name""")

    def placed_candidates(self):
        return self._query("""SELECT c.name,c.email,p.company_name,p.designation,p.package,p.actual_joining_date
        FROM placements p JOIN applications a ON p.application_id=a.application_id
        JOIN candidates c ON a.candidate_id=c.candidate_id WHERE p.joining_status='JOINED'""")

    def unplaced_candidates(self):
        return self._query("""SELECT c.candidate_id,c.name,c.email,c.technology FROM candidates c
        WHERE c.is_active=TRUE AND c.candidate_id NOT IN
        (SELECT a.candidate_id FROM applications a JOIN placements p ON a.application_id=p.application_id
         WHERE p.joining_status='JOINED') ORDER BY c.name""")
