#this method is for interaction with the user and record its responses
def takeuserdata(mycursor):
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
