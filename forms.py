from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *



class login_form(FlaskForm):
    id=StringField("username" ,validators=[data_required()])
    password=PasswordField('password',validators=[data_required()] )






class Register_form(FlaskForm):
    name =StringField('name',validators=[data_required()])
    patient_ssn =StringField('patient_ssn',validators=[data_required()] )
    email =StringField('email' ,validators=[data_required()])
    password = PasswordField('password',validators=[data_required()])
    confirm_password = PasswordField('Confirm Password',validators=[data_required()])
    address=StringField('address',validators=[data_required()])
    age=StringField('username',validators=[data_required()] )
    phone_number = StringField('phone_num',validators=[data_required()])
    gender = StringField('gender',validators=[data_required()])


class Register_emp(FlaskForm):
    name =StringField('name',validators=[data_required()])
    employee_id =StringField('employee_id',validators=[data_required()] )
    email =StringField('email' ,validators=[data_required()])
    password = PasswordField('password',validators=[data_required()])
    confirm_password = PasswordField('Confirm Password',validators=[data_required()])
    address=StringField('address',validators=[data_required()])
    age=StringField('username',validators=[data_required()] )
    phone_number = StringField('phone_num',validators=[data_required()])
    gender = StringField('gender',validators=[data_required()])
    job_title = StringField('job_title',validators=[data_required()])


class offline_appointment(FlaskForm):
    name =StringField('fullname',validators=[data_required()])
    patient_ssn =StringField('username' ,validators=[data_required()])
    patient_ssn =StringField('username' ,validators=[data_required()])
    organ =StringField('organ' ,validators=[data_required()])
    modality =StringField('modality',validators=[data_required()] )
    branch_name =StringField('branch_name',validators=[data_required()] )
    datetime =StringField('branch_name' ,validators=[data_required()])
    address=StringField('address',validators=[data_required()])
    age=StringField('username' ,validators=[data_required()])
    phone_number = StringField('phone_num',validators=[data_required()])
    gender = StringField('Gender',validators=[data_required()])

class online_appointment(FlaskForm):
    organ =StringField('organ',validators=[data_required()] )
    modality =StringField('modality',validators=[data_required()] )
    branch_name =StringField('branch_name',validators=[data_required()] )
    datetime =StringField('branch_name' ,validators=[data_required()])






    #with vaildatorsss
# class Register_form(FlaskForm):
#     name =StringField('fullname' , validators=[data_required() , length(min =3, max =30,message='Username must have at least 3 letters')])
#     patient_ssn =StringField('username' , validators=[data_required() , length(min =3 , max =30,message='Username must have at least 3 letters')])
#     email =StringField('email' , validators=[data_required() , Email(message="invaild Email")])
#     password = PasswordField('password',validators=[DataRequired(), Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$',message='Password must have letters and digits')])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Confirm doesn't match the password")])
#     address=StringField('address', validators=[DataRequired(), Length(min=5, max=30, message="Address must be between 5 and 30 characters")])
#     age=StringField('username' , validators=[data_required() , length(min =3 , max =30,message='Username must have at least 3 letters')])
#     phone_num = StringField('phone_num', validators=[Length(min=11, max=11, message='Phone number must be 11 digits')])
#     gender = StringField('Gender', validators=[DataRequired(), AnyOf(['M', 'F'], message="Invalid gender")])
    #  username=StringField("username" , validators=[DataRequired(), length(min=3 , max=30 , message="Name must be greater than 3 char ")])
    # password=PasswordField('password' ,validators=[DataRequired(), Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$',message='Password must have at least one letter,one number')])
   
