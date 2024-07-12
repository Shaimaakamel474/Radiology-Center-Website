from flask import Flask , request , render_template , redirect , session ,jsonify , url_for,send_from_directory
from flask_wtf.csrf import generate_csrf , CSRFProtect
import secrets
from forms import *
from connections import *
import os
from werkzeug.utils import secure_filename
app= Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a random key
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)



BASE_DIR=r'E:\Med_ray\Cancer_Mediastinal_window\PACS SYSTEM'





# home pageeee 
@app.route('/',methods=['POST', 'GET'])
def home():
   csrf=generate_csrf()
   return render_template('/main.html',csrf_token=csrf)



@app.route('/login' , methods =['POST', 'GET'])
def login( ):
    if request.method == 'POST':   
        form=login_form(request.form)
        if form.validate_on_submit():
            data=request.form.to_dict()
            print (f"in login data knoww  iss {data}")  
            
            page=user_page(data)
            print(f"the pageeeeee is {page}")           
            
            if page is False :
                csrf_token = generate_csrf()
                return  render_template('Login.html',csrf_token=csrf_token) 


            if page =='/patient':
                patient_data=get_all_data_patient(data)
                print(f"alll patient dataaaa isss  {patient_data}")
                # add patient to the session 
                session['patient']=patient_data
            else:
                # get the data based on id of employee
                employee_data=get_all_data_employee(data)

                emp=employee_data['job_title']
                print(f"empp noww is sss{emp}")

                # add employee in session based on its title
                session[emp]=employee_data
                print(f"dataaa for this {emp} is {session}")
            
            print(f"in redirectt {page}")
            # here must be redirecttt
            return redirect(page)  
           
        else :
            # error in vaildation
            for field, errors in form.errors.items():
                for error in errors:
                    print(f" in field :{field} the error is : {error}")
                    csrf_token = generate_csrf() 
                    render_template('Login.html',csrf_token=csrf_token) 
    
    
    # if it wasss get request

    csrf_token = generate_csrf()
    print(f"in loginn gett ")
    return render_template('Login.html',csrf_token=csrf_token)












@app.route('/register' , methods =['POST' , 'GET'])
def register():
    my_messages={}
    if request.method=='POST':
        form=Register_form(request.form)
        if form.validate_on_submit():

            patient_data=request.form.to_dict()   
            print(f"user data is nowww  {patient_data}")
            
            all_vaild=vaild_data(patient_data)
        #    sure the all data vaild else return messagess 
            if all_vaild == True:
               add=creat_account(patient_data)
               session['patient']=get_all_data_patient(patient_data)
               print(f'createddddddddd{add}')
               return redirect('/patient' )
            else:
                print(f'the vaildationnnn {all_vaild}')


        else:
            for field, errors in form.errors.items():
                for error in errors:
                    my_messages[f'{field}']=error
                     

    csrf_token = generate_csrf()   
    return render_template('register.html',csrf_token=csrf_token)




@app.route('/patient' , methods =['POST' , 'GET'])
def patient():
    print(f"in patientttttt  {session.get('patient')}")
    if session.get('patient') is not None:
       data=session.get('patient')
    #    print(f"in user the all data know isss {data}")
       csrf_token = generate_csrf()  
       return render_template('patient.html',data=data , csrf_token=csrf_token)
    else:
        # print("in elsee go to loginnnnn")
        return redirect('/login')



@app.route('/pacs' , methods =['POST' , 'GET'])
def pacs():
    if session.get('Physician') is not None:
        data_user=session['Physician']
        csrf_token = generate_csrf()  
        return render_template('pacs.html',csrf_token=csrf_token,data=data_user)
    elif session.get('admin') is not None:
        data_user=session['admin']
        csrf_token = generate_csrf()  
        return render_template('pacs.html',csrf_token=csrf_token,data=data_user)
    else:
        return redirect('/login')



@app.route('/radiologist' , methods =['POST' , 'GET'])
def radiologist():
    print("hereee in radiology")
    
    if session.get('radiologist') is not None:
        data_user=session['radiologist']
        print(f"radiologist data noww {data_user}")
        csrf_token = generate_csrf()
        return render_template('radiologist.html',data=data_user,csrf_token=csrf_token)
    elif session.get('admin') is not None:
        data_user=session['admin']
        csrf_token = generate_csrf()
        return render_template('radiologist.html',data=data_user,csrf_token=csrf_token)
    else:
        return redirect('/login')    


@app.route('/front_desk' , methods =['POST' , 'GET'])
def front_desk():

    if session.get('receptionist') is not None:
        user_data=session['receptionist']
        csrf_token = generate_csrf()
        return render_template('front_desk.html' , csrf_token=csrf_token,data=user_data)
    elif session.get('admin') is not None:
        user_data=session['admin']
        csrf_token = generate_csrf()
        return render_template('front_desk.html' , csrf_token=csrf_token,data=user_data)
    else:
        print(f"the data for receptionist is not in session {session}")
        return redirect('/login')





@app.route('/offline_patient' , methods =['POST'])
def offline_patient():
        # print("in offline patientttt appointmentt")
        form=offline_appointment(request.form)
        if form.validate_on_submit():
            # print("in posttttt and vaild formm")
            all_data=request.form.to_dict()  
            # print(f"data for the offline appoinment {all_data}")
          
            print(f"all data for appiontmenttt {all_data}")
            # get patient data and add appionment to json fileeeee
            patient_data  =json_app_patientdata(all_data)
            print(f"data_patient{patient_data}")


            created=creat_account(patient_data)
            print(f'the accounttt created for online patient{created}')
            


            return redirect('/front_desk')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"offline error  {field} :{error}")
            return redirect('/front_desk')


@app.route('/online_patient' , methods =['POST'])
def online_patient():
        # print("in onlineee patientttt appointmentt")

        form=online_appointment(request.form)
        if form.validate_on_submit():
            # print("in posttttt and vaild formm")
            all_data=request.form.to_dict()  

            if session.get('patient') is not None :
                print(f"the data from session noww isss {session.get('patient')}")
                
                # merge the patient data from session and the data get from the form 
                all_data.update(session.get('patient'))

                print(f"all data to split{all_data}")
                json_app_patientdata(all_data)
                return redirect('/patient')
           
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f' the field is {field} :{error}')
            return redirect('/patient')
                     
@app.route('/register_emp' , methods =['POST' , 'GET'])
def register_emp():  
    if request.method=='POST':
        # print("in postttttttttttttttttt")
        print(request.form.to_dict() )
        form=Register_emp(request.form)
        if form.validate_on_submit():
            print("in posttttt and vaild formm")
            emp_data=request.form.to_dict()   
            print(f"user data is nowww 9 {emp_data}")
            emp_data.pop('csrf_token')
            insert_data_json('register_emp.json',emp_data)
            
        else:
            print("in elseeee ")
            for field, errors in form.errors.items():
                for error in errors:
                   print(f" the field: {field} the error is: {error}")


    # print("in gettttttttt in registerr_emppppp")
    csrf_token = generate_csrf()   
    return render_template('register_emp.html',csrf_token=csrf_token)



# admin pageee
@app.route('/admin',methods=['POST', 'GET'])
def admin():
    if session.get('admin') is not None:
        user_data=session['admin']
        csrf_token = generate_csrf()
        return render_template('home_admin.html' , csrf_token=csrf_token,data=user_data)
    else:
        print(f"the data for receptionist is not in session {session}")
        return redirect('/login')




today = date.today()  
print(today)

# # sendd jsonnnn file to front deskk
# @app.route('/front_desk_table', methods=['GET'])
# def front_table():
#     data= read_data('front_table.json')
#     database_info=get_app_database()
#     tot= data+database_info
#     print(f"adataa from front_deskkk {tot}")
#     return jsonify(tot)



@app.route('/today_app', methods=['GET'])
def get_patients_endpoint1():
    print("heree")
    json_data=read_data('front_table.json')
    data=get_app_database('today_app',f"'{today}'" )
   
    tod=filter_by_date(json_data ,str(today),'today_app')
    
    tot=  tod +data  
    print(f"the functionn {tot}")
    return jsonify(tot)


@app.route('/next_app', methods=['GET'])
def get_patients_endpoint2():
    json_data=read_data('front_table.json')
    data=get_app_database('next_app' ,f"'{today}'")
   
    nex=filter_by_date(json_data,str(today),'next_app')
    # print(f"the functionn {nex}")
    tot=nex +data  
    return jsonify(tot)

@app.route('/previous_app', methods=['GET'])
def get_patients_endpoint3():
    json_data=read_data('front_table.json')
    data=get_app_database('previous_app',f"'{today}'" )
    # print(f"data from database  perrr {data}")
    per=filter_by_date(json_data ,str(today),'previous_app')
    # print(f"the functionn {per}")
    tot=data + per
    return jsonify(tot)

@app.route('/all_app', methods=['GET'])
def get_patients_endpoint4():
    json_data=read_data('front_table.json')
    data_per=get_app_database('previous_app',f"'{today}'" )
    per=filter_by_date(json_data ,str(today),'previous_app')

    data_tod=get_app_database('today_app',f"'{today}'" )
    tod=filter_by_date(json_data ,str(today),'today_app')

    data_nex=get_app_database('next_app',f"'{today}'" )
    nex=filter_by_date(json_data ,str(today),'next_app')
   
    tot=data_nex+nex +tod + data_tod+ data_per + per
    return jsonify(tot)













# add appionment inn databaseee with paymentt
@app.route('/get_payment', methods=['POST','GET'])
def get_payment():
    print("in gettt paymentttt")
    if request.method == 'POST':
        # print("in postttt get paymenttt")
        data = request.form  # Retrieve form data
        data=data.to_dict()
        print(f"data get from get payment {data}")
        add_ap=add_appointment(data)
        print(f"the appoinment creationnn {add_ap}")
         # deletee the appiontmenttt from json 
        
        del_appoinm(data)

        # add data to radiology table with paymenttt
        rad=radiology_add_payment(data)
        print(f"the dataa in radiolgyy {rad}")

        return redirect('/front_desk')
    print("here in gettt in shaimaaa")
    return redirect('/front_desk')








@app.route('/front_desk_updated', methods=['POST'])
def front_desk_updated():
    if request.method == 'POST':
        print("in postttt front_desk updatedd")
        data = request.form  # Retrieve form data
        data=data.to_dict()
        print(f"the updated front_desk is {data}")
        tst=update_payment(data)
    print(f" updateee paymentt {tst}")
    return redirect('/front_desk')






@app.route('/cancel_app' , methods=['POST'])
def cancel_app():
    if request.method == 'POST':
            data = request.form  # Retrieve form data
            data=data.to_dict()
            del_appoinm(data)

    return redirect('/front_desk')



# send json for radiology 
@app.route('/radiology_table', methods=['GET'])
def radiology_tabless():
    data= read_data('radiology_table.json')
    print("in radiologyyyy tableee{data}")
    return jsonify(data)




@app.route('/today_rad', methods=['GET'])
def get_rad_endpoint1():
    print("here todaaaay")
    json_data=read_data('radiology_table.json')
    data=get_rad_database('today_rad',f"'{today}'" )
    
    # print(f"data get from database {data}")
    
    tod=filter_by_date(json_data ,str(today),'today_app')
    # print(f"the jsonnn today  {tod}")
    tot=  tod +data  
    return jsonify(tot)


@app.route('/next_rad', methods=['GET'])
def get_rad_endpoint2():

    json_data=read_data('radiology_table.json')
    data=get_rad_database('next_rad' ,f"'{today}'")
   
    nex=filter_by_date(json_data,str(today),'next_app')
    # print(f"the functionn {nex}")
    tot=nex +data 
    print(tot) 
    return jsonify(tot)

@app.route('/previous_rad', methods=['GET'])
def get_rad_endpoint3():
    print("previousss")
    json_data=read_data('radiology_table.json')
    data=get_rad_database('previous_rad',f"'{today}'" )
    # print(f"data from database  perrr {data}")
    per=filter_by_date(json_data ,str(today),'previous_app')
    # print(f"the functionn {per}")
    tot=data + per
    return jsonify(tot)

@app.route('/all_rad', methods=['GET'])
def get_rad_endpoint4():
    json_data=read_data('radiology_table.json')
    data_per=get_rad_database('previous_rad',f"'{today}'" )
    per=filter_by_date(json_data ,str(today),'previous_app')

    data_tod=get_rad_database('today_rad',f"'{today}'" )
    tod=filter_by_date(json_data ,str(today),'today_app')

    data_nex=get_rad_database('next_rad',f"'{today}'" )
    nex=filter_by_date(json_data ,str(today),'next_app')
   
    tot=data_nex+nex +tod + data_tod+ data_per + per
    print(f"allllllllllllllllllllllllll {tot}")
    return jsonify(tot)






## get the scann folder and id radiology add them to database
# get the scann folder and id radiology add them to database
@app.route('/get_scan', methods=['POST'])
def get_scan():
    if request.method == 'POST':
        print("in postttt scaannnnnnnnn")
        data = request.form  # Retrieve form data
        data=data.to_dict()
        print(f"dataaaa isss in get scannnn {data}")
        # delte the examm 
        del_rad_exam(data)

        # Get uploaded files
        files = request.files.getlist('files')
        print(files)


        file = files[0]
        # Secure the filename
        filename_folder = secure_filename(file.filename)
        # Split the filename to extract the folder part
        folder_name = filename_folder.split('_')[0]
        data['scan']=folder_name

        upload_directory = os.path.join(BASE_DIR, str(folder_name))
        os.makedirs(upload_directory, exist_ok=True)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        
        for file in files:
            filename = secure_filename(file.filename)
            if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                file_path = os.path.join(upload_directory, filename)
                file.save(file_path)
                print(f"Saved file: {file_path}")


        # createe database for the radiologyy exammmm 
        print(f"data before enter the exammm")
        tst=add_radiolgistexamm(data)
        print(f"addd the radiology to databasee {tst}")

        return jsonify(tst)
    # print("here in gettt in get scann")
    # return 

















# get data for pacs from the database
@app.route('/pacs_table', methods=['GET'])
def pacs_table():
    print("in pacss noww shaimaa")
    data=pacs_table_data()
    print(f"dataaaa in pacs table data  {data}")
    return jsonify(data)


# get data for devices 
@app.route('/devices', methods=['GET'])
def devices():
    data_devices=get_devices()
    return jsonify(data_devices)






# add updated data to database for the reportt
@app.route('/pacs_updated', methods=['POST'])
def pacs_updated():
    if request.method == 'POST':
        print("in postttt pacs updatedd")
        data = request.form  # Retrieve form data
        data=data.to_dict()
        upd=update_pacs(data)
        print(f"the updated pacs is {upd}")



        return redirect('/pacs')
    print("here in gettt in pacs")
    return redirect('/pacs')





@app.route('/view_images', methods=['GET' , 'POST'])
def view_images():
    print("inn viewwww imagessssssss")
    data = request.form  # Retrieve form data
    data=data.to_dict()
    print(f"data get from vies scannn is {data}")

    scan_id =  data['scan'] # Example scan_id, replace with your logic to retrieve the correct scan_id
  
    folder_path = os.path.join(BASE_DIR, str(scan_id))
    image_urls = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_urls.append(url_for('serve_image', filename=f'{scan_id}/{filename}'))

    print(f"the urlss {image_urls}")

 # Assuming you have a function to generate CSRF token
    csrf_token = generate_csrf()  # Assuming you have a function to generate CSRF token
    return jsonify({ 'image_urls': image_urls, 'csrf_token': csrf_token})

# ///////////////////

@app.route('/update_patient_acc', methods=['POST'])
def update_patient_data():
            print("hereeeeeee")
            update_data = request.form.to_dict() 
            print(dict(update_data))
            
            return jsonify(update_data)
    

@app.route('/update_radiologists_tablee',methods=['post'])
def update_radiologists_tablee():

        if request.method == 'POST':
            print("in postttt update_radiologists_tablee updatedd")
            data = request.get_json()
            print(data)
            the_corr_data=get_all_data_tssts(data)
            print(the_corr_data)

            tst=get_updates(the_corr_data , data)
            print(tst)
           
            return jsonify(data)























# /////////////////////////////
# adminnnnnnn

@app.route("/send_patient_table",  methods=['GET'])
def send_patient_table():

    tst=get_all_patient_status(session.get('patient'))
    print(f"dataaa of patientttt is {tst}")
    if len(tst) == 0  :
       print("emptyy data ")
       return []
    else :
      return jsonify(tst)
    



@app.route('/doctor_table', methods=['GET'])
def doctor_table():
    data=get_employee_table_admin('Physician')

    return jsonify(data)



@app.route('/radiologist_table', methods=['GET'])
def radiology_table():
    data=get_employee_table_admin('radiologist')
    return jsonify(data)



@app.route('/clinical_table', methods=['GET'])
def clinical_table():
    data=get_employee_table_admin('clinical_eng')
    print(f"data of engg ")
    return jsonify(data)




@app.route('/receptionist_table', methods=['GET'])
def receptionist_table():
    data=get_employee_table_admin('receptionist')
    print(f"data of reccc is")
    return jsonify(data)



@app.route('/HR_table', methods=['GET'])
def HR_table():
    data=get_employee_table_admin('HR')
    print(f"data of reccc is")
    return jsonify(data)


@app.route('/Manager_table', methods=['GET'])
def Manager_table():
    data=get_employee_table_admin('manager')
    print(f"data of reccc is")
    return jsonify(data)







@app.route('/patient_admin_table', methods=['GET'])
def patient_admin_table():
    data=get_patient_table_admin()

    return jsonify(data)



@app.route('/device_admin_table', methods=['GET'])
def device_admin_table():
    data=get_device_table_admin()
    return jsonify(data)

@app.route('/branch_admin_table', methods=['GET'])
def branch_table():
    data=get_branch_table_admin()
    return jsonify(data)


















@app.route('/upload_scan', methods=['POST'])
def upload_scan():
    print("in uploadd _scann ")
    print(dict(request.form))
    global folder_paths
    scan_id = 2 # Example of scan_id, you may generate this dynamically
    folder_path = request.files.getlist('scan_folder')
    upload_directory = os.path.join("E:\\Med_ray\\Cancer_Mediastinal_window\\test", str(scan_id))
    os.makedirs(upload_directory, exist_ok=True)
    
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    
    for file in folder_path:
        filename = secure_filename(file.filename)
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            file_path = os.path.join(upload_directory, filename)
            file.save(file_path)
            print(f"Saved file: {file_path}")

    # folder_paths.append(upload_directory)  # Append the directory path, not folder_path
    print(upload_directory)
    return redirect('test_upload')









@app.route('/images/<path:filename>')
def serve_image(filename):
    # Construct the full file path
    file_path = os.path.join(BASE_DIR, filename.replace('/', '\\'))

    # Check if the file exists
    if os.path.exists(file_path):
        return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))
    else:
        return 'Image not found'













    
@app.route('/homehr',methods=['POST', 'GET'])
def homehr( ):
   csrf_token = generate_csrf()
   print(f"in loginn gett csrf {csrf_token}")
   return render_template('homehr.html',csrf_token=csrf_token)





# //////////////////////////////////////////CHARTSSSS ////////////////////////////////////////

@app.route('/num_malfunctions_per_device' , methods=['GET' , 'POST'])
def num_malfunctions():

    devices = num_malfunctions_per_device()
    return jsonify(devices)


@app.route('/api/maintenance_per_device', methods=['GET' , 'POST'])
def maintenance():
    maintenances = maintenance_per_device()
    return jsonify( maintenances)

@app.route('/installation_date_distribution', methods=['GET' , 'POST'])
def installation():
    installations_tst = installation_date_distribution()
    return jsonify( installations_tst)

@app.route('/api/devices_near_warranty_expiry', methods=['GET' , 'POST'])
def devices_near():
 
    near_expiry =devices_near_warranty_expiry()
    return jsonify( near_expiry)







@app.route('/gender-doctor')
def gender():
    conn = gender_distribution('Physician')

    return jsonify(conn)


@app.route('/payment-doctor')
def payment_type_distribution():
    conn = payment_distribution('Physician')
    print(conn)
    return jsonify(conn)



@app.route('/salary-doctor')
def salary():
    conn = salary_distribution('Physician')
    print(conn)
    return jsonify(conn)


@app.route('/technique-doctor')
def technique_distribution():
    conn = tech_distribution('Physician')
    
    return jsonify(conn)






@app.route('/gender-radiology')
def gender_rad():
    conn = gender_distribution('radiologist')

    return jsonify(conn)



@app.route('/payment-radiology')
def payment_rad():
    conn = payment_distribution('radiologist')
    print(conn)
    return jsonify(conn)



@app.route('/salary-radiology')
def salary_rad():
    conn = salary_distribution('radiologist')
    print(conn)
    return jsonify(conn)

@app.route('/technique-radiology')
def technique_rad():
    conn = tech_distribution('radiologist')
    print(conn)
    return jsonify(conn)



# /////////////////////

# @app.route('/gender-receiptionist')
# def gender_():
#     conn = gender_distribution('')

#     return jsonify(conn)


# @app.route('/age_')
# def gender_():
#     conn = age_distribution('')

#     return jsonify(conn)



# @app.route('/salary-')
# def salary_():
#     conn = salary_distribution('')
#     print(conn)
#     return jsonify(conn)


# ////////////////////

# @app.route('/gender-receiptionist')
# def gender_():
#     conn = gender_distribution('')

#     return jsonify(conn)


# @app.route('/age_')
# def gender_():
#     conn = age_distribution('')

#     return jsonify(conn)



# @app.route('/salary-')
# def salary_():
#     conn = salary_distribution('')
#     print(conn)
#     return jsonify(conn)




# //////////////////////

@app.route('/gender-receiptionist')
def gender_rse():
    conn = gender_distribution('receiptionist')

    return jsonify(conn)


@app.route('/age_receiptionist')
def age_res():
    conn = age_distribution('receiptionist')

    return jsonify(conn)



@app.route('/salary-receiptionist')
def salary_res():
    conn = salary_distribution('receiptionist')
    print(conn)
    return jsonify(conn)




# ///////////////////////////

@app.route('/gender-manager')
def gender_man():
    conn = gender_distribution('manager')
    print(conn)
    return jsonify(conn)


@app.route('/age_manager')
def age_man():
    conn = age_distribution('manager')
    print(f" age  {conn}")
    return jsonify(conn)



@app.route('/salary-manager')
def salary_man():
    conn = salary_distribution('manager')
    print(f" salaryyy {conn}")
    return jsonify(conn)




# /////////////////////////////////

@app.route('/gender-clinical_eng')
def gender_clin():
    conn = gender_distribution('clinical_eng')

    return jsonify(conn)


@app.route('/age_clinical_eng')
def age_clin():
    conn = age_distribution('clinical_eng')
    print(f"ageee {conn}")
    return jsonify(conn)



@app.route('/salary-clinical_eng')
def salary_clin():
    conn = salary_distribution('clinical_eng')
    print(conn)
    return jsonify(conn)


# /////////////////////
@app.route('/gender-hr')
def gender_hr():
    conn = gender_distribution('HR')
    print(conn)
    return jsonify(conn)


@app.route('/age_hr')
def age_hr():
    conn = age_distribution('HR')
    print(conn)
    return jsonify(conn)



@app.route('/salary-hr')
def salary_hr():
    conn = salary_distribution('HR')
    print(conn)
    return jsonify(conn)



@app.route('/logoutfront')
def logoutfront():
    # Clear the session data
    session.pop('receptionist')
    # Redirect to the login page or home page
    return redirect(url_for('login'))



@app.route('/logoutpatient')
def logoutpatient():
    # Clear the session data
    session.pop('patient')
    # Redirect to the login page or home page
    return redirect(url_for('login'))




@app.route('/logoutrad')
def logoutrad():
    # Clear the session data
    session.pop('radiologist')
    # Redirect to the login page or home page
    return redirect(url_for('login'))

@app.route('/logoutpacs')
def logoutpacs():
    # Clear the session data
    session.pop('Physician')
    # Redirect to the login page or home page
    return redirect(url_for('login'))



@app.route('/logoutadmin')
def logoutadmin():
    # Clear the session data
    session.pop('admin')
    # Redirect to the login page or home page
    return redirect(url_for('login'))
































# @app.route('/api/devices_per_branch')
# def devices_per_branch():

#     branches = conn.execute('SELECT device_branch, COUNT(device_sn) as device_count FROM device GROUP BY device_branch').fetchall()

#     return jsonify([dict(branch) for branch in branches])



@app.route('/tst',methods=['get'])
def tst():
   csrf_token=generate_csrf()
   return render_template('/tst.html' , csrf_token=csrf_token)





@app.route('/doctor_charts',methods=['get'])
def doctor_charts():
   csrf_token=generate_csrf()
   data=session.get('admin')
   return render_template('/doctor_charts.html',data =data, csrf_token=csrf_token)


@app.route('/radiology_charts',methods=['get'])
def rad_charts():
   csrf_token=generate_csrf()
   data=session.get('admin')
   print(f"data of admin {data}")
   return render_template('/radiology_charts.html' , data=data ,csrf_token=csrf_token)





@app.route('/manager_charts',methods=['get'])
def man_charts():
   csrf_token=generate_csrf()
   data=session.get('admin')
   return render_template('/manager_charts.html' , data =data,csrf_token=csrf_token)



@app.route('/clinical_charts',methods=['get'])
def clinc_charts():
   csrf_token=generate_csrf()
   data=session.get('admin')
   return render_template('/clinical_charts.html' , data =data,csrf_token=csrf_token)


@app.route('/hr_charts',methods=['get'])
def hr_charts():
   csrf_token=generate_csrf()
   data=session.get('admin')
   return render_template('/hr_charts.html' , data =data,csrf_token=csrf_token)



@app.route('/device_charts',methods=['get'])
def device_charts():
   csrf_token=generate_csrf()
   data=session.get('admin')
   return render_template('/device_charts.html' , data =data,csrf_token=csrf_token)





if __name__ == '__main__':
    app.run(debug=True)

