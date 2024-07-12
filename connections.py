import psycopg2
from psycopg2 import extras
import json
from datetime import datetime , date
import os
import datetime 
database_connection = psycopg2.connect(
  database= "medray",
  host= "localhost",
  user= "postgres",
  port=5432,
  password= 1782003
)

cursor = database_connection.cursor(cursor_factory=extras.DictCursor)

cursor2 = database_connection.cursor(cursor_factory=extras.DictCursor)
cursor3 = database_connection.cursor(cursor_factory=extras.DictCursor)
cursor4 = database_connection.cursor(cursor_factory=extras.DictCursor)
cursor5 = database_connection.cursor(cursor_factory=extras.DictCursor)
cursor6 = database_connection.cursor(cursor_factory=extras.DictCursor)

# ////////////////////////////////////////////////
# the login page >> is employee or patient 

# if is employee return job tilte if not return False
def select_employee(data):
            try:
                cursor.execute('''
                select job_title from employee where employee_id = %s  and password =%s
            ''',(data.get('id'),data.get('password')))
                out=cursor.fetchone()
                if out is not None:
                    return out[0]
                else :
                    return False
            
            except Exception as e:
                    print(f"An error occurred: {e}")
        





# if patient return string patient if not return False
def select_patient(data):
    try:     
        cursor.execute('''
        select * from patient where patient_ssn = %s  and password =%s
    ''',(data.get('id'),data.get('password')))
        out=cursor.fetchone()
        if out is not None:
            return f'patient'
        
        else :
           return False
        
    except Exception as e:
          print(f"An error occurred: {e}")

# based on the above 2 function return with page will openn (patient , receiption , radiology , pacs )
def user_page(data):
     is_employee=select_employee(data)
     is_patient=select_patient(data)
     
     if (is_employee is False ) and (is_patient is False ):
          return False
     if is_patient == 'patient':
          return f'/patient'
     if is_employee == 'Physician' :
          return f'/pacs'
     if is_employee =='radiologist':
          return f'/radiologist'
     if is_employee =='receptionist':
          return f'/front_desk'
     if is_employee =='HR':
          return f'/HR'
     if is_employee =='manager' or is_employee =='admin'or is_employee == 'clinical_eng' :
          return f'/admin'


# //////////////////////////////////////////////////////////////////////////////////

# used in login to get data to show it in its page 

# get data of patient using id  to put in patient page  using patient_ssn in registerrr
def get_all_data_patient(data={}):
    if data.get('id') is None:
         patient_ssn=data.get('patient_ssn')
    else :
         patient_ssn=data.get('id')
    cursor.execute('''
  select *
  from patient
  where patient_ssn = %s
''',( patient_ssn,))
    val =cursor.fetchone()
    return dict(val)


# get data of employee using id  to put in its page 
def get_all_data_employee(data={}): 
    
    cursor.execute('''
  select *
  from employee
  where employee_id = %s
''',( data['id'],))
    val =cursor.fetchone()
    val_ts=dict(val)


    val_ts['start_shift']= val_ts['start_shift'].strftime('%H:%M'),
    val_ts['end_shift']=val_ts['end_shift'].strftime('%H:%M'),
    val_ts['address']=val_ts['address_home_no']+" "+val_ts['address_street']+" "+val_ts['address_city']
    print(f'in get all data for employeee {val}')
  
    return val_ts
# get data of employee using id  to put in its page 
def get_all_data_tssts(data={}): 
    
    cursor.execute('''
  select *
  from employee
  where employee_id = %s
''',( data.get('employee_id'),))
    val =cursor.fetchone()
    val_ts=dict(val)


    # formatted_data = [
    #         {
    #             'start_shift': row['start_shift'].strftime('%H:%M'),
    #             'end_shift': row['end_shift'].strftime('%H:%M'),
    #             'address': f"{row['address_home_no']} {row['address_street']} {row['address_city']}"
    #         }
    #         for row in val_ts
    #     ]
    
    return val_ts


# //////////////////////////////////////

# registeerrrr form sure the correct data is enter 

def address_split(address):
    parts=address.split('_')
    if len(parts)==3:
        if parts[0].isdigit() and not parts[1].isdigit() and not parts[2].isdigit():
            address_dict = {
                'address_home_no': parts[0],
                'address_street': parts[1],
                'address_city': parts[2]
            }
            
            return address_dict
            

        else:
            return "enter num and 2 integers"
    else:
        return  "write 3 parts"

def name_split(name):
    parts=name.split(' ')
    if len(parts) >=2:
            name_dict = {
                'fname': parts[0],
                'lname': parts[1]
            }
            
            return name_dict
        
    else:
        return f' please enter 2 names'

def vaild_email(email):
    cursor.execute('''
        select email  from patient where email = %s  
    ''',(email,))
    data=cursor.fetchone()
    if data :
          return f'exist email'
    else :
          return True
    
def vaild_ssn(ssn):
    cursor.execute('''
        select patient_ssn  from patient where patient_ssn = %s  
    ''',(ssn,))
    data=cursor.fetchone()
    if data :
          return f'exist ssn '
    else :
          return True
    
# online registerr sure the 2 name , 3 address , unique ssn , email >> if true return true if not return messages 
def vaild_data(data={}):
     messages={}
     validated_data = {
    'name': name_split(data.get('name')),
    'address': address_split(data.get('address')),
    'ssn': vaild_ssn(data.get('patient')),
    'email': vaild_email(data.get('email'))
             }
     for key , val in validated_data.items():
          if isinstance(val , str):
               messages[key]= val
     if not messages:
        return True
    
     return messages

# creat account from online , offline 
def creat_account(data={}):
        val_ssn=vaild_ssn(data.get('patient_ssn'))
        val_data=vaild_data(data)
        val_email =vaild_email(data.get("email"))
        print(val_ssn , val_data)
        print(f" data from craete accountt {data}")
        if val_data == True and val_ssn== True:           
        # offline patient >> default email , password
            if data.get('email') is None:
                data['email']= data.get('patient_ssn')
                data['password']=((data.get('name')).split(' '))[0]+data['age']
                appointment_tech='guest'
            elif val_email == True :
                appointment_tech='user'
            else :
                 return val_email
              
            #   split the address
            address=data.get("address")
            address_tot=address_split(address)
            data['address']=address_tot 
        # split the name 
            name=data.get('name')
            name_tot=name_split(name)
            data['name']=name_tot 
            
            try:
                cursor.execute('''
                            insert into patient(patient_ssn, fname, lname,email, password, age,gender,phone_number,address_city, address_street , address_home_no,booking_technique)
                                    VALUES (%s ,%s,%s,%s,%s,%s ,%s,%s,%s,%s,%s,%s) 
                                    ''' , (data.get('patient_ssn') ,
                                            data.get('name').get('fname'),
                                            data.get('name').get('lname'),
                                            data.get('email' ),
                                            data.get('password'),
                                            data.get('age'),
                                            data.get('gender'), 
                                            data.get('phone_number')   , 
                                            data.get('address').get('address_city')   , 
                                            data.get('address').get('address_street')   , 
                                            data.get('address').get('address_home_no')   , 
                                            appointment_tech, ))
                database_connection.commit()
                return True

            except Exception as e:
                        print(f"An error occurred: {e}")
                        database_connection.rollback()
        else:
             return [val_ssn , val_data]





# def name_split_tst(name):
#     parts = name.split(' ')
#     if len(parts) >= 2:
#         name_dict = {
#             'fname': parts[0],
#             'lname': parts[1]
#         }
#         return name_dict
#     else:
#         return {
#             'fname': name,  # Assuming the entire input is treated as first name
#             'lname': ''     # Empty string for last name
#         }


# def construct_update_query(table_name, update_data, condition):
#     columns = []

#     # Split 'name' if it exists in update_data
#     if update_data.get('name'):
#         name_data = name_split_tst(update_data['name'])
#         update_data.update(name_data)
#         del update_data['name']

#     # Split 'address' if it exists in update_data
#     if update_data.get('address'):
#         address_data = address_split(update_data['address'])
#         update_data.update(address_data)
#         del update_data['address']

#     # Construct columns for SQL update statement
#     for key, value in update_data.items():
#         if value is not None:  # Only include non-None values
#             columns.append(f"{key} = '{value}'")

#     # Construct the SQL query
#     sql = f"UPDATE {table_name} SET {', '.join(columns)} WHERE {condition};"

#     # Execute the SQL query using the provided cursor
#     try:
#         cursor6.execute(sql)
#         database_connection.commit()
#         print("Update query executed successfully.")
#     except Exception as e:
#         print(f"Error executing update query: {str(e)}")

#     return sql

# # Example usage:
# update_data = {
#     'name': 'shaimaa',
#     'employee_id': '25',
#     'age': '58',
#     'gender': 'F',
#     'phone_number': '7573886103',
#     'email': 'carolsimmons@example.com',
#     'password': '6856',
#     'address': '63322_Cynthia_Pine_Andersonland',  # Example address in the format of 'home_no_street_city'
#     'salary': '78807',
#     'pay_scale': '1',
#     'start_shift': '17:30',
#     'end_shift': '08:45',
#     'branch_id': '3',
#     'technique': 'MRI Angiography'
# }

# cond=f"employee_id = {update_data.get('employee_id')}"
# construct_update_query('radiolohist' , update_data ,cond  )




def get_updates(curr, new_update):
    updates = {}
    for key, value in new_update.items():
        if key in curr.keys():
            current_value = curr.get(key)
            if str(value) != str(current_value) and str(value) != '' and key != 'csrf_token':
                updates[key] = value
    return updates







# return dic consist of 2 dic >> for creating and for appointment ollllllllllllld
def split_appointment(data={}):
     app_keys=['patient_ssn' , 'branch_name','modality','organ','date']
     patient_keys=['name' , 'patient_ssn', 'age' ,'gender','address','phone_number']
     patient,appointment={},{}
     for key in app_keys:
          appointment[key]=data.get(key)

     for key in patient_keys:
          patient[key]=data.get(key)

     return patient , appointment

# get data to create account , add rest of data to json file till the payment added 
# return patient data 
def json_app_patientdata(data={}):
    print("hereee in appiontmentt ")
    patient,json_data={},{}
    if data.get('fname') is not None:
      json_data['name']=data['fname']+' '+data['lname']
      json_keys=['patient_ssn' ,'age','phone_number', 'branch_name','modality','organ','datetime','gender']
    else:
        json_keys=['name','patient_ssn' ,'age','phone_number', 'branch_name','modality','organ','datetime','gender']

    patient_keys=['name' , 'patient_ssn', 'age' ,'gender','address','phone_number']
    
    for key in json_keys:
        json_data[key]=data.get(key)

    for key in patient_keys:
        patient[key]=data.get(key)

    print(f"the data added to json {json_data}")
    insert_data_json('front_table.json',json_data)
    return patient 




# use in patient table
def merge_date(merged_data):
    if 'date' in merged_data and 'time' in merged_data:
        # Convert date to ISO format if it isn't already
        if isinstance(merged_data['date'], datetime):
            date_str = merged_data['date'].isoformat()
        else:
            date_str = merged_data['date']
        
        # Combine date and time into a single datetime object
        datetime_obj = datetime.fromisoformat(f"{date_str}T{merged_data['time'].strftime('%H:%M:%S')}")
        
        # Format the datetime object to the desired format
        day = datetime_obj.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        formatted_date = datetime_obj.strftime(f'%d{suffix} %B %Y, %I:%M %p')
        
        # Update the merged_data dictionary
        merged_data['datetime'] = str(formatted_date)
        del merged_data['date']
        del merged_data['time']
        
    return merged_data

# change its format to patient table 
def format_datetime(data):
    for entry in data:
        if 'datetime' in entry:
            # Parse the datetime string into a datetime object
            datetime_obj = datetime.fromisoformat(entry['datetime'])

            # Format the datetime object into the desired string format
            formatted_date_str = datetime_obj.strftime('%dth %B %Y, %I:%M %p')

            # Update the 'datetime' key in the dictionary with the formatted string
            entry['datetime'] = formatted_date_str

    return data

def merge_names_and_serialize_data(data):
    merged_data = data.copy()
    print(f"data in merge namesss is {data}")
    fname = merged_data.pop('fname')
    lname = merged_data.pop('lname')
    merged_data['name'] = f"{fname} {lname}"
    if 'date' in merged_data:
        merged_data['date'] = merged_data['date'].isoformat()
    time_str = merged_data['time'].strftime('%H:%M:%S')

    datetime_str = f"{merged_data['date']}T{time_str}"
    merged_data['datetime'] = datetime_str
    del merged_data['date']
    del merged_data['time']
    
    # Return the modified data
    return merged_data

















# this for pacssss 
def merge_name(data):
    merged_data = data.copy()
    fname = merged_data.pop('fname')
    lname = merged_data.pop('lname')
    merged_data['name'] = f"{fname} {lname}"
    return merged_data


def split_datetime(datetime_string):
    date_part, time_part = datetime_string.split('T')
    return date_part, time_part



# ///////////////////////////////////////////////////
# add appointment(online , offlineee) with paymentttt
def add_appointment(data={}):
              
              branch_id=get_branch_id(data['branch_name'])
              date,time=split_datetime(data['datetime'])

              cursor.execute('''
                          insert into register (patient_ssn, branch_id, date ,time,modality,organ,branch_name,payment)
                                  VALUES (%s ,%s,%s,%s,%s,%s,%s,%s) 
                                  ''' , (data.get('patient_ssn') ,
                                           branch_id,
                                           date,
                                           time,
                                           data.get('modality' ),
                                           data.get('organ'),
                                           data.get('branch_name'), 
                                           data.get('payment') ))
              database_connection.commit()
              return True



# add data for radiologyy tablee send the json fileeeee 

def radiology_add_payment(data):
     app_keys=['name','patient_ssn' , 'branch_name','modality','organ','datetime']
     rad_table={}
     for key in app_keys:
         rad_table[key]=data.get(key)
     

     insert_data_json('radiology_table.json',rad_table)
     return "inserteddd"








def pacs_table_data():
    try:
        cursor.execute(
            '''
            SELECT
                p.fname, p.lname, p.patient_ssn, p.age, p.gender,
                r.organ, r.modality, r.branch_name, r.date as datetime, e.radiologist_id,
                e.scan_folder, e.verified, e.doctor_id, e.report
            FROM
                patient p
            JOIN
                register r ON p.patient_ssn = r.patient_ssn
            JOIN
                radiology_exams e ON p.patient_ssn = e.patient_ssn
            WHERE
                r.modality = e.modality
                AND r.organ = e.organ
                AND r.date = e.date
                AND r.time = e.time
            '''
        )
        data = cursor.fetchall()
        
        new_data = [dict(row) for row in data]
        print(f"data geted from pacs {new_data}")
        data_n = [merge_name(row) for row in new_data]  # Assuming merge_name function is defined elsewhere
        
        return data_n
     
    except Exception as e:
        print(f"An error occurred: {e}")






# get the id to add in appointment
def get_branch_id(branch_name):
    cursor.execute('''
        select branch_id  from branch where bname = %s  
    ''',(branch_name,))
    data=cursor.fetchone()
    return data[0]

# get the devicee ssn 
def get_device_id(device_name , device_branch):
    cursor.execute('''
        select device_sn  from device where device_name = %s  and device_branch=%s
    ''',(device_name,device_branch))
    data=cursor.fetchone()

    return data[0]




# /////////////////////////////////////////////
# hereeee correcteeeeeeee

# add data in radiologist examm >>> send to pacsss 
def add_radiolgistexamm(data={}):
    print(f"data entered to radiology examm is {data}")
    branch_id = get_branch_id(data.get('branch_name'))
    device_sn = get_device_id(data.get('modality'), branch_id)
    date, time = split_datetime(data.get('datetime'))
    verified="Not Checked"
    try:
        cursor.execute('''
            INSERT INTO radiology_exams (patient_ssn, scan_folder, modality, organ, radiologist_id, device_sn, date, time,verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
        ''', (
            data.get('patient_ssn'),
            data.get('scan'),
            data.get('modality'),
            data.get('organ'),
            data.get('rad_id'),
            device_sn,
            date,
            time,
            verified
        ))
        database_connection.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()
        return False

def convert_datetime_tst(merged_data):
    merged_data['date'] = merged_data['date'].isoformat()
    time_str = merged_data['time'].strftime('%H:%M:%S')

    datetime_str = f"{merged_data['date']}T{time_str}"
    merged_data['datetime'] = datetime_str
    del merged_data['date']
    del merged_data['time']
    return merged_data




def get_app_database(app_type, date):
    print(f"date fromm database {date}")
    query = '''
        SELECT p.fname, p.lname, p.patient_ssn, p.age, p.gender, p.phone_number, b.bname,
               r.modality, r.organ, r.date, r.time, r.payment 
        FROM register r
        JOIN patient p ON r.patient_ssn = p.patient_ssn
        JOIN branch b ON r.branch_id = b.branch_id
    '''

    if app_type == 'today_app':
        query += ' WHERE r.date = %s'
    elif app_type == 'next_app':
        query += ' WHERE r.date > %s'
    elif app_type == 'previous_app':
        query += ' WHERE r.date < %s'
    else:
        print("Invalid appointment type provided.")
        return []

    try:
        cursor.execute(query, (date,))
        data = cursor.fetchall()
        data = [dict(row) for row in data]
        print(data)
        # Convert date and time to ISO format datetime string
        data = [convert_datetime_tst(row) for row in data]
        data=[merge_name(row) for row in data]
        print(f"data nowww{data}")
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


    




























def extract_non_empty_values(data):
    extracted_data = {}

    # Specify the fields to extract
    fields_to_extract = ['name', 'id', 'email', 'password', 'age', 'phone_number', 'address']

    # Loop through specified fields and add non-empty values to extracted_data
    for field in fields_to_extract:
        if data[field] != '':
            extracted_data[field] = data[field]

    return extracted_data

# # Example usage:
# input_data ={'message': 'Patient data updated successfully', 'data':
#               {'csrf_token': 'IjIwYzk2NzMxMzMzZjViODYyZWNkNjBmYzJkMjk5Y2UxYzQyODhhOGUi.Znd-2Q.FPS8URMEuH-ggcKMH3eZmApMVVY', 
#                'organ': 'Brain', 'modality': 'MRI Machine', 'branch_name': 'Port Said Clinic', 
#                'datetime': '', 'name': 'dhsfjhdsfdsf', 'id': '', 'email': '', 
#                'password': '', 'age': '', 'phone_number': '', 'address': ''}}


# selected_fields = extract_non_empty_values(input_data['data'])
# print(selected_fields)












from datetime import datetime

from datetime import datetime

from datetime import datetime, date

def filter_by_date(json_data, base_date_str, text):
    print(f"heree filteerrrr {base_date_str}")
    base_date = datetime.strptime(base_date_str, '%Y-%m-%d').date()  # Convert base_date_str to datetime.date object

    results = []
    for entry in json_data:
        entry_date = datetime.strptime(entry['datetime'], '%Y-%m-%dT%H:%M').date()  # Adjusted format without seconds
        if text == 'next_app' and entry_date > base_date:
            results.append(entry)
        elif text == 'previous_app' and entry_date < base_date:
            results.append(entry)
        elif text == 'today_app' and entry_date == base_date:
            results.append(entry)

    return results

# # Example usage:
# json_data = [
#     {
#         "name": "muhammed salah",
#         "patient_ssn": "1",
#         "age": "20",
#         "phone_number": "276678",
#         "branch_name": "Assiut Health Institute",
#         "modality": "CT Scanner",
#         "organ": "Stomach",
#         "datetime": "2024-06-27T10:01",
#         "gender": "M"
#     },
#     {
#         "name": "shaimaa shaheen ",
#         "patient_ssn": "2",
#         "age": "20",
#         "phone_number": "276678",
#         "branch_name": "Mansoura General Hospital",
#         "modality": "MRI Machine",
#         "organ": "Intestine",
#         "datetime": "2024-06-22T09:24",
#         "gender": "F"
#     }
# ]

# base_date = date.today()  # Today's date
# print("Base Date:", base_date)

# print("\nPrevious dates:")
# print(filter_by_date(json_data, str(base_date), 'previous'))

# print("\nNext dates:")
# print(filter_by_date(json_data, str(base_date), 'next'))

# print("\nSame dates:")
# print(filter_by_date(json_data, str(base_date), 'same'))



# /////////////////////////////////////////////////////////




def update_payment(data):
    date, time=split_datetime(data.get('datetime'))
    branch=get_branch_id(data.get('branch_name'))

    try:
        cursor.execute('''
update  register  r set payment=%s
where  r.patient_ssn = %s and r.date=%s and r.time=%s and r.branch_id=%s

        ''',(
          data.get('payment'),
          data.get('patient_ssn'),
          date,
          time,
          branch

        ))
        database_connection.commit()

        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()







# updateee data in radiologyy exammmmm 
def update_pacs(data):
    try:
        cursor.execute('''
            UPDATE RADIOLOGY_EXAMs
            SET doctor_id = %s, report = %s, verified = %s
            WHERE patient_ssn = %s AND scan_folder = %s;
        ''', (
            data.get('doctor_id'),
            data.get('report'),
            data.get('status'),
            data.get('patient_ssn'),
            data.get('scan')
        ))
        database_connection.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()
        return False








def get_rad_database(app_type, date):

    query = '''
SELECT p.fname, p.lname, p.patient_ssn, b.bname,
       r.modality, r.organ, r.date, r.time, r.scan_folder, r.radiologist_id
FROM radiology_exams r
JOIN register g ON r.date = g.date AND r.time = g.time
JOIN patient p ON g.patient_ssn = p.patient_ssn
JOIN branch b ON g.branch_id = b.branch_id
    '''

    if app_type == 'today_rad':
        query += ' WHERE r.date = %s'
    elif app_type == 'next_rad':
        query += ' WHERE r.date > %s'
    elif app_type == 'previous_rad':
        query += ' WHERE r.date < %s'
    else:
        print("Invalid appointment type provided.")
        return []

    try:
        cursor.execute(query, (date,))
        data = cursor.fetchall()
        data = [dict(row) for row in data]
        # Convert date and time to ISO format datetime string
        data = [convert_datetime_tst(row) for row in data]
        data=[merge_name(row) for row in data]
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []







# all functions dealll with jsonn fileeee

folder_path_all = r'C:\Users\lenovo\Final_project\his-finalproject-database_sbe_spring24_team5\json_files'

def create_json_file(file_name, initial_data=None, folder_path=folder_path_all):
    if initial_data is None:
        initial_data = {}
    
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as json_file:
        json.dump(initial_data, json_file, indent=4)
    print(f"New JSON file created at {file_path}")


def insert_data_json(file_name, new_data, folder_path=folder_path_all):
    file_path = os.path.join(folder_path, file_name)
    
    try:
        with open(file_path, 'r+') as json_file:
            data = json.load(json_file)
            
            if isinstance(data, dict):
                if isinstance(new_data, dict):
                    data.update(new_data)
                else:
                    print("New data must be a dictionary to update the JSON dictionary.")
                    return
            elif isinstance(data, list):
                if isinstance(new_data, list):
                    data.extend(new_data)
                else:
                    data.append(new_data)
            else:
                print("Unsupported JSON data type.")
                return
            
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()
        print("Data inserted successfully.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"The file {file_path} is empty or contains invalid JSON.")


def read_data(file_name, folder_path=folder_path_all):    
    file_path = os.path.join(folder_path, file_name)
    
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        # print("Data read successfully.")
        return data
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    
# get data from the offline appoinment , online till get scann 
def get_data_for_patient(file_name,patient_ssn,folder_path=folder_path_all):

    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as json_file:
            data = json.load(json_file)

    # Filter the data based on patient_ssn             patient_ssn
    filtered_data = [entry for entry in data if int(entry["patient_ssn"]) == patient_ssn]

    if filtered_data:
        return filtered_data
    else:
        return {}



def delete_object_from_json(json_file, record, folder_path=folder_path_all):
    file_path = os.path.join(folder_path, json_file)
    
    # Read JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Convert record values to string for consistent comparison
    record = {k: str(v) for k, v in record.items()}
    
    # Find and delete the object that matches the record
    data = [obj for obj in data if not all(str(obj.get(key)) == value for key, value in record.items())]

    # Write updated JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# delete the appointment from json 
def del_appoinm(data):
     data_tst=data.copy()
     data_tst.pop('csrf_token')
     data_tst.pop('payment')
     print(f"data that will deletedd is {data_tst}")
     delete_object_from_json('front_table.json',data_tst)
     print("deletedd appionment")


# delete the the exam from radiologistttt
def del_rad_exam(data):
     data_tst=data.copy()
     data_tst.pop('csrf_token')
     data_tst.pop('rad_id')
     data_tst.pop('scan')
     print(f"data that will deletedd in radiology exammm  {data_tst}")
     delete_object_from_json('radiology_table.json',data_tst)
     print("deletedd radiology_exammmm")


# all devicesss 
def get_devices():

      try:
        cursor2.execute('''
select  d.device_tech , f.device_name , b.bname
    from device_tech d , device f , branch b
where  d.device_sn = f.device_sn  and b.branch_id = f.device_branch
        ''')
        out=cursor2.fetchall() 
        new_data=[dict(row) for row in out]
        return new_data
      except Exception as e:
          print(f"An error occurred: {e}")
          database_connection.rollback()



def select_keys(data):
     dic={}
     keys=['organ','modality','branch_name','datetime']
     for key in keys:
          dic[key]=data[key]
     if data.get('scan_folder') is None:
          dic['verified']="waiting the date of appoinment"
      
     return dic





def table_patient_pacs(data):
    print(f" patient ssn is {data.get('patient_ssn')}")
    try:
        cursor.execute(
            '''
            SELECT  r.organ, r.modality, g.branch_name, r.date, r.time,
                r.scan_folder, r.verified, r.report
            FROM  radiology_exams r  , register g
            WHERE  r.patient_ssn = g.patient_ssn and
                   r.date =g.date and r.time = g.time and
                r.patient_ssn = %s
            ''',
            (data.get('patient_ssn'),)
        )
        
        tst_dataaa = cursor.fetchall()
        print(f"the data direct fetcheddddd  in functionnn {tst_dataaa}")
        tst_dataaa2 = [dict(row) for row in tst_dataaa]    
        final_data = [merge_date(row) for row in tst_dataaa2]
        # for row in final_data:
        #     if isinstance(row['time'], sqlite3.Row):
        #         row['time'] = row['time'].strftime('%H:%M:%S')

        return final_data
     
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()








def get_all_patient_status(data_patient):
     from_pacs=table_patient_pacs(data_patient)
     from_frontdisk = get_data_for_patient('front_table.json',data_patient.get('patient_ssn'))
    #  formate the datetimee
     new_from_frontdisk=format_datetime(from_frontdisk)
    #  select needed data only 
     front_data=[select_keys(row) for row in new_from_frontdisk ]

     from_radiology = get_data_for_patient('radiology_table.json',data_patient.get('patient_ssn'))
    #  formate the datetimee
     new_from_radiology=format_datetime(from_radiology)
    #  select needed data only 
     rad_data=[select_keys(row) for row in new_from_radiology ]
     print("//////////////////////////////////////////////////////")
     print(f"in function statuss the data from the sqlll functionn is {from_pacs}")
     print(f"in function statuss the data from the json front table {front_data}")
     print(f"in function statuss the data from the json radiologyyy {rad_data}")
     all_data=from_pacs + front_data +rad_data
     print(f"all data from the function {all_data}")
     return all_data
      


def get_employee_table_admin(job_title):
        try:
            cursor5.execute(
                '''
SELECT e.*, s.SCAN_TYPE, t.TECHNIQUE , w.branch_id
FROM employee e
LEFT JOIN SCAN_TYPE s ON e.employee_id = s.PH_ID
LEFT JOIN TECHNIQUE t ON e.employee_id = t.R_ID
INNER JOIN works_at w ON e.employee_id = w.employee_id 
                WHERE e.job_title = %s
                ''',
                (job_title,)
            )
            
            data = cursor5.fetchall()
        except Exception as e:
           print(f"An error occurred: {e}")

        
        
        formatted_data = [
            {
                **merge_name(dict(row)),
                'start_shift': row['start_shift'].strftime('%H:%M'),
                'end_shift': row['end_shift'].strftime('%H:%M'),
                'address': f"{row['address_home_no']} {row['address_street']} {row['address_city']}"
            }
            for row in data
        ]
        
        return formatted_data
    





def get_patient_table_admin():
    try:
        cursor5.execute(
            '''
            SELECT *
            FROM patient 

            '''
        )
        
        data = cursor5.fetchall()
        formatted_data = [
            {
                **merge_name(dict(row)),
                'address': f"{row['address_home_no']} {row['address_street']} {row['address_city']}"
            }
            for row in data
        ]

        return formatted_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()



def get_device_table_admin():
    try:
        cursor5.execute(
            '''
select  d.device_tech ,d.device_sn , f.d_data1 ,f.d_data2 , f.d_data3, f.device_name , b.bname
    from device_tech d , device f , branch b
where  d.device_sn = f.device_sn  and b.branch_id = f.device_branch

            '''
        )
        
        data = cursor5.fetchall()
        formatted_data = [dict(row) for row in data]
        return formatted_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()

def get_branch_table_admin():
    try:
        cursor5.execute(
            '''
select  *
from  branch

            '''
        )
        
        data = cursor5.fetchall()
        formatted_data = [dict(row) for row in data]
        return formatted_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        database_connection.rollback()









# //////////////////////charttttts /////////////////////////
def num_malfunctions_per_device():
    try:
        cursor.execute(
            '''
select d.device_name , d.num_malfunctions
    from DEVICE d
            '''
        )
        data = cursor.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")



# print(num_malfunctions_per_device())


def maintenance_per_device():
    try:
        cursor2.execute(
            '''
SELECT device_name, d.corrective_maintenance,
 d.preventative_maintenance  FROM device d

            '''
        )
        data = cursor2.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")


def installation_date_distribution():
    try:
        cursor3.execute(
            '''
SELECT
    TO_CHAR(installation_date, 'Mon YYYY') AS month_year_label,
    COUNT(*) AS installation_count
FROM
    device
GROUP BY
    TO_CHAR(installation_date, 'Mon YYYY')
            '''
        )
        data = cursor3.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")





 
        
def devices_near_warranty_expiry():
    try:
        cursor4.execute(
            '''
SELECT device_name, warrantyexpirydate
FROM device
WHERE warrantyexpirydate <= CURRENT_DATE + INTERVAL '30 days'
ORDER BY warrantyexpirydate;
            '''
        )
        data = cursor4.fetchall()        
        new_data = [dict(row) for row in data]  
        formatted_data = [
    {
        'device_name': device['device_name'],
        'warrantyexpirydate': device['warrantyexpirydate'].strftime('%Y-%m-%d')
    }
    for device in new_data
]
        return formatted_data
     
    except Exception as e:
        print(f"An error occurred: {e}")








def gender_distribution(job_title):
    try:
        cursor.execute(
            '''
SELECT gender, COUNT(*) AS count FROM employee e 
where e.job_title =%s
GROUP BY gender
            '''
       ,(job_title,) )
        data = cursor.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")








def payment_distribution(job_title):
    try:
        cursor2.execute(
            '''
SELECT payment, COUNT(*) AS count FROM employee e 
where e.job_title=%s
GROUP BY payment
            '''
       ,( job_title ,) )
        data = cursor2.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")





def salary_distribution(job_title):
    print(job_title)
    try:
        cursor3.execute(
            '''

SELECT
    CASE
        WHEN salary BETWEEN 0 AND 10000 THEN '0-10,000'
        WHEN salary BETWEEN 10001 AND 20000 THEN '10,001-20,000'
        WHEN salary BETWEEN 20001 AND 30000 THEN '20,001-30,000'
        WHEN salary BETWEEN 30001 AND 40000 THEN '30,001-40,000'
        WHEN salary BETWEEN 40001 AND 50000 THEN '40,001-50,000'
        WHEN salary BETWEEN 50001 AND 60000 THEN '50,001-60,000'
        WHEN salary BETWEEN 60001 AND 70000 THEN '60,001-70,000'
        WHEN salary BETWEEN 70001 AND 80000 THEN '70,001-80,000'
        WHEN salary BETWEEN 80001 AND 90000 THEN '80,001-90,000'
        WHEN salary BETWEEN 90001 AND 100000 THEN '90,001-120,000'
        ELSE '100,001+'
    END AS salary_range,
    COUNT(*) AS count
FROM
    employee e
where e.job_title=%s
GROUP BY
    salary_range
ORDER BY
    salary_range;
            '''
      , ( job_title ,) )
        data = cursor3.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")


def age_distribution(job_title):
    print(job_title)
    try:
        cursor6.execute(
            '''


SELECT
    CASE
        WHEN age BETWEEN 20 AND 29 THEN '20-29'
        WHEN age BETWEEN 30 AND 39 THEN '30-39'
        WHEN age BETWEEN 40 AND 49 THEN '40-49'
        WHEN age BETWEEN 50 AND 59 THEN '50-59'
        WHEN age BETWEEN 60 AND 69 THEN '60-69'
        ELSE '70+'
    END AS age_range,
    COUNT(*) AS count
FROM
    employee
WHERE
    job_title = %s
GROUP BY
    age_range
ORDER BY
    age_range;
            '''
      , ( job_title ,) )
        data = cursor6.fetchall()        
        new_data = [dict(row) for row in data]       
        return new_data
     
    except Exception as e:
        print(f"An error occurred: {e}")









def tech_distribution(job_title):

    if job_title=='Physician':
        try:
            cursor6.execute(
                '''

    SELECT s.SCAN_TYPE, COUNT(*) AS count FROM employee e, scan_type s
    where e.employee_id = s.PH_ID
    GROUP BY s.SCAN_TYPE

                '''
            )
            data = cursor6.fetchall()        
            new_data = [dict(row) for row in data]       
            return new_data
        
        except Exception as e:
            print(f"An error occurred: {e}")

    if job_title == 'radiologist':
        try:
            cursor4.execute(
                '''

    SELECT t.TECHNIQUE, COUNT(*) AS count FROM employee e, technique t
    where e.employee_id = t.R_ID
    GROUP BY t.technique

                '''
            )
            data = cursor4.fetchall()        
            new_data = [dict(row) for row in data]       
            return new_data
        
        except Exception as e:
            print(f"An error occurred: {e}")









































