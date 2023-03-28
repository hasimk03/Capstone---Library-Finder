import time as t
from getpass import getpass
from mysql.connector import connect, Error
from dateutil.parser  import parse
import upload_to_azure as azure

def read_raw_data(connection):
    start = t.time()
    i,count,prev,azure_output,stack = 0,0,-1,'',[]
    data_entries=0
    open('azure_data.txt', 'w').close()                                             #open and delete azure_data.txt file
    with open('data1.txt','r') as f:
        while True:
            data = f.readline()                                             #read data from text file
            write=False
            try:
                data_num, npc_count,date,time = data.split(" | ")           #split data by delimitter
                time = time[0:8]
            except ValueError as e:
                print("Could not locate data. Sleeping for 5 seconds...")
                t.sleep(5)
                try:
                    data = f.readline()
                    index+=1
                    data_num, npc_count,date,time = data.split(" | ")           #split data by delimitter
                except:
                    print("No more data available. Check hardware is still functional")
                    return

            print("READING..."+data_num)                      
            npc_count = npc_count[4:]
            if i==0: 
                stack.append(int(npc_count))
                print("Querying database with first value:\n  people={0}\n  date={1}\n  time={2}".format(npc_count,date,time))
                query_db(connection,npc_count,date,time)                         #query_db
                azure_output = "data-{0}|{1}|{2}|{3}|".format(count,str(npc_count),date,time)+"\n"          #azure output text
                write=True
                t.sleep(3); 
            elif len(stack)>0 and stack[-1] != int(npc_count):                   #new incoming data val
                prev = stack[-1]
                stack.append(int(npc_count))     
                count=0                                
            elif len(stack)>0 and prev > int(npc_count) and count==70:                      #incr num ppl and query db
                print("Querying database with:\n  people={0}\n  date={1}\n  time={2}".format(npc_count,date,time))
                query_db(connection,npc_count,date,time)   
                azure_output = "data-{0}|{1}|{2}|{3}|".format(count,str(npc_count),date,time)+"\n"          #azure output text
                write=True
                t.sleep(3); 
            elif len(stack)>0 and prev < int(npc_count) and count==7:                     #dec num ppl and query db
                print("Querying database with:\n  people={0}\n  date={1}\n  time={2}".format(npc_count,date,time))
                query_db(connection,npc_count,date,time)            
                azure_output = "data-{0}|{1}|{2}|{3}|".format(count,str(npc_count),date,time)+"\n"          #azure output text
                write=True
                t.sleep(3); 

            if len(stack)>0 and stack[-1] == int(npc_count):                   #same value
                count+=1
            print("count={0} | npc_count={1} | stack.pop()={2}".format(count,npc_count,stack[-1]))
            pop = stack[-1]                                                      #top of stack
            i+=1

            elapsed_time = t.time() - start
            if (write==True and elapsed_time >=30) or (count==1):               #pushed to stack and 30s passed or 1st iteration
                upload_blob_to_azure(azure_output,count,data_entries)           #push data to output text file and/or container
            t.sleep(0.45)

#write data to azure output file and upload to containers
def upload_blob_to_azure(azure_output,count,data_entries):
    print("Writing data {0} to Azure Blob Storage".format(count))
    azure_file = open('azure_data.txt','a')
    start = t.time()                                                            #update start time
    azure_file.write(azure_output)
    azure_file.close()
    data_entries+=1                                                             #data values stored in output file
    if data_entries > 5:                            
        print(f'Found 5 data entries...Uploading to Azure')
        t.sleep(1)
        data_entries=0
        azure.main()                                                           #connect and upload to azure containers
        t.sleep(1)

def connect_to_mySQL_server():
    try:
        connection = connect(                                                       #connect to sql-server localhost
                            host="localhost",
                            #user=input("Enter username: "),
                            #password=getpass("Enter password: "),
                            user='root',
                            password='password',
                            auth_plugin='mysql_native_password')
    except Error as e:
        print("Error while connecting to MySQL", e)
        return
    return connection

#query database stored in connection
def query_db(connection,npc_count=0,raw_date='',time='',push=True):
    if raw_date != '':
        date = parse(raw_date).strftime('%Y-%m-%d'); datetime = date+" "+time
    else:
        datetime=date=''

    #upload one entry
    push_data = '''USE locations; 
                    INSERT INTO test_room 
                    VALUE ({0},'{1}','{2}','{3}');'''.format(npc_count,datetime,date,time)
    pull_data = '''                                                             
        USE locations; 
        SELECT * FROM test_room;'''


    script = push_data if push else pull_data
    if connection.is_connected():                                               #connecton established
        with connection.cursor() as cursor:                                     #enter queries
            for statement in script.split(';'):
                if len(statement) > 0 and push:                                 #query db (push)
                    try:
                        cursor.execute(statement + ';')
                        connection.commit()
                    except Error as e:
                        print("Error ",e," occured when attempting to insert into table")
                if len(statement)>0 and not push:                             #pull from db
                    try:
                        cursor.execute(statement + ';')
                        for db in cursor:
                            for person in db:
                                print(person)
                    except Error as e:
                        print("Error ",e, "occured when attempting to pull from table")
            cursor.close()

    else:
        return "No existing connections found"
    

#close existing connection
def close_mySQL(connection):                                                
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")


def main():
    print("\nStart")
    connection = connect_to_mySQL_server()
    try:
        read_raw_data(connection)
    except Error as e:
        print("The following error occured: ",e)
    finally:
        print(f'Saving data to container')
        azure.main()
        print("closing connection")
        close_mySQL(connection)


if __name__ == "__main__":
    main()
