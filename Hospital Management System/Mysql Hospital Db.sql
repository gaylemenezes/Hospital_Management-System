use hospital;
truncate table patient;
truncate table doctors;
truncate table staff;
select * from doctors;
select * from staff;
select * from patient;
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    appointment_date DATE,
    appointment_time TIME,
    doctor_id INT,  
    status VARCHAR(20), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO appointments (patient_name, appointment_date, appointment_time, doctor_id, status)
VALUES ('John Doe', '2025-05-18', '10:00:00', 1, 'scheduled'),
       ('Jane Smith', '2025-05-18', '11:00:00', 1, 'scheduled');
INSERT INTO appointments (patient_name, appointment_date, appointment_time, doctor_id, status)
VALUES('Dennis Richie', '2025-05-19', '10:00:00', 1, 'scheduled'),
       ('Maria Goldwin', '2025-05-19', '11:00:00', 1, 'scheduled'),
       ('Frank Alice', '2025-05-19', '11:30:00', 1, 'scheduled'),
       ('Steve Cook', '2025-05-20', '10:00:00', 1, 'scheduled'),
       ('Anthony Vase', '2025-05-20', '11:00:00', 1, 'scheduled');
select * from appointments;
describe patient;
describe appointments;
alter table appointments Add column patient_id INT;
alter table appointments
add constraint fk_patient
foreign key(patient_id) references patient(id),
add constraint fk_doctor
foreign key(doctor_id) references doctors(id);
SELECT id FROM patient WHERE id IN (1,2,3,4,5,6,7);
SELECT id FROM doctors WHERE id = 1;

describe patient;


select * from appointments;

update appointments set patient_id =1 where patient_name='John Doe';
update appointments set patient_id =2 where patient_name='Jane Smith';
update appointments set patient_id =3 where patient_name='Dennis Richie';
update appointments set patient_id =4 where patient_name='Maria Goldwin';
update appointments set patient_id =5 where patient_name='Frank Alice';
update appointments set patient_id =6 where patient_name='Steve Cook';
update appointments set patient_id =7 where patient_name='Anthony Vase';
SET SQL_SAFE_UPDATES = 0;

INSERT INTO patient (name, email, phone, password) VALUES 
('Jane Smith', 'jane@gmail.com', '9876543210', 'password123'),
('Dennis Richie', 'dennis@gmail.com', '7654321980', 'password123'),
('Maria Goldwin', 'maria@gmail.com', '8765432109', 'password123'),
('Frank Alice', 'frank@gmail.com', '6543210987', 'password123'),
('Steve Cook', 'steve@gmail.com', '5432109876', 'password123'),
('Anthony Vase', 'anthony@gmail.com', '4321098765', 'password123');

UPDATE patient
SET username = 'jane_smith'
WHERE email = 'jane@gmail.com';

UPDATE patient
SET username = 'dennis_ritchie'
WHERE email = 'dennis@gmail.com';

UPDATE patient
SET username = 'maria_goldwin'
WHERE email = 'maria@gmail.com';

UPDATE patient
SET username = 'frank_alice'
WHERE email = 'frank@gmail.com';

UPDATE patient
SET username = 'steve_cook'
WHERE email = 'steve@gmail.com';

UPDATE patient
SET username = 'anthony_vase'
WHERE email = 'anthony@gmail.com';

CREATE TABLE reports(
id int auto_increment primary key,
patient_id int not null,
doctor_id int not null,
report_date date not null,
report_title varchar(255),
report_description text,
foreign key(patient_id) references patient(id),
foreign key(doctor_id) references doctors(id)
);
ALTER TABLE patient ENGINE = InnoDB;
ALTER TABLE doctors ENGINE = InnoDB;
select * from reports