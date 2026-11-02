from util.db import connect
from exception.errors import CandidateNotFoundError, ValidationError
import mysql.connector

class CandidateDAO:
    def add(self, c):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""INSERT INTO candidates
            (name,email,mobile,qualification,percentage,passing_year,technology,backlog_count)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
            (c.name,c.email,c.mobile,c.qualification,c.percentage,c.passing_year,c.technology,c.backlog_count))
            con.commit(); return cur.lastrowid
        except mysql.connector.IntegrityError:
            con.rollback(); raise ValidationError("Email or mobile number already exists.")
        finally: cur.close(); con.close()

    def all(self, active_only=False):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            q="SELECT * FROM candidates"
            if active_only: q += " WHERE is_active=TRUE"
            q += " ORDER BY candidate_id"
            cur.execute(q); return cur.fetchall()
        finally: cur.close(); con.close()

    def get(self, cid):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM candidates WHERE candidate_id=%s",(cid,))
            row=cur.fetchone()
            if not row: raise CandidateNotFoundError("Candidate not found.")
            return row
        finally: cur.close(); con.close()

    def update(self, cid, c):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""UPDATE candidates SET name=%s,email=%s,mobile=%s,qualification=%s,
            percentage=%s,passing_year=%s,technology=%s,backlog_count=%s WHERE candidate_id=%s""",
            (c.name,c.email,c.mobile,c.qualification,c.percentage,c.passing_year,c.technology,c.backlog_count,cid))
            if cur.rowcount == 0: raise CandidateNotFoundError("Candidate not found.")
            con.commit()
        except mysql.connector.IntegrityError:
            con.rollback(); raise ValidationError("Email or mobile number already belongs to another candidate.")
        finally: cur.close(); con.close()

    def deactivate(self, cid):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("UPDATE candidates SET is_active=FALSE WHERE candidate_id=%s",(cid,))
            if cur.rowcount == 0: raise CandidateNotFoundError("Candidate not found.")
            con.commit()
        finally: cur.close(); con.close()

    def search(self, term):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            like=f"%{term}%"
            cur.execute("""SELECT * FROM candidates WHERE name LIKE %s OR technology LIKE %s
            OR qualification LIKE %s ORDER BY name""",(like,like,like))
            return cur.fetchall()
        finally: cur.close(); con.close()
