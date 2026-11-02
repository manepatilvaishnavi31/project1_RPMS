from util.db import connect
from exception.errors import JobNotFoundError

class JobDAO:
    def add(self, j):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""INSERT INTO jobs(company_id,title,technology,openings,location,package,
            minimum_percentage,passing_year,maximum_backlogs,deadline)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (j.company_id,j.title,j.technology,j.openings,j.location,j.package,
             j.minimum_percentage,j.passing_year,j.maximum_backlogs,j.deadline))
            con.commit(); return cur.lastrowid
        finally: cur.close(); con.close()

    def all(self, open_only=False, search_term=None):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            q="""SELECT j.*,c.company_name FROM jobs j JOIN companies c ON j.company_id=c.company_id WHERE 1=1"""
            args=[]
            if open_only: q += " AND j.status='OPEN'"
            if search_term:
                q += " AND (j.title LIKE %s OR j.technology LIKE %s OR c.company_name LIKE %s)"
                like=f"%{search_term}%"; args += [like,like,like]
            q += " ORDER BY j.job_id DESC"
            cur.execute(q,args); return cur.fetchall()
        finally: cur.close(); con.close()

    def get(self, jid):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM jobs WHERE job_id=%s",(jid,))
            row=cur.fetchone()
            if not row: raise JobNotFoundError("Job not found.")
            return row
        finally: cur.close(); con.close()

    def close(self, jid):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("UPDATE jobs SET status='CLOSED' WHERE job_id=%s",(jid,))
            if cur.rowcount == 0: raise JobNotFoundError("Job not found.")
            con.commit()
        finally: cur.close(); con.close()

    def update(self, jid, j):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""UPDATE jobs SET company_id=%s,title=%s,technology=%s,openings=%s,location=%s,
            package=%s,minimum_percentage=%s,passing_year=%s,maximum_backlogs=%s,deadline=%s
            WHERE job_id=%s""",
            (j.company_id,j.title,j.technology,j.openings,j.location,j.package,j.minimum_percentage,
             j.passing_year,j.maximum_backlogs,j.deadline,jid))
            if cur.rowcount == 0: raise JobNotFoundError("Job not found.")
            con.commit()
        finally: cur.close(); con.close()
