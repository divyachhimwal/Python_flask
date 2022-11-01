from flask import Flask, render_template, request, redirect, session,  url_for
from flask_mysqldb import MySQL
import MySQLdb

from werkzeug.utils import secure_filename
import os


import math, random
from datetime import datetime

import datetime as dt



app = Flask(__name__)
app.secret_key = "123456789"

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'shreemudrakosh'

#db = MySQL(app)

mysql=MySQL(app)

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")
@app.route('/services', methods=['GET', 'POST'])
def services():
    return render_template("services.html")


    


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    
    return render_template("gallery.html")
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")




######..................Admin page......................#####################


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    msg =""

    if request.method == 'POST':
        if 'A_Id' in request.form and 'Pass' in request.form :
            idd = request.form['A_Id']
            pwd = request.form['Pass']
            
   
            

            
            
            cursor = mysql.connection.cursor()

            #cursor.execute("select * From  register where phone ='"+Ph+"' and  password='"+pwd+"' and UserType='"+typ+"'")

            
            cursor.execute("SELECT Admin_id,A_FName,A_LName,Password FROM admin_register WHERE Admin_id= %s AND Password= %s ", (idd,pwd))


            info = cursor.fetchone()

            print(info)
##
##            for inn in info:
##
##              print(inn)
##
##            uid=info[0]
##
##            admin_Nm = info[1] +" "+ info[2]
##            
            

          

            

            if info is not None:

                admin_Nm = info[1] +" "+ info[2]
               
                if info[0]==idd and info[3] == pwd :

                    session['loginsuccess'] = True
                    session['A_Id'] = info[0]
                    session['A_Name'] = admin_Nm

                    return redirect(url_for('admin_show_profile'))
                    
                    #return redirect(url_for('show_profile'))
            else:

                msg = "Incorrect Admin_Id and Password !"

    return render_template("adminn.html",msg=msg)



@app.route('/admin_reg', methods=['GET', 'POST'])
def admin_reg():
    msg =''
    idd = ''
         
    if request.method == "POST":
        if "Fname" in request.form and "Lname" in request.form and "Phone" in request.form and "Pass" in request.form :
            fnm = request.form['Fname']
            lnm = request.form['Lname']
            Ph = request.form['Phone']
            pwd = request.form['Pass']
            


            characters = "0123456789";
            length = len(characters)                   
            lenString = 5;
            randomstring = '';

            
            for i in range(0 , lenString) :
            
                rnum = characters[math.floor(random.random() * length)]
                randomstring += rnum

            ID ="AID55"+ randomstring;

            print(ID)

            session['AID'] = ID





            print("new_user",session.get('AID'))

            

            cur = mysql.connection.cursor()

            #cur.execute("Insert into register values('"+ID+"','"+fnm+"','"+lnm+"','"+ph+"','"+pwd+"','"+typ+"',curdate())")

            cur.execute('SELECT * FROM admin_register WHERE Phone_no = % s ', (Ph, ))

            account = cur.fetchone()

            print(account)

            if account:
                 msg = 'Account already exists !'


            else:
                cur.execute("INSERT INTO admin_register(Admin_id,A_FName,A_LName,Phone_no, Password,Date)VALUES(%s, %s, %s, %s, %s, curdate())", (ID, fnm,lnm,Ph,pwd))

            
                mysql.connection.commit()


                return redirect(url_for('message'))

    return render_template("admin_reg.html" ,msg = msg, idd=idd)

@app.route('/message',methods=['GET', 'POST'])
def message():

    msg=''
    idd = ''

    print("login====",session.get('AID'))

    cur = mysql.connection.cursor()

    cur.execute('Select Admin_id from admin_register where Admin_id = %s', ( session['AID'],))
    opt = cur.fetchone()

    a= opt
    y=str(a).split('(')
    z = y[1]
               
    k=str(z).split(',')
    idd = k[0]

    print(idd)


    msg = 'Your Registeration Id is:'

    return render_template("AIDmsg.html" , msg = msg, idd= idd)


@app.route('/admin_profile',methods=['GET', 'POST'])
def admin_profile():


        if 'loginsuccess' in session:

             cursor=mysql.connection.cursor()

             cursor.execute("SELECT A_FName,A_LName,Phone_no FROM admin_register WHERE Admin_id= %s ", ( session['A_Id'],))

             res = cursor.fetchone()

             A_Nm = res[0] +" "+ res[1]

             A_ph = res[2]

      
        if request.method == "POST":

            nm = request.form['name']
            email = request.form['mail']
            mob = request.form['mobile']
            
            
            

            id_num = request.form['id_card_no']
            id_nm = request.form['id_name']

            
##            #upload Identity Card
##            input = request.form
##            f = request.files['photo']
##            f.save(os.path.join('templates/images', secure_filename(f.filename)))
##            photo_Admin = f.filename

           
            cursor=mysql.connection.cursor()
        
            cursor.execute("INSERT INTO `admin_profile`(`Admin_Id`, `Name`, `Email`, `Phone_no`,`Unique_Id`, `Unique_Id_Number`) VALUES (%s, %s, %s, %s, %s, %s)", (session.get('A_Id'),nm,email,mob,id_nm,id_num))
            #qry="Insert into profile values('"+nm+"','"+dob+"','"+Gen+"','"+mob+"','"+occ+"','"+id_nm+"','"+photo_n+"','"+addr+"','"+pin+"','"+cty+"','"+st+"')";

            mysql.connection.commit()
##
            if 'loginsuccess' in session:

             cursor=mysql.connection.cursor()

             cursor.execute("SELECT * FROM admin_profile WHERE Admin_id= %s ", ( session['A_Id'],))

             opt = cursor.fetchone()

             print(opt)

            
             

####             
             if opt[1] == nm and opt[2] == email and opt[3] == mob and opt[4] == id_nm and opt[5] == id_num :
        
                return redirect(url_for('admin_show_profile'))
            
             else:
                return redirect(url_for('admin_profile'))

       
    
        return render_template("admin_prof.html", A_Nm = A_Nm ,A_ph=A_ph)








@app.route('/admin_show_profile',methods=['GET', 'POST'])
def admin_show_profile():


             cursor=mysql.connection.cursor()

             cursor.execute("SELECT * FROM admin_profile WHERE Admin_id= %s ", ( session['A_Id'],))

             account = cursor.fetchone()

             print(account)

             if account is not None:
                 return render_template("display_admin_prof.html", account = account) 
                 
             else:
                 return redirect(url_for('admin_profile'))
        

             return render_template("display_admin_prof.html", account = account)

           

##@app.route('/Loan',methods=['GET', 'POST'])
##def Loan():
##
##    if request.method == "POST":
##
##            nm = request.form['name']
##            l_amt = request.form['amt']
##            intrst = request.form['intrst']
##            tm = request.form['tm']
##            instll = request.form['instll']
##            dt = request.form['dt']
##            fee = request.form['fee']
##
##            cursor=mysql.connection.cursor()
##
##            cursor.execute("INSERT INTO `loan`(`Name`, `L_Amount`, `Interest`, `Time`, `Installment`, `Issue_Date`, `Processing_Fee`) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nm,l_amt,intrst,tm,instll,dt,fee))
##
##            mysql.connection.commit()
##
##
##    return render_template("Loan.html")








@app.route('/Nominee_info',methods=['GET', 'POST'])
def Nominee_info():

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM `user_profile`")

    ttl = cursor.fetchall()

    for inn in ttl:
        

        U_nm = inn[1] + " "+inn[2]
        

        session['Name']=U_nm

   
        
    


    

    return render_template("Nominee_info.html",ttl = ttl )



@app.route('/nominee/<string:Nm>',methods=['GET', 'POST'])
def nominee(Nm):


##            if 'loginsuccess' in session:
##
##             cursor=mysql.connection.cursor()
##
##             cursor.execute("SELECT * FROM profile WHERE Name= %s ", ( session['Name'],))
##
##             res = cursor.fetchone()
##
##             print(res)
##
##             Nm = res[1]
           
          
            msg =""

            

            if request.method == "POST":

              print('1---if')

              if "name" in request.form and "Fname" in request.form and "Lname" in request.form and "Dob" in request.form and "relation" in request.form and "ph" in request.form and "gen" in request.form and "card" in request.form :  

                 print('2---if')
                 
                 

                 fnm = request.form['Fname']
                 lnm = request.form['Lname']
            
                 dob = request.form['Dob']
                 rel = request.form['relation']
                 PH = request.form['ph']
                 Gen = request.form['gen']

                 id_nm = request.form['card']
                 id_card_no = request.form['card_no']
                 

            
##                 #upload Identity Card
##                 input = request.form
##                 f = request.files['photo']
##                 f.save(os.path.join('templates/images', secure_filename(f.filename)))
##                 photo_n = f.filename

                 print(dob)

                 d = str(dob)
                 a = str(d).split('-')
                 b = a[0]
                 print(b)

                 ag = int(b)

                 current_year = dt.datetime.now().year
                 age = current_year - ag

                 print(age)
                 



                 

                 if (age < 55):
                
                   cursor=mysql.connection.cursor()
                

                   cursor.execute("INSERT INTO `nominee`(`Name`,`FName`,`LName`, `Gender`, `Phone`, `Relation`, `I_card_Nm`, `I_card_No`, `DoB`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(Nm,fnm,lnm,Gen,PH,rel,id_nm,id_card_no,dob))

                   mysql.connection.commit()

                 else:
                     print('not acceptable')

                     msg = 'The age of nominee not acceptable'

                     return render_template('Nominee.html' , msg = msg ,Nm = Nm)

                 return redirect(url_for('Nominee_info'))
                 

            return render_template('Nominee.html' , msg = msg ,Nm = Nm)


@app.route('/show_nominee/<string:Name>',methods=['GET', 'POST'])
def show_nominee(Name):


             cursor=mysql.connection.cursor()

             cursor.execute("SELECT * FROM nominee WHERE Name= %s ", (Name,))

             acc = cursor.fetchone()

             print(acc)

             if acc is not None:
                 
                 return render_template("display_nominee.html", acc = acc) 
                 
             else:
                 return redirect(url_for('nominee' , Nm = Name ))

             return render_template("display_nominee.html", acc = acc)    

############################################################................Loan..........############################

@app.route('/Loann',methods=['GET', 'POST'])
def Loann():

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM `user_profile`")

    ttl = cursor.fetchall()

    for inn in ttl:
        

        U_nm = inn[1] + " "+inn[2]
        

        session['Name']=U_nm

   
        
    


    

    


    return render_template('loan_list.html',ttl = ttl)

    
@app.route('/Loann_info/<string:Name>',methods=['GET', 'POST'])
def Loann_info(Name):

    nm = Name

##    if request.method == "POST":
##
##            nm = request.form['nm']
##            l_amt = request.form['lamt']
##            tm = request.form['tm']
##            dt = request.form['Dt']
##            instll = request.form['Per_Amt']
##            Pay = request.form['pay']
##            fee = request.form['fee']
##            intrst = request.form['ir']
##           
##
##            cursor=mysql.connection.cursor()
##
##            cursor.execute("INSERT INTO `loan`(`Name`, `L_Amount`, `Interest`, `Time`, `Installment`, `Issue_Date`, `Processing_Fee`,`Mode_of_Payment`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(nm,l_amt,intrst,tm,instll,dt,fee,Pay))
##
##            mysql.connection.commit()


    return render_template('loan.html', nm = nm)

    




#####################################################################################################################################################
########################################.........................Deposit..................##########################################################
#####################################################################################################################################################


@app.route('/deposit_typ',methods=['GET', 'POST'])
def deposit_typ():

    return render_template("deposite_typ.html",)


@app.route('/daily_deposit',methods=['GET', 'POST'])
def daily_deposit():

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM `user_profile` WHERE UserType='Daily Deposit'")

    ttl = cursor.fetchall()

    for inn in ttl:
        

        U_nm = inn[1] + " "+inn[2]
        

        session['Name']=U_nm

   
        
    


    

    #return render_template("daily_deposite.html",ttl = ttl )
    return render_template("new_daily_deposit.html",ttl = ttl )

@app.route('/Recurring_deposit',methods=['GET', 'POST'])
def Recurring_deposit():

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM `user_profile` WHERE UserType='Recurring Deposit'")

    ttl = cursor.fetchall()

    for inn in ttl:

        idd = inn[0]

        
        

        U_nm = inn[1] +" "+inn[2]

        print(U_nm)
        

        session['Name']=U_nm

        

   
        
        #return redirect(url_for('R_deposite',Id = idd))


    

    #return render_template("recurring_deposite.html",ttl = ttl )
    return render_template("new_recurring_deposit.html",ttl = ttl )

@app.route('/Fixed_deposit',methods=['GET', 'POST'])
def Fixed_deposit():

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM `user_profile` WHERE UserType='Fixed Deposit'")

    ttl = cursor.fetchall()

    for inn in ttl:
        

        U_nm = inn[1] + " "+inn[2]
        

        session['Name']=U_nm

   
        
    


    

    #return render_template("Fixed_deposite.html",ttl = ttl )
    return render_template("new_fixed_deposit.html",ttl = ttl )
    

#################################################.......Daily Deposit Section..................################################
################################################################################################################################


@app.route('/D_deposit/<string:Acc_no>', methods=["GET", "POST"])
def D_deposit(Acc_no):

    
        msg =""
    

        cursor=mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM User_profile WHERE Account_No= %s",(Acc_no,))

        account = cursor.fetchone()

        
        Nm = account[2]

        typ = account[4]

        

    

        

        if request.method == "POST":

            
            
            if 'Dt' in request.form and 'd1' in request.form and 'amt' in request.form   :


              day = request.form['d1']

              per_day = request.form['per_Amt']
              
              dt = request.form['Dt']
            
              amt = request.form['amt']

              IR = request.form['ir']

              pay_typ = request.form['pay']



               
              ttl_amt = int(day) * int(per_day)  ##########.............for condition....not entered extra installment......########     

                   

              P = int(amt)
              T = int(day)/365
              R = float(IR)

              print(P)
              print(T)
              print(R)





              x = (P*R*T)/100

              print('x=',x)

              i = round(x, 2)

              print('i=',i)
              
              si = str(i)

              print('si=',si)

              amt1= float(amt) + i

              

              print('Amount',amt1)

              print(Acc_no)

              cursor=mysql.connection.cursor()

              cursor.execute("select sum(Deposit_Amount) from daily_deposit where Account_No= %s",(Acc_no,))

              op = cursor.fetchone()

              print(op[0])

              if op[0] == None :


                  cursor=mysql.connection.cursor()

                  cursor.execute("INSERT INTO `daily_deposit`(`Account_No` ,`Name`, `UserType`, `Days`, Per_Day_Amount , `Date`, `Time`,`Deposit_Amount`, `Interest`, `Amount` ,`Mode_of_Payment`) VALUES (%s , %s, %s , %s, %s , %s , curtime(),%s, %s, %s, %s)", (Acc_no,Nm,typ,day,per_day,dt,amt,si,amt1,pay_typ))
                  mysql.connection.commit()

                  



              else:    

              

                 if op[0] == ttl_amt :

                   msg = 'Installment Completed!'

                   return render_template("completeMsg.html" , msg = msg)
              


              
                 else:
              

                  cursor=mysql.connection.cursor()

                  cursor.execute("INSERT INTO `daily_deposit`(`Account_No` ,`Name`, `UserType`, `Days`, Per_Day_Amount , `Date`, `Time`,`Deposit_Amount`, `Interest`, `Amount` ,`Mode_of_Payment`) VALUES (%s , %s, %s , %s, %s , %s , curtime(),%s, %s, %s, %s)", (Acc_no,Nm,typ,day,per_day,dt,amt,si,amt1,pay_typ))
                  mysql.connection.commit()
 
             


        return render_template('Ddeposite.html',Nm = Nm, typ = typ , Acc_no = Acc_no)



#############################################.......................Recurring Deposit Section...............#############################
##########################################################################################################################################

@app.route('/R_deposit/<string:Acc_no>', methods=["GET", "POST"])
def R_deposit(Acc_no):



        msg =""

    

        
        cursor=mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM User_profile WHERE Account_No= %s",(Acc_no,))

        account = cursor.fetchone()

        Acc_no = account[1]
        Nm = account[2]

        typ = account[4]
    

        

        if request.method == "POST":
            
            if 'Dt' in request.form and 'd1' in request.form and 'amt' in request.form :

               


              Month = int(request.form['d1'])                                   

              per_Month = int(request.form['per_Amt'])
              
              dt = request.form['Dt']
            
              amt = float(request.form['amt']) ######################.............Principle per Month

              IR = float(request.form['ir'])  ######################.............Interest Rate

              #N = float(4) ##################......Quaterly
              pay_typ = request.form['pay']
             
              print('$$$$')

              ttl_amt = Month * per_Month

              print(ttl_amt)



              


              

             




              cursor=mysql.connection.cursor()

              cursor.execute("SELECT sum(Deposit_Amount) from recurring_deposit Where Account_No= %s",(Acc_no,))

              acc = cursor.fetchone()

              print(acc[0])

              


              

              

              if acc[0] == None:

                  print('===============')
                  P = int(amt)
                  R = IR
                  T = int(Month)/12
                    

                  print(P)
                  print(T)
                  print(R)

                  x = (P*R*T)/100

                  print('x=',x)

                  i = round(x, 2)

                  print('i=',i)
              
                  si = str(i)

                  print('si=',si)

                  amt1= float(amt) + i

                  print('Amount',amt1)

                  cursor=mysql.connection.cursor()


                  cursor.execute("INSERT INTO `recurring_deposit`(`Account_No`,`Name` ,`UserType`, `Month`, `Per_Month_Amount` , `Date`, `Time`,`Deposit_Amount`,`Interest`, `Amount` , `Mode_of_Payment`) VALUES (%s, %s, %s , %s, %s, %s, curtime(), %s, %s, %s , %s)", (Acc_no,Nm,typ,Month,per_Month,dt,amt,si,amt1,pay_typ)) 

                  #INSERT INTO `recurring_deposit`(`Account_No`, `Name`, `UserType`, `Month`, `Per_Month_Amount`, `Date`, `Time`, `Deposit_Amount`, `Interest`, `Amount`, `Mode_of_Payment`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]','[value-8]','[value-9]','[value-10]','[value-11]')
                    
                  mysql.connection.commit()
                  

              else:

                    print('acc[0] =',acc[0])
                    print('ttl_amt =',ttl_amt)


                    if acc[0] == ttl_amt :

                         msg = 'Installment Completed!'

                         return render_template("completeMsg.html" , msg = msg)


                    else:

                        P = int(amt)
                        R = IR
                        T = int(Month)/12
                    

                        print(P)
                        print(T)
                        print(R)

                        x = (P*R*T)/100

                        print('x=',x)

                        i = round(x, 2)

                        print('i=',i)
              
                        si = str(i)

                        print('si=',si)

                        amt1= float(amt) + i

                        print('Amount',amt1)

                        cursor.execute("INSERT INTO `recurring_deposit`(`Account_No`,`Name` ,`UserType`, `Month`, `Per_Month_Amount` , `Date`, `Time`,`Deposit_Amount`,`Interest`, `Amount` ,`Mode_of_Payment`) VALUES (%s, %s, %s , %s, %s,%s, curtime(), %s, %s, %s , %s)", (Acc_no,Nm,typ,Month,per_Month,dt,amt,si,amt1,pay_typ)) 

                        mysql.connection.commit()
                        


                    
                  


             


        return render_template('Rdeposite.html',Nm = Nm, typ = typ, Acc_no = Acc_no )

######################################...............Fixed_Deposit...........###########################    


@app.route('/F_deposit/<string:Acc_no>', methods=["GET", "POST"])
def F_deposit(Acc_no):


        msg =""
    

        
        cursor=mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM User_profile WHERE Account_No= %s",(Acc_no,))

        account = cursor.fetchone()

        Acc_no = account[1]
        Nm = account[2]

        typ = account[4]
    

        

        if request.method == "POST":
            
            if 'Dt' in request.form and 'd1' in request.form and 'amt' in request.form :

              


              year = int(request.form['d1'])
              
              dt = request.form['Dt']
            
              amt = float(request.form['amt']) ######################.............Principle per Month

              IR = float(request.form['ir'])  ######################.............Interest Rate

              #N = float(4) ##################......Quaterly

              #Month = year*12 ######################..............Time.......#####convert into Months

              pay_typ = request.form['pay']


              

              rate = IR/100

              #print('rate====',rate)

              ############......Formual RD Maturity..........####..... A = P *(1+R/10)^(N = time) 

              RN = (1 + rate)**year

              print("RN====",RN)


              A = amt * RN 
                  

                  


              print('A========',A)

              intrst_rate = A - amt

              print("ir ====",intrst_rate)

              cursor=mysql.connection.cursor()

              cursor.execute("SELECT count(*) from fixed_deposit Where Account_No= %s",(Acc_no,))

              opp = cursor.fetchone()

              print(opp[0])

              if opp[0] == None:

                     cursor.execute("INSERT INTO `fixed_deposit`(`Account_No` ,`Name`, `UserType`, `Year`, `Date`, `Time`,`Deposit_Amount`,`Interest`, `Amount`,`Mode_of_Payment`) VALUES ( %s,  %s , %s , %s, %s, curtime(), %s, %s , %s, %s)", (Acc_no,Nm,typ,year,dt,amt,intrst_rate,A,pay_typ)) 

                     mysql.connection.commit()

              else:

                  if opp[0] == 1 :

                         msg = 'Installment Completed!'

                         return render_template("completeMsg.html" , msg = msg)

                  else:

                      cursor.execute("INSERT INTO `fixed_deposit`(`Account_No` ,`Name`, `UserType`, `Year`, `Date`, `Time`,`Deposit_Amount`,`Interest`, `Amount`,`Mode_of_Payment`) VALUES ( %s,  %s , %s , %s, %s, curtime(), %s, %s , %s, %s)", (Acc_no,Nm,typ,year,dt,amt,intrst_rate,A,pay_typ)) 

                      mysql.connection.commit()

                  

              

                  

             


        return render_template('Fdeposite.html',Nm = Nm, typ = typ ,Acc_no = Acc_no )

    
        

#################################################################################################################
#############################################......Daily_Deposit(Statement).......##############################
#################################################################################################################    

@app.route('/statement/<string:Acc_no>',methods=['GET', 'POST'])
def statement(Acc_no):

    
    
    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM daily_deposit WHERE Account_No =%s ",(Acc_no,))

    acc = cursor.fetchall()

    print(acc)
    

    
    if acc:


     ####################################....Installment.....#####################################################    

        cursor.execute("SELECT count(*) FROM daily_deposit WHERE Account_No=%s ",(Acc_no,))

        instl = cursor.fetchone()

        i = instl

        print(i)
            

        k= str(i).split(',')
        c = k[0]
        print(c)
            

        l= str(c).split("(")
        j = l[1]
        print(j)

        st = j
     ####################################....Sum Amount.....................#######################################

        
        cursor.execute("SELECT sum(Amount) FROM daily_deposit WHERE Account_No=%s ",(Acc_no,))

        Ttl_Amt = cursor.fetchone()

        print(Ttl_Amt)

        i = Ttl_Amt

        print(i)
            

        k= str(i).split(',')
        c = k[0]
        print(c)
            

        l= str(c).split("'")
        j = l[1]
        print('j===',j)

        Amt = j

        cursor.execute("select Account_No, DATE_ADD(date, INTERVAL Days DAY) FROM daily_deposit GROUP BY Account_No having Account_No=%s ",(Acc_no,))

        dt = cursor.fetchone()

        print(dt)
        
        
        

    else:

        return render_template('d_stmsg.html')

    

    

    return render_template('d_st.html', acc = acc , st = st ,Amt = Amt , dt = dt)

@app.route('/statements/<string:Name>',methods=['GET', 'POST'])
def statements(Name):

    

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM daily_deposit WHERE Name= %s ", (Name,))

    acc = cursor.fetchall()

    print(acc)

    if acc:

      ###############....Installment.....##############

      cursor.execute("SELECT count(*) FROM daily_deposit WHERE Name= %s ", (Name,))

      instl = cursor.fetchone()

      i = instl

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("(")
      j = l[1]
      print(j)

      st = j
            ############....Sum Amount.....................############

    
      cursor.execute("SELECT sum(Amount) FROM daily_deposit WHERE Name= %s ", (Name,))

      Ttl_Amt = cursor.fetchone()

      print(Ttl_Amt)
  
      i = Ttl_Amt

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("'")
      j = l[1]
      print('j===',j)

      Amt = j

      cursor.execute("select Account_No, DATE_ADD(date, INTERVAL Days DAY),Name FROM daily_deposit GROUP BY Account_No having Name=%s ",(Name,))

      dt = cursor.fetchone()

      print(dt)

    else:

        return render_template('d_stmsg.html')  

    

    
    return render_template('d_st.html', acc = acc , st = st ,Amt = Amt , dt = dt)
    #return render_template('statement.html', acc = acc , st = st ,Amt = Amt)


#########################################......................recurring_deposite statement..................#####################################
##################################################################################################################################################

    
                
@app.route('/r_statement/<string:Acc_no>',methods=['GET', 'POST'])
def r_statement(Acc_no):

    
    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM recurring_deposit WHERE ACcount_No=%s ",(Acc_no,))

    acc = cursor.fetchall()

    if acc:
   
    
    
            ##########....Installment.....############ 
      cursor.execute("SELECT count(*) FROM recurring_deposit WHERE Account_No=%s ",(Acc_no,))

      instl = cursor.fetchone()

      i = instl

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("(")
      j = l[1]
      print(j)

      st = j
                ###############....Sum Amount.....................############

    
      cursor.execute("SELECT sum(Amount) FROM recurring_deposit WHERE Account_No=%s ",(Acc_no,))

      Ttl_Amt = cursor.fetchone()

      print(Ttl_Amt)

      i = Ttl_Amt

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("'")
      j = l[1]
      print(j)

      Amt = j

      cursor.execute("select Account_No, DATE_ADD(date, INTERVAL Month Month) FROM recurring_deposit GROUP BY Account_No having Account_No=%s ",(Acc_no,))

      dt = cursor.fetchone()

      print(dt)

    else:

        return render_template('r_stmsg.html')  
  

    

    

    #return render_template('statement.html', acc = acc , st = st ,Amt = Amt)
    return render_template('r_st.html', acc = acc , st = st ,Amt = Amt, dt = dt)

@app.route('/r_statements/<string:Name>',methods=['GET', 'POST'])
def r_statements(Name):

    print(Name)

   

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM recurring_deposit WHERE Name= %s ", (Name,))

    acc = cursor.fetchall()

    if acc:

           ###########....Installment.....####################    

      cursor.execute("SELECT count(*) FROM recurring_deposit WHERE Name= %s ", (Name,))

      instl = cursor.fetchone()

      i = instl

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("(")
      j = l[1]
      print(j)

      st = j
           ###############....Sum Amount.....................##############

    
      cursor.execute("SELECT sum(Amount) FROM recurring_deposit WHERE Name= %s ", (Name,))

      Ttl_Amt = cursor.fetchone()

      print(Ttl_Amt)

      i = Ttl_Amt

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("'")
      j = l[1]
      print(j)

      Amt = j

      cursor.execute("select Account_No, DATE_ADD(date, INTERVAL Month Month), Name FROM recurring_deposit GROUP BY Account_No having Name=%s ",(Name,))

      dt = cursor.fetchone()

      print(dt)

    else:

        return render_template('r_stmsg.html')  


    

    

    return render_template('r_st.html', acc = acc , st = st ,Amt = Amt, dt = dt)


#########################################......................fixed_deposite statement..................#########################################
##################################################################################################################################################

@app.route('/f_statement/<string:Acc_no>',methods=['GET', 'POST'])
def f_statement(Acc_no):

   

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM fixed_deposit WHERE Account_No=%s ",(Acc_no,))

    acc = cursor.fetchall()

    if acc:
    
            ##########....Installment.....############ 

      cursor.execute("SELECT count(*) FROM fixed_deposit  WHERE Account_No=%s ",(Acc_no,))

      instl = cursor.fetchone()

      i = instl

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("(")
      j = l[1]
      print(j)

      st = j
                ###############....Sum Amount.....................############

    
      cursor.execute("SELECT sum(Amount) FROM fixed_deposit WHERE Account_No=%s ",(Acc_no,))

      Ttl_Amt = cursor.fetchone()

      print(Ttl_Amt)

      i = Ttl_Amt

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("'")
      j = l[1]
      print(j)

      Amt = j

      cursor.execute("select Account_No, DATE_ADD(date, INTERVAL Year Year) FROM fixed_deposit GROUP BY Account_No having Account_No=%s ",(Acc_no,))

      dt = cursor.fetchone()

      print(dt)

    else:

        return render_template('f_stmsg.html')  


    

    

    return render_template('f_st.html', acc = acc , st = st ,Amt = Amt , dt = dt)

@app.route('/f_statements/<string:Name>',methods=['GET', 'POST'])
def f_statements(Name):

   

    cursor=mysql.connection.cursor()

    cursor.execute("SELECT * FROM fixed_deposit WHERE Name= %s ", (Name,))

    acc = cursor.fetchall()

    if acc:

           ###########....Installment.....####################    

      cursor.execute("SELECT count(*) FROM fixed_deposit WHERE Name= %s ", (Name,))

      instl = cursor.fetchone()
 
      i = instl

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("(")
      j = l[1]
      print(j)

      st = j
           ###############....Sum Amount.....................##############

    
      cursor.execute("SELECT sum(Amount) FROM fixed_deposit WHERE Name= %s ", (Name,))

      Ttl_Amt = cursor.fetchone()

      print(Ttl_Amt)

      i = Ttl_Amt

      print(i)
        

      k= str(i).split(',')
      c = k[0]
      print(c)
        

      l= str(c).split("'")
      j = l[1]
      print(j)

      Amt = j

      cursor.execute("select Account_No, DATE_ADD(date, INTERVAL Year Year) , Name FROM fixed_deposit GROUP BY Account_No having Name =%s ",(Name,))

      dt = cursor.fetchone()

      print(dt)

    else:

        return render_template('f_stmsg.html')  


    

    

    return render_template('f_st.html', acc = acc , st = st ,Amt = Amt , dt = dt)



#####################################################................Reports..................#####################################################



@app.route('/reports',methods=['GET', 'POST'])
def reports():

    return render_template('reports.html') 

    

@app.route('/daily_deposit_report', methods=['GET', 'POST'])
def daily_deposit_report():

    Utyp = 'Daily Deposit'

    session['typ']= Utyp

    return render_template('Dd_report.html')


@app.route('/recurring_deposit_report', methods=['GET', 'POST'])
def recurring_deposit_report():

    Utyp = 'Recurring Deposit'

    session['typ']= Utyp

    return render_template('Rd_report.html')


@app.route('/fixed_deposit_report', methods=['GET', 'POST'])
def fixed_deposit_report():

    Utyp = 'Fixed Deposit'

    session['typ']= Utyp

    return render_template('Fd_report.html')


@app.route('/dd_complete', methods=['GET', 'POST'])
def dd_complete():

     cursor=mysql.connection.cursor()

     #cursor.execute("select Account_No,  Name,Days,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM daily_deposit GROUP BY Account_No having count(Account_No) = Days")

     cursor.execute("select Account_No,  Name,Days,Per_Day_Amount,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM daily_deposit GROUP BY Account_No having sum(Deposit_Amount) = Days * Per_Day_Amount")

     acc = cursor.fetchall()

     print(acc)

     

    

     #return render_template('Dd_complete_report.html',acc=acc)
     return render_template('new_dd_report.html',acc=acc)

@app.route('/dd_ongoing', methods=['GET', 'POST'])
def dd_ongoing():

     cursor=mysql.connection.cursor()

     #cursor.execute("select Account_No, Name,Days,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM daily_deposit GROUP BY Account_No having count(Account_No) <> Days")
     cursor.execute("select Account_No,  Name,Days,Per_Day_Amount,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM daily_deposit GROUP BY Account_No having sum(Deposit_Amount) <> Days * Per_Day_Amount")

     acc = cursor.fetchall()

     print(acc)

     

    


     #return render_template('Dd_complete_report.html',acc=acc)
     return render_template('new_dd_report.html',acc=acc)
    


@app.route('/Rd_complete', methods=['GET', 'POST'])
def Rd_complete():

     cursor=mysql.connection.cursor()

     #cursor.execute("select Account_No, Name,Month,count(ID),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM recurring_deposit GROUP BY ID having count(ID) = Month")

     cursor.execute("select Account_No,  Name,Month,Per_Month_Amount,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM recurring_deposit GROUP BY Account_No having sum(Deposit_Amount) = Month * Per_Month_Amount")

     acc = cursor.fetchall()

     print(acc)

     

    

     return render_template('new_rd_report.html',acc=acc)

@app.route('/Rd_ongoing', methods=['GET', 'POST'])
def Rd_ongoing():

     cursor=mysql.connection.cursor()

     #cursor.execute("select Account_No, Name,Month,count(ID),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM recurring_deposit GROUP BY ID having count(ID) <> Month")

     cursor.execute("select Account_No,  Name,Month,Per_Month_Amount,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount) FROM recurring_deposit GROUP BY Account_No having sum(Deposit_Amount) <> Month * Per_Month_Amount")
    
     acc = cursor.fetchall()

     print(acc)

     

    

     return render_template('new_rd_report.html',acc=acc)
    
        

@app.route('/Fd_complete', methods=['GET', 'POST'])
def Fd_complete():

     cursor=mysql.connection.cursor()

     cursor.execute("select Account_No, Name,Year,count(Account_No),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount),DATE_ADD(Date,Interval 1*Year year) As datee FROM Fixed_deposit GROUP BY Account_No having datee  < CURRENT_DATE")

     acc = cursor.fetchall()

     print(acc)

     

    

     # return render_template('Fd_complete_report.html',acc=acc)
     return render_template('new_fd_report.html',acc=acc)

@app.route('/Fd_ongoing', methods=['GET', 'POST'])
def Fd_ongoing():

     cursor=mysql.connection.cursor()

     cursor.execute("select Account_No, Name,Year,count(Account_NO),SUM(Deposit_Amount),SUM(Round(interest,2)),SUM(Amount),DATE_ADD(Date,Interval 1*Year year) As datee FROM Fixed_deposit GROUP BY Account_No having datee  > CURRENT_DATE")

     acc = cursor.fetchall()

     print(acc)

     

    

     #return render_template('Fd_complete_report.html',acc=acc)
     return render_template('new_fd_report.html',acc=acc)
    
        





########################################...................Admin Page.............................#####################################################



#########################################################################################################################################################################################


########################################################................USER Page.......................######################################################



################################################......Login Page....###################################



@app.route('/Login', methods=['GET', 'POST'])
def Login():



    msg=''

    

    
    if request.method == 'POST':
        if 'R_Id' in request.form :
            CIF = request.form['R_Id']
        
         
   
            

            
            
            cursor = mysql.connection.cursor()

            #cursor.execute("select * From  register where phone ='"+Ph+"' and  password='"+pwd+"' and UserType='"+typ+"'")

            
            cursor.execute("SELECT ID,FName,LName,Phone FROM register WHERE ID= %s", (CIF,))

            
            


            info = cursor.fetchone()
##            for inn in info:
##                print(inn)
##                print(info)
##            uid=info[0]
##
##            Nm = info[1] +" "+ info[2]
##            print(Nm)
            
            print(info)
        
            

          

            

            if info is not None:
                Nm = info[1] +" "+ info[2]
                print(Nm)
               
                if info[0]== CIF  :

                    session['loginsuccess'] = True
                    session['CIF'] = info[0]
                    
                    session['Name'] = Nm
                    
                    return redirect(url_for('select_acc'))
            else:

                
                msg = 'Incorrect CIF Number'

                
                #return redirect(url_for('index'))

    return render_template("log.html",msg = msg)


###########################################################################....................Registration.............##########################################




    
@app.route('/new_user',methods=['GET', 'POST'])
def new_user():

    msg =''
    
    
    if request.method == "POST":
        if "Fname" in request.form and "Lname" in request.form and "Phone" in request.form  :
            fnm = request.form['Fname']
            lnm = request.form['Lname']
            Ph = request.form['Phone']
            
            


            characters = "0123456789";
                    
            length = len(characters)                   
            lenString = 4;
            randomstring = '';

    
            for i in range(0 , lenString) :
    
                rnum = characters[math.floor(random.random() * length)]
                randomstring += rnum

            ID ="CIF55"+ randomstring;

            

            print(ID)

            session['CIF'] = ID


##            now = datetime.now()
##
##            br ="1001"
##
##            date_time = now.strftime("%m%d%Y")
##
##            dd = date_time+br
##
##        	
##
##            ID = ""
##            length = len(dd)
##  
##            for i in range(6):
##              ID+= dd[math.floor(random.random() * length)]


            print("new_user",session.get('CIF'))

            cur = mysql.connection.cursor()

            #cur.execute("Insert into register values('"+ID+"','"+fnm+"','"+lnm+"','"+ph+"','"+pwd+"','"+typ+"',curdate())")

            cur.execute('SELECT * FROM register WHERE Phone = % s', (Ph,))

            account = cur.fetchone()

            print(account)

            if account:
                 msg = 'Account already exists !'


            else:

               
               print("####",ID) 

               cur.execute("INSERT INTO register(ID,FName,LName,Phone, Date)VALUES(%s, %s, %s, %s,  curdate())", (ID, fnm,lnm,Ph))
               
              
               mysql.connection.commit()


               
               return redirect(url_for('msg'))
         

               
               #msg = 'Your Registeration Id is:'
            
    return render_template("login.html" , msg = msg)






@app.route('/msg',methods=['GET', 'POST'])
def msg():

    msg=''
    idd = ''

    print("login====",session.get('CIF'))

    cur = mysql.connection.cursor()

    cur.execute('Select ID from register where ID = %s', ( session['CIF'],))
    opt = cur.fetchone()

    a= opt
    y=str(a).split('(')
    z = y[1]
               
    k=str(z).split(',')
    idd = k[0]

    print(idd)


    msg = 'Your Registeration Id is:'

    return render_template("IDmsg.html" , msg = msg, idd= idd)

#####################################################################........................Select Account.....................################################


@app.route('/select_acc',methods=['GET', 'POST'])
def select_acc():


   Idd = session['CIF']

   Nm = session['Name']
   print('Hhello')

   if request.method == "POST":

       print('hello')

       acc_typ = request.form['Acc_type']


       session['Acc_typ'] = acc_typ

       print("............",session.get('Acc_typ'))

       return redirect(url_for('show_profile'))
       
       
   return render_template("select_Acc.html",Idd = Idd ,Nm = Nm)











##################################################.....................Profile Page..............###############################################


@app.route('/profile',methods=['GET', 'POST'])
def profile():


    
         if 'loginsuccess' in session:

             cursor=mysql.connection.cursor()

             cursor.execute("SELECT FName,LName,Phone FROM register WHERE ID= %s ", ( session['CIF'],))

             account = cursor.fetchone()

             Nm = account[0] +" "+ account[1]

             ph = account[2]

             Atyp = session['Acc_typ']

##             #session['Phone']= ph
##
##             #print(session.get('Phone'))
##             #print( session.get('R_Id'))
##             
##
##             
##             
##
##
##        
         if request.method == "POST":

            nm = request.form['name']
            mob = request.form['mobile']
            
            dob = request.form['Dob']
            
            Gen = request.form['gen']
            occ = request.form['occ']
            
            addr = request.form['add']
            pin = request.form['pin']
            cty = request.form['city']
            st = request.form['state']

            id_nm = request.form['card']
            i_card_no=request.form['cardno'] 

            
##            #upload Identity Card
##            input = request.form
##            f = request.files['photo']
##            f.save(os.path.join('templates/images', secure_filename(f.filename)))
##            photo_n = f.filename



            cur = mysql.connection.cursor()

          


            Number="0001"


##            characters = "0123456789";
##                    
##            length = len(characters)                   
##            lenString = 4;
##            randomstring = '';
##
##    
##            for i in range(0 , lenString) :
##    
##                rnum = characters[math.floor(random.random() * length)]
##                randomstring += rnum


            if Atyp == 'Daily Deposit':

                   cur.execute("SELECT count(*) FROM User_Profile WHERE UserType="'"Daily Deposit"'"")

                   res = cur.fetchone()

                   print(res)

                   if res[0] == 0:

                        Acc_no ="CHINDD1"+ Number;

                        print(Acc_no)

                   else:

                       print("hello")
                       cur.execute('SELECT Account_No FROM User_Profile  WHERE UserType= %s Order BY Account_No DESC LIMIT 1',(Atyp,))

                       res1 = cur.fetchone()
                       print(res1)

                       print(res1[0])
 
                       idd = res1[0]

                       i = str(idd).split('D')

                       print(i)
                       
                       iid = (i[2])

                       print(iid)

                       IDD = int(iid)

                      

                       Num= IDD + 1

                       print(Num)

                       No = str(Num)

                       Acc_no ="CHINDD"+ No;

                       print(Acc_no)

                       

            elif Atyp == 'Recurring Deposit':

                   cur.execute("SELECT count(*) FROM User_Profile WHERE UserType="'"Recurring Deposit"'"")

                   res = cur.fetchone()

                   print(res)

                   if res[0] == 0:

                        Acc_no ="CHINRD2"+ Number;

                        print(Acc_no)

                   else:

                       print("hello")
                       cur.execute('SELECT Account_No FROM User_Profile  WHERE UserType= %s Order BY Account_No DESC LIMIT 1',(Atyp,))

                       res1 = cur.fetchone()
                       print(res1)

                       print(res1[0])
 
                       idd = res1[0]

                       i = str(idd).split('D')

                       print(i)
                       
                       iid = (i[1])

                       print(iid)

                       IDD = int(iid)

                      

                       Num= IDD + 1

                       print(Num)

                       No = str(Num)

                       Acc_no ="CHINRD"+ No;

                       print(Acc_no)
                       
            elif Atyp == 'Fixed Deposit':

                   cur.execute("SELECT count(*) FROM User_Profile WHERE UserType="'"Fixed Deposit"'"")

                   res = cur.fetchone()

                   print(res)

                   if res[0] == 0:

                        Acc_no ="CHINFD3"+ Number;

                        print(Acc_no)

                   else:

                       print("hello")
                       cur.execute('SELECT Account_No FROM User_Profile  WHERE UserType= %s Order BY Account_No DESC LIMIT 1',(Atyp,))

                       res1 = cur.fetchone()
                       print(res1)

                       print(res1[0])
 
                       idd = res1[0]

                       i = str(idd).split('D')

                       print(i)
                       
                       iid = (i[1])

                       print(iid)

                       IDD = int(iid)

                      

                       Num= IDD + 1

                       print(Num)

                       No = str(Num)

                       Acc_no ="CHINFD"+ No;

                       print(Acc_no)

           
                   
    

                

            session['Acc_No'] = Acc_no

            print(session.get('Acc_No'))

           
            cursor=mysql.connection.cursor()
        
            cursor.execute("INSERT INTO `user_profile`(`ID`,`Account_No`,`Name`, `DoB`,`UserType` ,`Gender`, `Phone`, `Occupation`, `I_card_Nm`, `I_card_No`, `Address`, `Pincode`, `City`, `State`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,% s)", (session.get('CIF'),Acc_no,nm,dob,Atyp,Gen,mob,occ,id_nm,i_card_no,addr,pin,cty,st))
            #qry="Insert into profile values('"+nm+"','"+dob+"','"+Gen+"','"+mob+"','"+occ+"','"+id_nm+"','"+photo_n+"','"+addr+"','"+pin+"','"+cty+"','"+st+"')";

            mysql.connection.commit()
##
            if 'loginsuccess' in session:

             cursor=mysql.connection.cursor()

             cursor.execute("SELECT * FROM user_profile WHERE Account_No = %s", (session['Acc_No'],))

             detail = cursor.fetchone()

             print(detail)

            
             print('----',detail[0])
             print('----',detail[1])
             print('----',detail[2])
             print('----',detail[3])
             print('----',detail[4])
             print('----',detail[5])
             print('----',detail[6])
             print('----',detail[7])
             print('----',detail[8])
             print('----',detail[9])
             print('----',detail[10])
             print('----',detail[11])
             print('----',detail[12])
             print('----',detail[13])

####             
             if detail[2] == nm and detail[5] == Gen and detail[7] == occ and detail[8] == id_nm and detail[9] == i_card_no and detail[10] == addr and detail[11] == pin and detail[12] == cty and detail[13] == st:
                    session['loginsuccess'] = True
                    session['Name'] = detail[2]
                    print('Hello')
                    
                    
                    return redirect(url_for('show_profile'))
             else:
                return redirect(url_for('profile'))

       
    
         return render_template("poffff.html", Nm = Nm ,ph=ph ,Atyp = Atyp)




#######################################......................Show Profile.........................################################################



@app.route('/show_profile',methods=['GET', 'POST'])
def show_profile():

    #if 'loginsuccess' in session:

             print(session.get('Acc_typ'))

             print(session.get('CIF'))

             cursor=mysql.connection.cursor()

             cursor.execute("SELECT * FROM user_profile WHERE ID= %s AND UserType =%s ", ( session['CIF'],session['Acc_typ'],))

             account = cursor.fetchone()

             print(account)

             if account is not None:
                 #return render_template("display_profile.html", account = account)
                 return render_template("new_display_profile.html", account = account) 
                 
             else:
                 return redirect(url_for('profile'))
        

             #return render_template("display_profile.html", account = account)
             return render_template("new_display_profile.html", account = account) 
    



#######################################.......................Update Profile...............###############################################



@app.route('/edit_profile',methods=['GET', 'POST'])
def edit_profile():

             cursor=mysql.connection.cursor()

             cursor.execute("SELECT * FROM user_profile WHERE UserType= %s ", ( session['Acc_typ'],))

             account = cursor.fetchone()

             Acc_no = account[1]

             Nm = account[2]

             dob = account[3]

             Acc_typ = account[4]

             Gen = account[5]

             mob = account[6]

             Id_nm = account[8]

             Id_card = account[9]

             if request.method == "POST":

                 
                 occ = request.form['occ']
            
                 addr = request.form['add']
                 pin = request.form['pin']
                 cty = request.form['city']
                 st = request.form['state']

                 cursor=mysql.connection.cursor()

                 cursor.execute("UPDATE user_profile SET Phone = %s , Occupation = %s , Address = %s, Pincode = %s, City = %s, State = %s WHERE Account_No = %s ", (mob,occ,addr,pin,cty,st, session['Acc_No'],))

                 mysql.connection.commit()
                 
                 updt = cursor.fetchone()

                 print(updt)

                 return redirect(url_for('show_profile'))

             return render_template("edit_profile.html", Nm = Nm , dob = dob, Gen = Gen, Id_nm = Id_nm, Id_card = Id_card)
             #return render_template("new_edit_profile.html", Acc_no = Acc_no ,Nm = Nm , dob = dob, Acc_typ = Acc_typ  , Gen = Gen, mob = mob ,Id_nm = Id_nm, Id_card = Id_card)
             

@app.route('/logout',methods=['GET', 'POST'])
def logout():

    session.pop('A_Id',None)
    session.pop('A_Name',None)

    return redirect(url_for('admin'))


if __name__ == '__app__':
    app.run(debug=True)

