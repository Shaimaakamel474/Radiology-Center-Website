from faker import Faker
import random

fake = Faker()

# Function to generate random time
def random_time():
    hour = random.randint(8, 20)  # assuming 8 AM to 5 PM shift
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02}:{minute:02}:00"

# Generate Branch Data
num_branches = 10
branches_data = []
for i in range(1, num_branches + 1):
    branch_data = {
        'branch_id': i,
        'bname': fake.company(),
        'phone_number': fake.random_number(digits=10),
        'email': fake.company_email(),
        'manager': random.randint(1, 10)  # assuming managers have employee_id from 1 to 10
    }
    branches_data.append(branch_data)

# Generate Device Data
devices_data = [
    (1, 'MRI Machine', 1, '4 Tesla', 'High-Resolution Imaging', 'Neuroimaging'),
    (2, 'CT Scanner', 1, '128-slice', 'Fast Scanning', 'Full-Body Imaging'),
    (3, 'Ultrasound Machine', 2, '4D Imaging', 'High-Frequency Probes', 'Fetal Imaging'),
    (4, 'X-ray Machine', 2, 'Digital Radiography', 'Low Radiation Dose', 'Orthopedic Imaging'),
    (5, 'PET Scanner', 3, 'Time-of-Flight PET', 'Whole-Body Imaging', 'Oncologic Imaging'),
    (6, 'Mammography Machine', 3, 'Digital Mammography', 'Breast Imaging', 'Breast'),
    (7, 'MRI Machine', 4, '3 Tesla', 'Functional MRI', 'Cardiovascular Imaging'),
    (8, 'CT Scanner', 4, '64-slice', 'Low-Dose CT', 'Angiography'),
    (9, 'Ultrasound Machine', 5, 'Portable Ultrasound', 'Point-of-Care Imaging', 'Abdominal Imaging'),
    (10, 'X-ray Machine', 5, 'Fluoroscopy', 'Mobile X-ray', 'Pulmonary Imaging'),
    (11, 'PET Scanner', 6, 'PET-CT', 'Brain Imaging', 'Brain'),
    (12, 'Mammography Machine', 6, '3D Mammography', 'Breast Tomosynthesis', 'Breast'),
    (13, 'MRI Machine', 7, '1.5 Tesla', 'Open MRI', 'Musculoskeletal Imaging'),
    (14, 'CT Scanner', 7, '256-slice', 'Dual-Energy CT', 'Abdominal Imaging'),
    (15, 'Ultrasound Machine', 8, 'Color Doppler Ultrasound', 'Vascular Imaging', 'Echocardiography'),
    (16, 'X-ray Machine', 8, 'C-arm Fluoroscopy', 'Interventional Imaging', 'Surgical Imaging'),
    (17, 'PET Scanner', 9, 'Digital PET', 'Oncology Imaging', 'Metabolic Imaging'),
    (18, 'Mammography Machine', 9, 'Digital Breast Tomosynthesis', 'Breast Cancer Screening', 'Breast'),
    (19, 'MRI Machine', 10, 'Wide Bore MRI', 'Spine Imaging', 'Orthopedic MRI'),
    (20, 'CT Scanner', 10, 'Dual-Source CT', 'Emergency Radiology', 'Trauma Imaging'),
    (21, 'MRI Machine', 1, '3 Tesla', 'Diffusion MRI', 'Neuroimaging'),
    (22, 'CT Scanner', 2, '256-slice', 'Whole-Body CT', 'Trauma Imaging'),
    (23, 'Ultrasound Machine', 3, '3D/4D Ultrasound', 'Gynecological Imaging', 'Obstetrics'),
    (24, 'X-ray Machine', 4, 'Digital Fluoroscopy', 'Pediatric Imaging', 'Orthopedic X-ray'),
    (25, 'PET Scanner', 5, 'FDG-PET', 'Brain PET', 'Brain'),
    (26, 'Mammography Machine', 6, 'Digital Breast Imaging', 'Breast Cancer Detection', 'Breast'),
    (27, 'MRI Machine', 7, 'Open MRI', 'Joint Imaging', 'Musculoskeletal MRI'),
    (28, 'CT Scanner', 8, '128-slice', 'Coronary CT Angiography', 'Cardiac Imaging'),
    (29, 'Ultrasound Machine', 9, 'Transvaginal Ultrasound', 'Pelvic Imaging', 'Reproductive Imaging'),
    (30, 'X-ray Machine', 10, 'Digital Radiography', 'Mobile X-ray', 'Emergency Imaging')
]

# Generate Device Technique Data
device_tech_data = [
    (1, 'Brain'), (2, 'Heart'), (3, 'Liver'), (4, 'Lung'), (5, 'Kidney'),
    (6, 'Pancreas'), (7, 'Intestine'), (8, 'Stomach'), (9, 'Spleen'), (10, 'Brain'),
    (11, 'Heart'), (12, 'Heart'), (13, 'Liver'), (14, 'Lung'), (15, 'Kidney'),
    (16, 'Pancreas'), (17, 'Intestine'), (18, 'Stomach'), (19, 'Spleen'), (20, 'Spleen'),
    (21, 'Brain'), (22, 'Heart'), (23, 'Liver'), (24, 'Lung'), (25, 'Kidney'),
    (26, 'Pancreas'), (27, 'Intestine'), (28, 'Stomach'), (29, 'Spleen'), (30, 'Brain')
]

# Generate Employee Data
num_employees = {
    'receptionist': 20,
    'radiologist': 30,
    'Physician': 50,
    'clinical_eng': 20,
    'HR': 10,
    'manager': 10,
    'admin': 1
}

employees_data = []
employee_id_counter = 1

for job_title, count in num_employees.items():
    for _ in range(count):
        employee_data = {
            'fname': fake.first_name(),
            'lname': fake.last_name(),
            'email': fake.email(),
            'age': random.randint(22, 65),
            'gender': random.choice(['M', 'F']),
            'phone_number': fake.random_number(digits=10),
            'address_city': fake.city(),
            'address_street': fake.street_name(),
            'address_home_no': fake.building_number(),
            'employee_id': employee_id_counter,
            'password': fake.random_number(digits=4),  # example password as 4-digit number
            'job_title': job_title,
            'payment': 'salaried_employee' if job_title != 'Radiologist' else 'scan_employee',
            'salary': random.randint(30000, 120000),
            'pay_scale': random.randint(1, 5),
            'start_shift': random_time(),
            'end_shift': random_time(),
            'img_url': fake.image_url()
        }
        employees_data.append(employee_data)
        employee_id_counter += 1

# Generate SCAN_TYPE Data for Physicians
scan_types_data = []
for employee_id in range(11, 61):  # Assuming employee_id for physicians starts from 11 to 60
    scan_type = random.choice(['MRI', 'CT Scan', 'X-Ray', 'Ultrasound', 'PET Scan'])
    scan_types_data.append({
        'PH_ID': employee_id,
        'SCAN_TYPE': scan_type
    })

# Generate TECHNIQUE Data for Radiologists
techniques_data = []
for employee_id in range(1, 31):  # Assuming employee_id for radiologists starts from 1 to 30
    technique = random.choice(['CT Angiography', 'PET ','Mammography', 'MRI Angiography', 'Ultrasound Imaging'])
    techniques_data.append({
        'R_ID': employee_id,
        'TECHNIQUE': technique
    })

# Generate WORKS_AT Data
works_at_data = []
for employee in employees_data:
    works_at_data.append({
        'employee_id': employee['employee_id'],
        'branch_id': random.randint(1, num_branches)
    })

# Print SQL INSERT Statements

# # BRANCH table
# print("-- INSERT INTO BRANCH (branch_id, bname, phone_number, email, manager) VALUES")
# for branch in branches_data:
#     print(f"({branch['branch_id']}, '{branch['bname']}', '{branch['phone_number']}', '{branch['email']}', {branch['manager']}),")
# print()

# DEVICE table
# print("-- INSERT INTO DEVICE (device_sn, device_name, device_branch, d_data1, d_data2, d_data3) VALUES")
# for device in devices_data:
#     print(f"({device[0]}, '{device[1]}', {device[2]}, '{device[3]}', '{device[4]}', '{device[5]}'),")
# print()

# # DEVICE_TECH table
# print("-- INSERT INTO DEVICE_TECH (device_sn, device_tech) VALUES")
# for tech in device_tech_data:
#     print(f"({tech[0]}, '{tech[1]}'),")
# print()

# EMPLOYEE table
# print("-- INSERT INTO EMPLOYEE (fname, lname, email, age, gender, phone_number, address_city, address_street, address_home_no, employee_id, password, job_title, payment, salary, pay_scale, start_shift, end_shift, img_url) VALUES")
# for employee in employees_data:
#     print(f"('{employee['fname']}', '{employee['lname']}', '{employee['email']}', {employee['age']}, '{employee['gender']}', '{employee['phone_number']}', '{employee['address_city']}', '{employee['address_street']}', '{employee['address_home_no']}', {employee['employee_id']}, {employee['password']}, '{employee['job_title']}', '{employee['payment']}', {employee['salary']}, {employee['pay_scale']}, '{employee['start_shift']}', '{employee['end_shift']}', '{employee['img_url']}'),")
# print()

# SCAN_TYPE table
# print("-- INSERT INTO SCAN_TYPE (PH_ID, SCAN_TYPE) VALUES")
# for scan_type in scan_types_data:
#     print(f"({scan_type['PH_ID']}, '{scan_type['SCAN_TYPE']}'),")
# print()

# # TECHNIQUE table
# print("-- INSERT INTO TECHNIQUE (R_ID, TECHNIQUE) VALUES")
# for technique in techniques_data:
#     print(f"({technique['R_ID']}, '{technique['TECHNIQUE']}'),")
# print()

# # WORKS_AT table
# print("-- INSERT INTO WORKS_AT (employee_id, branch_id) VALUES")
# for works_at in works_at_data:
#     print(f"({works_at['employee_id']}, {works_at['branch_id']}),")
