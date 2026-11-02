from util.db import connect

class CompanyDAO:
    def add(self, name, location, email):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("INSERT INTO companies(company_name,location,contact_email) VALUES(%s,%s,%s)",
                        (name,location,email))
            con.commit(); return cur.lastrowid
        finally: cur.close(); con.close()
    def all(self):
        con=connect(); cur=con.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM companies ORDER BY company_name"); return cur.fetchall()
        finally: cur.close(); con.close()
