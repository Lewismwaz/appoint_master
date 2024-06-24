<p align="center"> <img src="https://i.imgur.com/OqKSwG3.png" alt="appoint-master-dark" width="55" height="55" style="vertical-align: middle;"><span style="font-size: 28px;">E-Appoint Master</span> </p>

## *Doctor Appointment Management System using Django*
[Appoint Master](https://github.com/Lewismwaz/appoint_master)**©** 2024, All Rights Reserved 
# System Documentation

### OVERVIEW

➢ **Electronic Appoint Master** is a Doctor-Patient Appointments Management System. This system was originally meant for Kenyatta University Health Centre (Organization) - [KUHC](https://www.ku.ac.ke/healthunit/).  


➢ Appoint Master steps in to make things easier for KUHC patients to book an appointment with their doctors. It tries to automate the process of booking doctor appointments from the old-school manual system.

>[!NOTE] 
Appoint Master **only** acts as an **intermediary** between the *patients* and *KUHC*; and thus ***does not go into the details of what happens during the appointments*** (any medical procedures). 


### Users

The system is restricted to:  
➢ **Students**,  
➢ **Staff**, and  
➢ **Doctors** of Kenyatta University - [KU](https://www.ku.ac.ke/). 

>[!NOTE]   
 Any Validation rules used in the system are in compliance with the KU system, such as user IDs. The **Admin** is also a user of the system; probably a member of the staff (but not a staff patient!).  




### Features

#### 1. Account Creation
➢ ***Patients*** (Students & Staff) can create their own Appoint Master account (by filling a registration form), and then get started right away. As for the ***Doctors*** and ***other Admins***, the admin (main) is responsible for creating a customized account for each one of them. 

> [!IMPORTANT]  
All Users can also **delete** their accounts (permanently) if they choose to.


#### 2. Appointments Management  
➢ Patients can ***book*** a doctor appointment, ***cancel*** it and even ***delete*** the appointments. Patients can also ***view*** all their appointments, that is, **Scheduled, Failed, Canceled**, and **Completed**. Doctors can ***view all appointments*** meant for them, for instance, dentists will only see appointments from patients with dental problems. Doctors can also ***close*** an appointment once it's completed. Admins can ***view*** and ***manage all appointments***; they can ***create, cancel, close*** and ***delete*** an appointment.  

>[!NOTE]   
> When looking at details about a specific appointment, the Patient and the Doctor have different page views. For instance, the patient can generate a report about that particular appointment while the doctor can't. The patient can also view their personal details such as *phone number* and *email* used for that appointment; the doctor won't see the patient's *phone number* or *email* when checking details about a specific appointment.


#### 3. Electonic Payments  
➢ Patients can pay for their appointments electronically via the  ***[PayStack API](https://paystack.com/docs/api/)*** by either using their ***M-Pesa*** or ***Visa***. After payment verification, it's only when the appointments can be deemed to be scheduled.  


#### 4. SMTP Mail Service  
➢ Appoint Master is incorporated with the ``send_mail`` service to send relevant emails to the users, based on certain operations. For instance, when patients ***book, pay for, cancel,*** or even ***delete*** an appointment, an email is sent to them. Doctors also get an email notifying them of newly booked or canceled appointments (by patients, meant for them).  


#### 5. One Time Password(OTP) Verification   
➢ OTP (One-Time Password) verification is a security mechanism used to authenticate users and verify their identity. In Appoint Master, this is achieved by the system sending 6-digit codes to **Doctors** and **Admins** via email during login. It's an added layer of security on top of the normal login page, to further validate high-level users.  

>[!NOTE]   
 This feature is not fully implemented (is incomplete). May require addition of time-sensitivity; OTPs to expire after a specific period of time. 


#### 6. User Logging   
➢ Every user's login session is captured by the system. For instance, the admin can trace which user logged into their accounts at what particular time, thus making it easier to account for any issues with the system, by tracing when and where (which user) the problems originated from.


#### 7. Account Deactivation/Activation  
➢ The Admin can deactivate user accounts, upon which the respective users would be locked out of their accounts. The Admin can also activate the accounts back, upon which the relevant users can now have access to their accounts (unlocked).


#### 8. Next-of-Kin  
➢ Patients can add information regarding their next-of-kin, and the next-of-kin are linked to those particular patients. Therefore, if for instance the patient account (with next-of-kin) is deleted, their next-of-Kins are also deleted along with it.   

>[!NOTE]   
 This feature is not fully implemented (is incomplete). May require addition of next-of-kin actions in the system such as appointment booking. 


#### 9. Reports Generation  
➢ The system can be used to generate reports for patient appointments and payments. Admins can generate reports of all payments and appointments for all the patients. Patients can generate a report of a specific appointment, and all their payments too.

>[!NOTE]   
 This feature is not fully implemented (is incomplete). May need to be customized based on various dates and time.


#### 10. Data Analytics  
➢ The system can show real data analytics (statistically) of appointments [Booked, Scheduled, Failed, Canceled, Completed, Closed], Payments [Mpesa transactions] and Active/Registered Patients [Student Cover, MediCare Cover-Staff]. See the screenshot below (Admin, Patient, & Doctor Dashboard).  

![analytics-admin](https://i.imgur.com/j5jauE0.png)
![patient-dashboard-analytics](https://i.imgur.com/TseCEaM.png)
![doctor-dashboard-analytics](https://i.imgur.com/KFA7Viv.png)


#### 11. Flexible Patient ID registration   
➢ It is possible to create new patient IDs (by Admin), which are initially set to unregistered. These IDs are linked to the registration system, where by registration is only possible for IDs already in the system. Once the patient fills the registration form successfully, the ID (which was initially unregistered) becomes registered under that user. Any attempt to create an account with same ID is revoked by the system.   

>[!IMPORTANT]   
> If an account of a registered user is deleted, the user ID remains in the database, but the ID's status now changes from registered to unregistered; a new user can now register with that ID (again). 




## SCREENSHOTS  
### Homepage  
![home1](https://i.imgur.com/C8WxVsV.png)![home2](https://i.imgur.com/UkAHAYE.jpeg)![home3](https://i.imgur.com/p0p9Gkb.png)![home4](https://i.imgur.com/8yMnNaI.png)![home5](https://i.imgur.com/3hwj34h.png)![home6](https://i.imgur.com/CZr1yOm.png)

### Account Login  
![User-login](https://i.imgur.com/bulZQOQ.png)

### 1. Patients  
#### Registration  
![Patient-registration](https://i.imgur.com/ttCATae.png)

#### Terms & Conditions  
![Terms-conditions](https://i.imgur.com/o9PIXrS.png)

#### Patient Login (Student)  
![Student-patient-login](https://i.imgur.com/cwHoc1r.png)

#### Reset Password  
##### Forgotten Password-Email  
![Reset-email](https://i.imgur.com/a7tFhEk.png)

>[!IMPORTANT]  
>You have to enter an existing email; already registered in the database, otherwise it won't work.

##### Reset success!
![reset-done](https://i.imgur.com/YfNspex.png)

##### Reset link (Email)  
![reset-email-link](https://i.imgur.com/Bq6RlCm.png)

##### Password Reset Page  
![password-reset-page](https://i.imgur.com/e7jVMMc.png)

##### Reset Complete  
![reset-complete](https://i.imgur.com/gLXlLuV.png)

##### Expired Reset Link  
![expired-link](https://i.imgur.com/ZK9AVgD.png)

#### Student Dashboard - No appointments (Dark mode)  
![student-dashboard-dark](https://i.imgur.com/D33qcif.png)

#### Student Dashboard - with appointments (Dark mode)
![student-dashboard-dark&](https://i.imgur.com/TseCEaM.png)

#### Student Dashboard - with appointments (Light mode)  
![student-dashboard-light&](https://i.imgur.com/4L0jKAh.png)

#### Student Profile Update
![student-profile](https://i.imgur.com/Ssx6oy3.png)

#### Student (Next-of-kin) Profile Update  
![next-of-kin](https://i.imgur.com/qjopYZx.png)

#### Appointment Booking  
##### Registration Page  
![appoint-registration](https://i.imgur.com/pVIQajc.png)
![appoint-booking-select-area](https://i.imgur.com/NXvujp6.png)
![appoint-booking-select-date](https://i.imgur.com/R58dcJW.png)

##### Registration Failed!  
![reg-failed1](https://i.imgur.com/3u12Ryw.png)
![reg-failed2](https://i.imgur.com/6NYXYXx.png)
![reg-failed3](https://i.imgur.com/63wMBLw.png)

##### Initiate Payment  
![initiate-payment](https://i.imgur.com/mMqjLmb.png)

##### Initiate Payment>Confirmed  
![initiate-payment-confirmed](https://i.imgur.com/sqsYhFc.png)

##### Initiate Payment>Accepted  
![initiate-payment-accepted](https://i.imgur.com/1gVZFvB.png)

##### Checkout Page  
![checkout-page](https://i.imgur.com/7Xsfjww.png)

##### Checkout Page> Enter Mpesa PIN on your Phone  
![Enter-mpesa-pin](https://i.imgur.com/FjWNaOT.png)
![mpesa-message](https://i.imgur.com/zDia6HV.jpeg)

##### Payment successful!  
![payment-success](https://i.imgur.com/dg9fsu7.png)

#### Payments  
##### View all your Payments
![student-view-payments](https://i.imgur.com/zdAQs02.png)

##### Payments Report  
![student-payments-report](https://i.imgur.com/54iH7aY.png)

#### Appointments  
##### View all Appointments  
![view-all-student-appointments](https://i.imgur.com/kzAsZQ0.png)

##### Manage all Appointments  
![manage-appointments](https://i.imgur.com/paga3xM.png)

##### View Appointment Details> by Appoint ID
![appoint-id-details](https://i.imgur.com/exK9l5h.png)

##### Appointment Report (by Appoint ID)  
![appointment-report-by-id](https://i.imgur.com/ONS6iIw.png)

#### Delete User Account Permanently!
![Delete-user-account-permanently](https://i.imgur.com/Z02z19n.png)


### 2. Admin  
#### Account Login  
##### Login Page  
![admin-login-page](https://i.imgur.com/KK1k6Yu.png)
![admin-login-failed](https://i.imgur.com/GEO3Kh1.png)

##### OTP Verification (if Login is successful)
![admin-otp-verification](https://i.imgur.com/T0z7x7l.png)
![otp-email](https://i.imgur.com/i19dpHV.png)
![otp-ver-failed](https://i.imgur.com/SV9rac1.png)

>[!TIP]
>You can directly log in as Admin (*Jazzmin Dashboard*) without the whole OTP verification by using the link "http://127.0.0.1:8000/admin/". You'll get the a different login page(as below) where you'll be prompted to enter your *Username* and *Password*; and that's it! You're logged in. Once logged in, you can navigate to the *Main Dashboard* (See other screenshots below).

![jazzmin-login](https://i.imgur.com/9k3JNyK.png)

#### Admin Dashboard(s)  
##### (a) Main Dashboard  
![admin-dash-dark](https://i.imgur.com/j5jauE0.png)
![admin-dash-light](https://i.imgur.com/A86Pj3z.png )

##### (b) Jazzmin Dashboard  
![jazzmin-dashboard](https://i.imgur.com/9vZDwhj.png)

>[!IMPORTANT]
>To access the Jazzmin dashboard, click the "**Dashboard**" button (top-left of the *Main Dashboard*). To go back to the *Main Dashboard*, click the "**Back to Site**" link (top-left-near-center of the *Jazzmin Dashboard*).


#### Admin Profile Update  
![update-profile](https://i.imgur.com/m8gpp2X.png)


#### View All Appointments  
![admin-view-all-appointments](https://i.imgur.com/1PzxuGK.png)

##### All Appointments Report  
![all-appointments-report-pdf](https://i.imgur.com/bwtXrfD.png)

#### Manage all Appointments  
![manage-all-appointments](https://i.imgur.com/lazap0j.png)
![manage-all-appoints-jazzmin](https://i.imgur.com/CPAYYr3.png)

#### View all Payments  
![admin-all-payments](https://i.imgur.com/rRrTTjl.png)

#### View all Payments Report  
![all-payments-report](https://i.imgur.com/199WyRd.png)

#### Manage all Payments  
![all-payments-manage](https://i.imgur.com/Zt22Z2B.png)

#### Manage all Users  
![manage-all-users](https://i.imgur.com/uWaPoZp.png)
![deactivate-users](https://i.imgur.com/o7TqKPN.png)

#### Doctor Registration  
![doctor-reg](https://i.imgur.com/QWxTd4X.png)


#### Admin registration  
![admin-registration](https://i.imgur.com/gK91v2r.png)

#### OTP Login History  
![otp-login-history](https://i.imgur.com/239mHcH.png)

#### Patient IDs  
![patient-ids](https://i.imgur.com/VLS2gur.png)
![patient-ids-staff](https://i.imgur.com/i8xLsJo.png)
![patient-ids-student](https://i.imgur.com/grWSpLC.png)


### 3. Doctors  
#### Doctor Login details (Email from Admin)  
![doctor-registered-email](https://i.imgur.com/Yi1kEhQ.png)

#### Login  
![doctor-login](https://i.imgur.com/EK1ztH9.png)
![doctor-invalid-login-creds](https://i.imgur.com/GEO3Kh1.png)

##### OTP Verification  
![otp-verify-doctor](https://i.imgur.com/qtPg7k3.png)
![otp-verification-email](https://i.imgur.com/9tgEC4Y.png)

### Doctor Dashboard  
##### Dark Mode
![doctor-dashboard-dark1](https://i.imgur.com/KFA7Viv.png)
![doctor-dashboard-dark2](https://i.imgur.com/rk1oJz3.png)

##### Light Mode  
![doctor-dashboard-light1](https://i.imgur.com/9GaBAJL.png)
![doctor-dashboard-light2](https://i.imgur.com/DjvjHNR.png)  

### Doctor Emails  
##### New Appointment
![doctor-email-new-appointment](https://i.imgur.com/4tScJ5Z.png)

##### Canceled Appointment  
![canceled-appointment-doctor-email](https://i.imgur.com/3hPMTBz.png)

##### Closed Appointment  
![closed-appointment-doctor](https://i.imgur.com/ImkU8Py.png)


### Doctor Profile Update  
![doctor-profile-update](https://i.imgur.com/khhMR1O.png)

### Manage Appointments  
![doctor-manage-appointment](https://i.imgur.com/GKzHXuC.png)  

### View Closed Appointments  
![view-closed-appointments](https://i.imgur.com/3jhlhGW.png)

### View Appointment Details>by Appoint ID  
![view-appointment-by-id-doctor](https://i.imgur.com/SEYlwV1.png)

### Close Appointment  
![doctor-close-appointment](https://i.imgur.com/RbaFOgc.png)



## INSTALLATION  

### Prerequisites  

>[!IMPORTANT]
Ensure that you've installed the dependencies below, before continuing to the next part. If you already installed them, you may skip this part.  

```
Python 3.12.3 (+)
Pip
Node.js and npm (for managing Tailwind CSS)
Visual Studio(VS) Code
```

>[!NOTE]
>This project is implemented on a Windows 11 Operating System (OS).


#### Useful links  

1. Download **Python** (Latest version): https://www.python.org/downloads/  
2. Download the Pip file: https://bootstrap.pypa.io/get-pip.py  
➢ More details about pip: https://pip.pypa.io/en/stable/installation/

![Pip installation](https://i.imgur.com/iG4RV83.png)

3. Node.js installer: https://nodejs.org/en/download/prebuilt-installer  
4. VS Code: https://code.visualstudio.com/download
5. Tailwind CSS installation Guide: [Worth understanding how to install!](https://django-tailwind.readthedocs.io/en/2.3.0/installation.html)

> [!TIP]
> You need to add the installed tools (*Python, Node.js & npm, VS Code*) to PATH. Check out guide [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).





### Getting Started  

➢ Download the Project by either:
1. Using the direct GitHub download link: https://github.com/Lewismwaz/appoint_master/archive/refs/heads/main.zip 
   or 
2. Typing the command below on the terminal. ([Git](https://www.git-scm.com/downloads) must be installed in your system!)  
   
```
   git clone https://github.com/Lewismwaz/appoint_master.git  
```


##### SMTP Server setup>Email
➢ Open the downloaded project folder(appoint_master). Right-click and select the option ***Open with VS Code***.   Click on the explorer (on the left) then navigate to: ***appoint→settings.py***

➢ Set up your default email for Django: [Django SMTP Server setup Guide](https://medium.com/django-unleashed/configuring-smtp-server-in-django-a-comprehensive-guide-91810a2bca3f)  

> [!IMPORTANT]
>You need to replace your email credentials in the *settings.py* file, as shown below. Find the email configuration in (***line 12-20***)

![Django Email Settings](https://i.imgur.com/caGebc0.png)

Check out the implementation below, using 'gmail' email-provider: 

>[!CAUTION]
> The email credentials **EMAIL_HOST_USER**, and **EMAIL_HOST_PASSWORD** below are not real! You need to replace them with your actual credentials. They're only just for demonstration.

```python
# settings.py

# SMTP Email Backend setup
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'janedoe@gmail.com'
EMAIL_HOST_PASSWORD = 'aksn wygf viyp gloh'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```




##### PayStack API setup>Payment 
➢ Set up your *private* and *public* **PayStack API Keys**:  

>[!WARNING]
> The PayStack payment API used in this project is tailored for people in Kenya (M-Pesa users) only. It won't work for other countries, unless of course by modifying the payment code (Located: .\appoint_master\payments).

>[!IMPORTANT]
> You have to **create** a verified PayStack account in order to get access to the live keys (private and public), in order for payment to work. Create a PayStack account [here](https://paystack.com/ke/?q=/).  When done, log into your account. Navigate to *Settings/ApI Keys & Webhooks/*, then **copy** the *Live Secret Key* and *Live Public Key*. Ensure that live is turned on (As shown below)

![PayStack API Keys](https://i.imgur.com/99Z8jwK.png)

➢ Paste the live keys you copied, inside the *settings.py* file ***(line 156-158)***, as shown below:  

```python
# PayStack API keys
PAYSTACK_SECRET_KEY = 'sk_live_7d72f71bdeb47084024e5f7d0ba1kbbc15fd6895'
PAYSTACK_PUBLIC_KEY = 'pk_live_fdc16c020d620652ad9d948e5ceda61de4e485e7'

```

>[!CAUTION]
>These are not real keys. They're only just for demonstration! Replace them with your actual keys.





##### Virtual Environment setup>venv  
➢ Inside VS Code, *open terminal*.   

>[!TIP]
>Use shortcut (**Control+Shift+~**).

➢ Install your virtual environment (venv) using the command below:  

```
python -m venv venv
```




##### Venv Activation  
➢ In the terminal, activate the virtual environment using the command below:  

```psh
.\venv\Scripts\Activate.ps1

```

You should now see the (venv) before the path to the current directory (as shown below):  

![venv: Active](https://i.imgur.com/tMNcrnZ.png)

>[!IMPORTANT]
>Always ensure you activate the virtual environment (venv) before starting the server, otherwise you'll get tracebacks in the project files and also the terminal. To deactivate the venv, run the command *deactivate* on the terminal. 


##### Project Requirements 
➢ Next, you need to install all the requirements below:  

```
aiohttp==3.9.3

aiohttp-retry==2.8.3

aiosignal==1.3.1

amqp==5.2.0

arabic-reshaper==3.0.0

arrow==1.3.0

asgiref==3.7.2

asn1crypto==1.5.1

attrs==23.2.0

Babel==2.14.0

beautifulsoup4==4.12.3

billiard==4.2.0

binaryornot==0.4.4

Brotli==1.1.0

cairocffi==1.7.0

celery==5.3.6

certifi==2023.11.17

cffi==1.16.0

chardet==4.0.0

charset-normalizer==3.3.2

click==8.1.7

click-didyoumean==0.3.0

click-plugins==1.1.1

click-repl==0.3.0

colorama==0.4.6

cookiecutter==2.5.0

crispy-bootstrap4==2024.1

crispy-bootstrap5==2024.2

cryptography==42.0.5

cssselect2==0.7.0

Django==5.0.1

django-browser-reload==1.12.1

django-crispy-forms==2.1

django-jazzmin==2.6.0

django-phonenumber-field==7.3.0

django-tailwind==3.8.0

django-widget-tweaks==1.5.0

djangorestframework==3.15.0

et-xmlfile==1.1.0

fonttools==4.53.0

frozenlist==1.4.1

html5lib==1.1

idna==2.10

Jinja2==3.1.3

kombu==5.3.5

lxml==5.1.0

markdown-it-py==3.0.0

MarkupSafe==2.1.4

mdurl==0.1.2

multidict==6.0.5

numpy==1.26.4

openpyxl==3.1.2

oscrypto==1.3.0

pandas==2.2.1

phonenumbers==8.13.30

pillow==10.2.0

prompt-toolkit==3.0.43

pycparser==2.21

pydyf==0.10.0

Pygments==2.17.2

pyHanko==0.23.0

pyhanko-certvalidator==0.26.3

PyJWT==2.8.0

pypdf==4.1.0

pyphen==0.15.0

pypng==0.20220715.0

python-bidi==0.4.2

python-dateutil==2.8.2

python-docx==1.1.0

python-slugify==8.0.1

pytz==2024.1

PyYAML==6.0.1

qrcode==7.4.2

reportlab==4.0.9

requests==2.31.0

rich==13.7.0

six==1.16.0

soupsieve==2.5

sqlparse==0.4.4

svglib==1.5.1

text-unidecode==1.3

tinycss==0.4

tinycss2==1.3.0

types-python-dateutil==2.8.19.20240106

typing_extensions==4.10.0

tzdata==2023.4

tzlocal==5.2

uritools==4.0.2

urllib3==1.26.18

vine==5.1.0

wcwidth==0.2.13

webencodings==0.5.1

xhtml2pdf==0.2.15

yarl==1.9.4

zopfli==0.2.3
```

➢ Use the command below to install all the requirements:  

```
pip install -r requirements.txt
```


##### Jazzmin Dashboard setup>Admin UI  
Copy the *base.html* file (Located: *appoint_master→Resources*), paste and replace it inside: **venv→Lib→site-packages→jazzmin→templates→admin**. 



### Migrations

➢  For the system to function, it needs a database (db.sqlite3), which does not exist at the moment. To create one, you need to make migrations to save, synch and format for instance, the SMTP server and PayStack settings, done earlier. Run the following commands in order:  

```
python manage.py makemigrations account
python manage.py migrate account
python manage.py makemigrations payments
python manage.py migrate payments
python manage.py migrate
```


### Superuser/Admin  
➢ To establish overall control over the system, an administrator is required. To create one, use the command below:  

```
python manage.py createsuperuser
```

You should get something like this (below):

![create-superuser](https://i.imgur.com/fzqIemI.png)


### Starting Server  
➢ To access the system, you need to run the server. This can be achieved by **opening two separate terminals**, then typing the two commands below (one per terminal):  

>[!TIP]
>To open a new (separate) terminal, click the plus(+) icon on your terminal window's top-right(See screenshot below)

```
python manage.py runserver
python manage.py tailwind start
```

You should get something like this (below):  

![Start-Server](https://i.imgur.com/c2PiiB9.png)

> [!IMPORTANT]
> Ensure that the venv is activated before running the 2 commands; in both terminals.

>[!NOTE]
>The Timezone used for this project is "Africa/Nairobi". For users from other regions, it is recommended to replace this with your own Timezone (*Settings.py line 130*).

### Accessing the site  
➢ To view the Appoint Master site, simply:
1. Press **Control+Click** in your terminal where there is "http://127.0.0.1:8000/"  
   or
2. Select, copy (*Control+C*), paste (*Control+V*) the link "http://127.0.0.1:8000/" into your browser, then press Enter.  

>[!IMPORTANT]
>Ensure you are connected to the internet when accessing the site; to load icons and also to be able to send/receive emails.


## Usage  

>[!IMPORTANT]
>Before anything else, log into the admin account, and create a couple of Patient (Student & Staff) IDs. Patients can't register themselves with the system if they're not recognized already, and thus this would make things easier when it comes to validating new users wanting to register, who are not students/staff. The video demo will come in handy. See implementation [here](https://drive.google.com/file/d/1eJhNkD0zOJYs890b8l1vtAldX9GkB4Oe/view?usp=drivesdk)

1. Open your browser and go to `http://127.0.0.1:8000/`.
2. Register yourself as a patient using your institution ID (Staff/Student). Reset password by selecting "forgotten password". For doctors and other admins, the admin creates their account, then the login credentials (username & password) are automatically sent to them (via email).
3. Log into Appoint Master Dashboard (if you already registered); enter username and password[Direct login for Patients only]. For Admins and Doctors, OTP Verification is required.
4. As an admin, you can manage users, patient IDs, OTP login History, payments and appointments from the admin panel. You can also generate reports for all user appointments and payments.
5. As a doctor, you can view and manage (close) your appointments.
6. As a patient, you can schedule/create, pay for, cancel, view and delete your appointments. You can also generate reports for a specific appointment and even for all your payments.

>[!CAUTION]
>All users have an option to delete their account PERMANENTLY! If they so choose to do that, then, everything about them in the system is permanently deleted.


## Video Demo of the system  

>[!NOTE]
>To see a full implementation of the system, click [here](https://drive.google.com/file/d/1eJhNkD0zOJYs890b8l1vtAldX9GkB4Oe/view?usp=drivesdk)


## Technologies used

- **Backend:** Django
- **Frontend:** HTML, CSS, Tailwind CSS, JavaScript
- **Database:** SQLite (default, can be changed to PostgreSQL or other databases)
- **Version Control:** Git

## Contributing

Contributions are welcome! Please follow these steps(below) to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License. View License [here.](https://github.com/Lewismwaz/appoint_master/blob/main/MIT%20LICENSE.txt)  

More details about the MIT License can be found [here.](https://choosealicense.com/licenses/mit/)
## Contact

For any inquiries, please contact:

- Email - eappointmaster@gmail.com
- GitHub - [@Lewismwaz](https://github.com/Lewismwaz)  

[Appoint Master](https://github.com/Lewismwaz/appoint_master)**©** 2024, All Rights Reserved
