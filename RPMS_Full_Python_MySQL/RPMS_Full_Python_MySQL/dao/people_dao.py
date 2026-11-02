from util.db import connect

class PeopleDAO:
    def add_interview(self, aid, round_name, date_time, mode, interviewer):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""INSERT INTO interviews(application_id,round_name,interview_date,mode,interviewer)
            VALUES(%s,%s,%s,%s,%s)""",(aid,round_name,date_time,mode,interviewer))
            con.commit(); return cur.lastrowid
        finally: cur.close(); con.close()

    def add_feedback(self, iid, technical, communication, remarks, result):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""INSERT INTO feedback(interview_id,technical_rating,communication_rating,remarks,result)
            VALUES(%s,%s,%s,%s,%s)""",(iid,technical,communication,remarks,result))
            con.commit()
        finally: cur.close(); con.close()

    def add_offer(self, aid, designation, package, offer_date, joining_date):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""INSERT INTO offers(application_id,designation,package,offer_date,joining_date)
            VALUES(%s,%s,%s,%s,%s)""",(aid,designation,package,offer_date,joining_date))
            cur.execute("UPDATE applications SET status='OFFERED' WHERE application_id=%s",(aid,))
            con.commit()
        finally: cur.close(); con.close()

    def add_placement(self, aid, company, designation, package, joining_date, joining_status):
        con=connect(); cur=con.cursor()
        try:
            cur.execute("""INSERT INTO placements(application_id,company_name,designation,package,
            actual_joining_date,joining_status) VALUES(%s,%s,%s,%s,%s,%s)""",
            (aid,company,designation,package,joining_date,joining_status))
            con.commit()
        finally: cur.close(); con.close()
