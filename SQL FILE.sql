CREATE TABLE PATIENT(
    patient_ssn     INT  PRIMARY KEY,
    fname           VARCHAR(32) NOT NULL,
    lname           VARCHAR(32) NOT NULL,
    email           VARCHAR(255),
    password        VARCHAR(32),
    age             INT         NOT NULL,
    gender          CHAR(1)     CHECK ( gender='f' or gender='m' or gender='M' or gender ='F' ) NOT NULL,
    phone_number    INT,
    address_city    VARCHAR(96),
    address_street  VARCHAR(96),
    address_home_no VARCHAR(32), -- many houses' numbers include also characters
    booking_technique VARCHAR(32) CHECK( booking_technique = 'guest' or booking_technique = 'user')
    CHECK (password IS NOT NULL OR booking_technique = 'guest')
);

CREATE TABLE BRANCH(
    branch_id       INT PRIMARY KEY,
    bname           VARCHAR(96) NOT NULL
);

CREATE TABLE DEVICE(
    device_sn       INT PRIMARY KEY,
    device_name     VARCHAR(96) UNIQUE,
    device_branch   INT,
    d_data1         VARCHAR(96),
    d_data2         VARCHAR(96),
    d_data3         VARCHAR(96),
    FOREIGN KEY (device_branch) REFERENCES branch(branch_id)
);

CREATE TABLE DEVICE_TECH(
    device_sn       INT,
    device_tech     VARCHAR(96) PRIMARY KEY,
    FOREIGN KEY (device_sn) REFERENCES device(device_sn)
);

CREATE TABLE REGISTER(
    patient_ssn     INT,
    branch_id       INT,
    date            DATE,
    time            TIME,
    modality        VARCHAR(96),
    organ           VARCHAR(96),
    payment         FLOAT,
    branch_name           VARCHAR(96),
    FOREIGN KEY (patient_ssn) REFERENCES patient (patient_ssn),
    FOREIGN KEY (branch_id)   REFERENCES branch  (branch_id),
    PRIMARY KEY (date,modality,branch_id,time)
);

CREATE TABLE EMPLOYEE(
    fname           VARCHAR(32) NOT NULL,
    lname           VARCHAR(32) NOT NULL,
    email           VARCHAR(255),
    age             INT         NOT NULL,
    gender          CHAR(1)     CHECK ( gender='f' or gender='m' or gender='M' or gender ='F' ) NOT NULL,
    phone_number    INT,
    address_city    VARCHAR(96),
    address_street  VARCHAR(96),
    address_home_no VARCHAR(32), -- many houses' numbers include also characters
    employee_id     INT PRIMARY KEY, --also it is the user for the employee
    password        INT NOT NULL,
    job_title       VARCHAR(96),
    payment         VARCHAR(96)   CHECK( payment = 'salaried_employee' or payment = 'scan_employee'),
    salary          INT,
    pay_scale       INT
);

CREATE TABLE SCAN_TYPE(
    PH_ID   INT,
    SCAN_TYPE VARCHAR(96),
    FOREIGN KEY (PH_ID) REFERENCES EMPLOYEE(employee_id)
);

CREATE TABLE TECHNIQUE(
    R_ID   INT,
    TECHNIQUE   VARCHAR(96),
    FOREIGN KEY (R_ID) REFERENCES EMPLOYEE(employee_id)
);

CREATE TABLE RADIOLOGY_EXAM(
    exam_id         INT PRIMARY KEY,
    patient_ssn     INT,
    verified        VARCHAR(32), --should be boolean but it does not work
    modality        VARCHAR(96),
    organ           VARCHAR(96),
    scan_folder     VARCHAR(1024) UNIQUE,
    report          VARCHAR(1024),
    device_sn       INT,
    employee_id     INT,
    FOREIGN KEY (patient_ssn) REFERENCES patient(patient_ssn),
    FOREIGN KEY (device_sn) REFERENCES device (device_sn),
    FOREIGN KEY (employee_id) REFERENCES employee (employee_id)
);

CREATE TABLE WORKS_AT(
    employee_id     INT,
    branch_id       INT,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);