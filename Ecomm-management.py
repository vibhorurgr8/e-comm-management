import sqlite3 #to use sql within py

new_pswd = 1000
connection = sqlite3.connect("prod.db") #db_name
cursor = connection.cursor() #will be used to traverse

try: #creating prod table
    sql_command ="""CREATE TABLE prod ( 
    pid INTEGER PRIMARY KEY,
    pname VARCHAR(10),
    pdesc VARCHAR(30),
    pqty INTEGER,
    pprice INTEGER);"""
    cursor.execute(sql_command)
except: # if prod table already exists
    pass

try: #creating user table
    cursor.execute("""CREATE TABLE user (
    uid INTEGER PRIMARY KEY,
    name VARCHAR(10),
    uname VARCHAR(30) UNIQUE,
    pswd VARCHAR(10),
    email VARCHAR(25) UNIQUE,
    mob VARCHAR(12) UNIQUE);""")
except: #if user table already exists
    pass

try: #creating cart table
    cursor.execute("""CREATE TABLE cart (
    uid INTEGER,
    pid INTEGER,
    pqty INTEGER);""")
except: #if cart table already exists
    pass

try: #adding status col in cart table
    cursor.execute("""ALTER TABLE user ADD UNIQUE (uname);""") 
except: #if status col already presesnt
    pass 

print("Choose one from options below")
login_choice = int(input("1. ADMIN_LOGIN \n2. USER_LOGIN \n3. Not a user yet?\n4.Forgot Password?\n")) #requesting login choice

if login_choice == 1: #if admin login
    if int(input("Enter PASSWORD\n")) == 1234: #validating admin
        admin_choice = int(input("1. Add PROD\n2. View PROD\n3. Modify PROD\n4. Delete PROD\n5. Check ORDERS\n")) #admin powers

        if admin_choice == 1: #admin_addprod
            cursor.execute("""INSERT INTO prod VALUES(NULL, "{0}", "{1}", {2}, {3});""".format(input("Enter Name "), input("Enter prod desciption "), int(input("Enter prod qty ")), int(input("Enter prod price "))))
            cursor.execute("""SELECT * FROM PROD;""")
            result = cursor.fetchall()
            print("PID            PNAME          PDESC          PQTY           PPRICE")
            print("__________________________________________________________________\n")
            
            for x in result:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")
        elif admin_choice == 2: #admin_
            cursor.execute("""SELECT * FROM PROD;""")
            result = cursor.fetchall()
            print("PID            PNAME          PDESC          PQTY           PPRICE")
            print("__________________________________________________________________\n")
            
            for x in result:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")

        elif admin_choice == 3:
            cursor.execute("""SELECT * FROM PROD;""")
            result = cursor.fetchall()
            print("PID            PNAME          PDESC          PQTY           PPRICE")
            print("__________________________________________________________________\n")
            
            for x in result:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")

            cursor.execute("""UPDATE prod SET pname = ?, pdesc = ?, pqty = ?,pprice = ? WHERE pid = ? """,(input("Enter PNAME"), input("Enter DESC"), int(input("Enter PQTY")), int(input("Enter PPRICE")), int(input("Enter PID"))))

            cursor.execute("""SELECT * FROM PROD;""")
            result = cursor.fetchall()
            print("PID            PNAME          PDESC          PQTY           PPRICE")
            print("__________________________________________________________________\n")
            
            for x in result:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")
        elif admin_choice == 4:
            cursor.execute("""SELECT * FROM PROD;""")
            result = cursor.fetchall()
            print("PID            PNAME          PDESC          PQTY           PPRICE")
            print("__________________________________________________________________\n")
            
            for x in result:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")
            
            cursor.execute("""DELETE FROM prod WHERE pid = ?""",input("Enter PID of PROD to be deleted"))

            cursor.execute("""SELECT * FROM PROD;""")
            result = cursor.fetchall()
            print("PID            PNAME          PDESC          PQTY           PPRICE")
            print("__________________________________________________________________\n")
            
            for x in result:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")

        elif admin_choice == 5:
            cursor.execute("""SELECT * FROM cart WHERE status = 1""")
            check_ord = cursor.fetchall()
            print("UID            PID            PQTY           STATUS")
            print("_____________________________________")
            for x in check_ord:
                for y in x:
                    print(y,end=" "*(15-len(str(y))))
                print("\n")
            

        else:
            print("Wrong INPUT")

    else:
        print("Wrong PASSWORD") 

elif login_choice == 2:
        cursor.execute("""SELECT uid FROM user WHERE uname = ? AND pswd = ?""",(input("Enter uname"),input("Enter pswd")))
        result = cursor.fetchone()
        if result:
            res = int(''.join(map(str, result)))           

        if result:
            print("WELCOME")
            user_choice = int(input("1. Add product\n2. Remove Product\n3. Place Order\n4. View CART"))
            
            if user_choice == 1:
                cursor.execute("""SELECT * FROM PROD;""")
                result = cursor.fetchall()
                print("PID            PNAME          PDESC          PQTY           PPRICE")
                print("__________________________________________________________________\n")
            
                for x in result:
                    for y in x:
                        print(y,end=" "*(15-len(str(y))))
                    print("\n")

                proid = input("Enter prodid")
                proqty = int(input("Enter prodqty"))

                cursor.execute("""SELECT pqty FROM prod WHERE pid = {0}""".format(proid))
                pqty_avail = cursor.fetchone()
                pqty_avail = int(''.join(map(str, pqty_avail)))

                if pqty_avail>=proqty:

                    cursor.execute("""SELECT pid FROM cart where uid= {0} """.format(res))
                    pidtuple = cursor.fetchall()
                    pidi = str(''.join(map(str, pidtuple)))
                
                    if proid in pidi:
                        cursor.execute("""UPDATE cart SET pqty = pqty + {0} WHERE uid = {1}  AND pid = {2}""".format(proqty, res, proid))
                    else:
                        cursor.execute("""INSERT INTO cart VALUES(?,?,?,NULL)""",(res, proid,  proqty))

                    cursor.execute("""SELECT * FROM cart where uid = {0} """.format(res))
                    result = cursor.fetchall()
                    print("UID            PID            PQTY")
                    print("________________________")
            
                    for x in result:
                        for y in x:
                            print(y,end=" "*(15-len(str(y))))
                        print("\n")

                    cursor.execute("""UPDATE prod SET pqty = pqty - {0} WHERE pid = {1}""".format(proqty, proid))

                else:

                    print("proqty is greater than pqty_avail")

            elif user_choice == 2:
                remove_choice = int(input("1. Remove PROD\n2. Decrease Qty"))

                if remove_choice == 1:
                    cursor.execute("""SELECT * FROM cart where uid = {0} """.format(res))
                    result = cursor.fetchall()
                    print("UID            PID            PQTY")
                    print("________________________")
            
                    for x in result:
                        for y in x:
                            print(y,end=" "*(15-len(str(y))))
                        print("\n")

                    proid = input("Enter proid of prod\n")
                    cursor.execute("""SELECT pqty FROM cart WHERE pid = {0} AND uid = {1}""".format(proid, res))
                    rem_qty = cursor.fetchone()
                    rem_qty = str(''.join(map(str, rem_qty)))
                                                        
                    cursor.execute("DELETE FROM cart WHERE pid = {0} AND uid = {1}""".format(proid, res))

                    cursor.execute("""UPDATE prod SET pqty = pqty + {0} WHERE pid = {1}""".format(rem_qty, proid))

                    cursor.execute("""SELECT * FROM cart where uid = {0} """.format(res))
                    result = cursor.fetchall()
                    print("UID            PID            PQTY")
                    print("________________________")
            
                    for x in result:
                        for y in x:
                            print(y,end=" "*(15-len(str(y))))
                        print("\n")

                elif remove_choice == 2:
                    cursor.execute("""SELECT * FROM cart where uid = {0} """.format(res))
                    result = cursor.fetchall()
                    print("UID            PID            PQTY")
                    print("________________________")
            
                    for x in result:
                        for y in x:
                            print(y,end=" "*(15-len(str(y))))
                        print("\n")

                    proid = input("Enter pid")
                    proqty = int(input("Enter qty to decrease"))

                    cursor.execute("""UPDATE cart SET pqty = pqty - {0} WHERE pid = {1} AND uid = {1}""".format(proqty,  proid, res))
                    cursor.execute("""UPDATE prod SET pqty = pqty + {0} WHERE pid = {1}""".format(proqty, proid))

                    cursor.execute("""SELECT * FROM cart where uid = {0} """.format(res))
                    result = cursor.fetchall()
                    print("UID            PID            PQTY")
                    print("________________________")
            
                    for x in result:
                        for y in x:
                            print(y,end=" "*(15-len(str(y))))
                        print("\n")

                else:
                    print("Wrong INPUT")

            elif user_choice == 3:

                status = input("PLACE ORDER?\n1. Yes\n2. No")
                if status:
                    cursor.execute("""UPDATE cart SET status = 1 WHERE uid = {0}""".format(res))

            elif user_choice == 4:
                cursor.execute("""SELECT * FROM cart where uid = {0} """.format(res))
                result = cursor.fetchall()
                print("UID            PID            PQTY")
                print("________________________")
            
                for x in result:
                    for y in x:
                            print(y,end=" "*(15-len(str(y))))
                    print("\n")

            else:
                print("Wrong INPUT")
                
        else:
            print("Wrong UNAME/PSWD")
    
elif login_choice == 3:

    try:
        cursor.execute("""INSERT INTO user VALUES(NULL, ?, ?, ?, ?, ?)""",(input("Enter NAME "), input("Enter UNAME "), input("Enter PASSWORD "), input("Enter E_MAIL "), input("Enter Mobile_NO ")))
        cursor.execute("""SELECT * FROM user""")
        result = cursor.fetchall()
        print("UID            NAME           UNAME          PSWD           EMAIL          MOB")
        print("___________________________________________________________")
        for x in result:
            for y in x:
                print(y,end=" "*(15-len(str(y))))
            print("\n")
    except:
        print("You already have an account with these credentials, Try Signing In")

elif login_choice == 4:
                new_pswd+=1
                f_uname = input("Enter username")
                cursor.execute("""SELECT email FROM user WHERE uname = "{0}" """.format(f_uname))
                f_email = cursor.fetchone()
                f_email = str(''.join(map(str, f_email)))
                print(f_email)

                import smtplib
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("badshahssic@gmail.com","aysbqagxhhjgguqu")
                new_pswd_str = 'Subject: SOTI:New Password\n\n Hi '+str(f_uname)+',\nYour new password is: ' +str(new_pswd)
                server.sendmail("badshahssic@gmail.com",f_email,new_pswd_str)
                server.quit()

                cursor.execute("""UPDATE user SET pswd = {0} WHERE uname = "{1}" """.format(new_pswd, f_uname))

                print("New password has been sent to yr email")

    
else:
    print("Wrong LOGIN CHOICE")

connection.commit()
connection.close()

        
        
