from util.db import connect
from exception.errors import ApplicationNotFoundError, DuplicateApplicationError
import mysql.connector

class ApplicationDAO:
    def apply(self, cid, jid):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("INSERT INTO applications(candidate_id,job_id) VALUES(%s,%s)",(cid,jid))
            con.commit(); return cur.lastrowid
        except mysql.connector.IntegrityError:
            con.rollback(); raise DuplicateApplicationError("Candidate has already applied for this job.")
        finally: cur.close(); con.close()

    def all(self, status=None):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            q="""SELECT a.*,c.name AS candidate_name,j.title AS job_title,co.company_name
                 FROM applications a JOIN candidates c ON a.candidate_id=c.candidate_id
                 JOIN jobs j ON a.job_id=j.job_id JOIN companies co ON j.company_id=co.company_id"""
            if status: q += " WHERE a.status=%s"; cur.execute(q,(status,))
            else: cur.execute(q)
            return cur.fetchall()
        finally: cur.close(); con.close()

    def get(self, aid):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            cur.execute("""SELECT a.*,c.name,c.is_active,c.percentage,c.passing_year,c.backlog_count,
            c.technology,j.title,j.status AS job_status,j.deadline,j.minimum_percentage,
            j.passing_year AS required_year,j.maximum_backlogs,j.technology AS required_technology,
            co.company_name FROM applications a JOIN candidates c ON a.candidate_id=c.candidate_id
            JOIN jobs j ON a.job_id=j.job_id JOIN companies co ON j.company_id=co.company_id
            WHERE a.application_id=%s""",(aid,))
            row=cur.fetchone()
            if not row: raise ApplicationNotFoundError("Application not found.")
            return row
        finally: cur.close(); con.close()

    def set_status(self, aid, status):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("UPDATE applications SET status=%s WHERE application_id=%s",(status,aid))
            if cur.rowcount == 0: raise ApplicationNotFoundError("Application not found.")
            con.commit()
        finally: cur.close(); con.close()
