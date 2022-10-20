import os
import sys
import getopt
import smtplib
import email.message
import mysql.connector
from datetime import datetime

def extract_database_data(ehrm_host, ehrm_user, ehrm_password, ehrm_database):
    try:
        mydb = mysql.connector.connect(
              host=ehrm_host,
              user=ehrm_user,
              password=ehrm_password,
              database=ehrm_database)
        mycursor = mydb.cursor()
        sql_select_Query = "select * from hs_hr_employee"
        mycursor.execute(sql_select_Query)
        hr_data = mycursor.fetchall()
        mydb.close()
        mycursor.close()
        return hr_data
    except:
        print("\nInformation","Can't connect to the eHRM database. Please recheck the database credentials")
        sys.exit(2)

def check_birthday(hr_data):
    try:
        detail_list = []
        for detail in hr_data:
            if detail[8] is not None:
                if detail[8].month == datetime.now().month and detail[8].day == datetime.now().day:
                    name = detail[3] + " " + detail[4] + " " + detail[2]
                    detail_list.append((name, detail[31]))
        return detail_list
    except:
        print("Error - 'Check birthday' function")

def email_send(name, email_addr, username, password, server, port, emailfrom, emailcc):
    try:
        with open(os.path.abspath( os.path.dirname( __file__ ))+"/assets/email_template.html", "r") as file:
            email_content3 = file.read()
        email_content = email_content3.replace('Reciver_Name', name)
    except:
        print("Can't find the email template, or a permission error")
        sys.exit(2)
    try:
        email_server = server +": "+ port
        msg = email.message.Message()
        msg['Subject'] = 'Wish You A Happy Birthday'
        msg['From'] = emailfrom
        msg['To'] = email_addr
        msg['Cc'] = emailcc
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)
        smtp = smtplib.SMTP(email_server)
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)
        print("email sent to: {} - {}".format(name, email_addr))
    except:
        print("Failed to send the email. Please check the email server credentials.")

def user_arg(argv):
    arg_dbhost = ""
    arg_dbuser = ""
    arg_dbpass = ""
    arg_db = ""
    arg_emailuser = ""
    arg_emailpass = ""
    arg_emailserv = ""
    arg_emailport = ""
    arg_emailfrom = ""
    arg_emailcc = ""
    arg_help = "{0} -H <dbhost> -U <dbuser> -P <dbpass> -D <dbname> -u <emailuser> -p <emailpass> -s <emailserv> -o <emailport> -f <emailfrom> -c <emailcc>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hH:U:P:D:u:p:s:o:f:c:", ["help", "dbhost=", 
        "dbuser=", "dbpass=", "dbname=", "emailuser=", "emailpass=", "emailserv=", "emailport=", "emailfrom=", "emailcc="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-H", "--dbhost"):
            arg_dbhost = arg
        elif opt in ("-U", "--dbuser"):
            arg_dbuser = arg
        elif opt in ("-P", "--dbpass"):
            arg_dbpass = arg
        elif opt in ("-D", "--dbname"):
            arg_db = arg
        elif opt in ("-u", "--emailuser"):
            arg_emailuser = arg
        elif opt in ("-p", "--emailpass"):
            arg_emailpass = arg
        elif opt in ("-s", "--emailserv"):
            arg_emailserv = arg
        elif opt in ("-o", "--emailport"):
            arg_emailport = arg
        elif opt in ("-f", "--emailfrom"):
            arg_emailfrom = arg
        elif opt in ("-c", "--emailcc"):
            arg_emailcc = arg

    return arg_dbhost, arg_dbuser, arg_dbpass, arg_db, arg_emailuser, arg_emailpass, arg_emailserv, arg_emailport, arg_emailfrom, arg_emailcc

def main():
    if __name__ == "__main__":
        dbhost, dbuser, dbpass, db, emailuser, emailpass, emailserv, emailport, emailfrom, emailcc = user_arg(sys.argv)
    hr_data = extract_database_data(dbhost, dbuser, dbpass, db)
    detail_list = check_birthday(hr_data)
    if detail_list != []: 
        for result in detail_list:
            email_send(result[0],result[1],emailuser, emailpass, emailserv, emailport, emailfrom, emailcc)

main()
