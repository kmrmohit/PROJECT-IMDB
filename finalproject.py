import requests
from bs4 import BeautifulSoup
import os, sys
from datetime import datetime
import mysql.connector
import smtplib
import config

#a mysql database could be created using a python script or manually in the mysql editor
#connection to an existing mysql database is made
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Km19982016",
    port="8081",
    database="testdb"
)

mycursor = mydb.cursor()

#scraping links
sublinks = ["/list/ls021409819/","/list/ls051600015/?st_dt=&mode=detail&sort=release_date,desc&page=1","/search/title?languages=hi&title_type=tv_series&page=1&sort=release_date,desc&view=advanced&ref_=adv_nxt"]
baselink = "https://www.imdb.com"


mp={"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"july":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}


#this function sends the mail with subject 'subject' , message 'msg' to the user = 'receiever'
def send_email(subject,msg,reciever):
    try:
        print(reciever)
        print(msg)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAILADDRESS,config.PASSWORD)
        message = 'Subject:{}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAILADDRESS,reciever,message)
        server.quit()
    except:
        print("FAILED")


#this method inserts data into the mysql database
#data is a tuple that has two values in it.First is the user_id and second is the name of the tvseries liked by the user
#any insertion and deletion takes place through explicit call through mysql commands
def insert_to_db(data):
    sqlformulains = "INSERT INTO appusers (user_id,tvseries) VALUES (%s,%s)"
    mycursor.execute(sqlformulains,data)
    mydb.commit()
    return

#below two methods deletes data from the database in case the user wants to update its preferences or withdraw from the service
def delete_from_db(uid):
    sqlformuladel ="DELETE FROM appusers WHERE user_id = "
    sqlformuladel += '"'
    sqlformuladel += uid
    sqlformuladel += '"'
    mycursor.execute(sqlformuladel)
    sqlformuladel ="DELETE FROM linker WHERE user_id = "
    sqlformuladel += '"'
    sqlformuladel += uid
    sqlformuladel += '"'
    mycursor.execute(sqlformuladel)
    mydb.commit()
    return

def delete_from_appusers(uid,seriesname):
    sqlformuladel ="DELETE FROM appusers WHERE user_id = "
    sqlformuladel += '"'
    sqlformuladel += uid
    sqlformuladel += '"'
    sqlformuladel += 'and '
    sqlformuladel += 'tvseries = '
    sqlformuladel += '"'
    sqlformuladel += seriesname
    sqlformuladel += '"'
    mycursor.execute(sqlformuladel)
    mydb.commit()

#this method is for getting the count of row or the number of users in the database
def get_rows():
    mycursor.execute("SELECT * FROM linker")
    ans = mycursor.fetchall()
    n = len(ans)
    return n

#this method is for interaction with the user and record its responses
def takeuserdata():
    print("Are you a new user?y/n")
    c = input()
    if(c=='y'):
        print("Enter your email-id:")
        mailid = input()
        print("Enter your preferences:")
        likes = input().strip()
        likes = likes.split(",")
        count = get_rows()
        count+=1
        sqlformulains = "INSERT INTO linker (user_id,email) VALUES (%s,%s)"
        data=list()
        data.insert(0,count)
        data.insert(1,mailid)
        mycursor.execute(sqlformulains,data)
        mydb.commit()
        for item in likes:
            val=list()
            val.insert(0,count)
            val.insert(1,str(item))
            val=tuple(val)
            insert_to_db(val)
    else:
        print("Do you want to update your preferences?y/n")
        print("Enter your email-id:")
        mailid = input()        
        print("Below are your current likes:")
        query='SELECT * FROM linker WHERE email = '
        query+='"'
        query+=str(mailid)
        query+='"'
        #print(query)
        mycursor.execute(query)
        thisid = mycursor.fetchone()
        thisid = thisid[0]
        query="SELECT tvseries FROM appusers WHERE user_id = "
        query+=str(thisid)
        mycursor.execute(query)
        thislist = mycursor.fetchall()
        for item in thislist:
            print(item[0])
        print("Do you want to delete some items?y/n")
        c=input()
        if(c=='y'):
            print("Enter the TV Series name from your list:")
            name=input()
            delete_from_appusers(thisid,name)
        else:
            print("Do you want to add some items?y/n")
            c=input()
            if(c=='y'):
                print("Enter the TV Series name:")
                name=input()
                val=list()
                val.insert(0,thisid)
                val.insert(1,str(name))
                val=tuple(val)
                insert_to_db(val)
            else:
                return
    return


#this method calculates the numeric order of a month between 1 to 12, given the input in string data type
def getmon(month):
    month = month.lower()
    month = month.replace(".","")
    num = mp[month]
    return num

#this method is responsible for web scraping and finding the imdb link for the tvseries which we are searching for
def getserieslink(baselink,s,seriesname):
    serieslink=""
    while 1==1 :
        #print(baselink+s)
        r = requests.get(baselink+s)
        c=r.content
        soup = BeautifulSoup(c,"html.parser")
        try:
            nextall = soup.find_all("div",{"class":"lister-item mode-detail"})
            for item in nextall:
                next1 = item.find_all("h3",{"class":"lister-item-header"})[0]
                temp=next1.find("a").text
                #print(temp.lower())
                #print(temp.lower())
                if(temp.lower() == seriesname.lower()):
                    href = next1.find_all("a")[0]
                    href = href["href"]
                    serieslink=href
            if(len(serieslink)>0):
                break
            else:
                
                    nextpage = soup.find("div",{"class":"list-pagination"})
                    #print(nextpage)
                    nextpage = nextpage.find_all("a")[1]
                    #print(nextpage["href"])
                    if(nextpage["href"] != "#"):
                        s=nextpage["href"]
                    else:
                        break
               
                    
        except:
            nextall = soup.find_all("div",{"class":"lister-item mode-advanced"})
            for item in nextall:
                next1 = item.find_all("h3",{"class":"lister-item-header"})[0]
                temp=next1.find("a").text
                #print(temp.lower())
                #print(temp.lower())
                if(temp.lower() == seriesname.lower()):
                    href = next1.find_all("a")[0]
                    href = href["href"]
                    serieslink=href
                    break
            if(len(serieslink)>0):
                break
            else:
                nextpage = soup.find("div",{"class":"nav"})
                #print(nextpage)
                try:
                    nextpage = nextpage.find_all("a")
                    temp=nextpage[0]
                    if(temp.text.lower()=="next"):
                        s=temp["href"]
                        break
                    else:
                        temp=nextpage[1]
                        if(temp.text.lower()=="next"):
                            s=temp["href"]
                            break
                        else:
                            temp=nextpage[2]
                            if(temp.text.lower()=="next"):
                                s=temp["href"]
                                break
                            else:
                                break
                    s="/search/title"+s
                except:
                    break
    return serieslink


#the link provided by the above function is further scraped to find the details about that tv series
def getseriesdetails(link):
    details=""
    r = requests.get(link)
    c=r.content
    soup = BeautifulSoup(c,"html.parser")
    nextall = soup.find("div",{"class":"seasons-and-year-nav"})
    #print(nextall)
    nextall = nextall.find_all("a")
    for item in nextall:
        try:
            a = int(item.text)
            if (a>1000) :
                currentYear = datetime.now().year
                #print(currentYear)
                #print(a)
                if currentYear < a :
                    details="The next season begins in "
                    details+=str(a)
                    details+="."
                elif currentYear > a :
                    details="The show has finished streaming all its episodes.We will keep you updated!"
                else:
                    temp=nextall[0]
                    seasonlink = temp["href"]
                    #print(baselink+seasonlink)
                    rr = requests.get(baselink+seasonlink)
                    cc=rr.content
                    soupp = BeautifulSoup(cc,"html.parser")
                    nextalll = soupp.find_all("div",{"class":"airdate"})
                    #print(nextalll)
                    #print(len(nextalll[-1].text))
                    #print(nextalll[-2].text)
                    latestmon=datetime.now().month
                    latestday=datetime.now().day
                    for each in nextalll:
                        airtime = each.text.split()
                        try:
                            airtime[1]=getmon(airtime[1])
                            airtime[0]=int(airtime[0])
                            #print(airtime)
                            #print(datetime.now().month)
                            #print(datetime.now().day)
                            #print(airtime[1]==datetime.now().month)
                            #print(airtime[0]>=datetime.now().day)
                            if(airtime[1]==datetime.now().month):
                                if(airtime[0]>=datetime.now().day):
                                    latestday=airtime[0]
                                    latestmon=airtime[1]
                                    break
                                else:
                                    latestday=airtime[0]
                            elif(airtime[1]>datetime.now().month):
                                latestday=airtime[0]
                                latestmon=airtime[1]
                                break
                            else:
                                latestday=airtime[0]
                                latestmon=airtime[1]
                        except:
                            pass
                    try:
                        tempmon=latestmon
                        tempday=latestday
                        if latestmon in range(1,10):
                            latestmon = "0"+str(latestmon)
                        if latestday in range(1,10):
                            latestday = "0"+str(latestday)                        
                        ans=str(currentYear)+"-"+str(latestmon)+"-"+str(latestday)
                        if(tempmon<datetime.now().month or (tempmon==datetime.now().month and tempday<datetime.now().day)):
                            details="The show has finished streaming all its episodes.The last episode was aired on ";
                            details+=ans;
                        else:
                            details="Next episode airs on "+ans
                    except:
                        details="No Details Available"
        
                break
            else:
                pass
        except:
            pass
    return details
    

takeuserdata()
mycursor.execute("SELECT * FROM linker")
ans = mycursor.fetchall()
mycursor.execute("SELECT * FROM appusers")
allusers = mycursor.fetchall()
for item in ans:
    userid = item[0]
    message=""
    for users in allusers:
        if users[0]==userid:
            seriesname=users[1]
            temp=""
            for links in sublinks:
                serieslink = getserieslink(baselink,links,seriesname)
                #print(serieslink)
                if(len(serieslink)>0):
                    serieslink = baselink+serieslink
                    seriesdetails = getseriesdetails(serieslink)
                    temp=seriesdetails
                    break
            if(len(temp)==0):
                message+="TV Series: " + seriesname.upper() +"\n" + "Status: "
                temp="No Details Available"
                message+=temp
            else:
                message+="TV Series: " + seriesname.upper() +"\n" + "Status: "
                message+=temp
            message+="\n\n"
    
    subject="YOUR FAVOURITE SHOWS'S CURRENT STATUS"
    msg = message
    send_email(subject,msg,item[1])

mycursor.close()
mydb.close()
