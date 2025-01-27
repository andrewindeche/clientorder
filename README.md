# Client Order Service

|Tool                | Description                    | Tags for tools used                                                                                               |
| ------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| 1.GitHub| Version Control| [Version-Control]; [Repo]; [Pipeline]; [Continuous integration];[Continuous Delivery]|
| 2.Django Rest API |  Python Based Backend Framework| [python]; [Django];|
| 3.PostgresQl | Relational Database| [Relational Integrity]; [Database];|
| 4.Pipenv | Package/Dependency manager| [Virtual Environment];[Dependency];|
| 5.Ansible |Configuration Automation Tool | [Orchestration];[ configuration management]|
| 6.Terraform | Infrastructure as Code Tool | [IaC]; [Provisioning]; [Cloud Resources];|
| 7.Kubernetes |	Container Orchestration Platform | [Containers]; [Cluster Management]; [Scalability];|
| 8.Africa’s Talking SMS Gateway |	Communication Platform | [SMS]; [API]; [Messaging];|
| 9.OpenID | Connect	Authentication Protocol | [OAuth 2.0]; [Authentication]; [Identity Management];|
| 10.Google Cloud Platform | Infrastructure As A Service | [Cloud Platform]; [Deployment];|
| 11.CircleCI | continuous integration and delivery (CI/CD) Platform | [Continuous integration]; [Continuous Delivery];[CI/CD]|

## <h1> Description</h1>
The aim of the project is to build a DRF(Django Rest Framework) client order service that enables a client to make orders.

## <h1> Set up Instructions</h1>
<p><b>Github</b></p>
<ul>
<li> Download the Zip file from the code tab on github to get the project Zip files (Recommended)</li>
<li> Clone the project using 'git clone https://github.com/andreindeche/clientorderservice.git'.</li>
<li> Unzip the file and add the Project folder to your IDE/Compiler</li>
</ul>

1. Create an .env environment on the Django root folder and add the recessary environment variables. 
Use <b>env.example</b> as a guide for environment variables.

<p><b>Django</b></p>
<p>The project uses pipenv, django and postgresql backend</p>

1. Install pipenv using the command 

```bash
pip install pipenv
```

2. Activate your virtual enviromnment

```bash
pipenv shell 
```

3. Naviagte to your Django project and use  in  the directory path: <b>backend\requirements.txt</b> to install the required django dependencies 

```bash
pipenv install -r requirements.txt
```

4. Create an .env on the Django root folder and add the recessary environment variables. 

Use (backend\env.example) as a guide for environment variables </li>

5. Create a Super User using 

```bash
python manage.py createsuperuser
```

6. Migrate your DB using 

```bash
python manage.py migrate
```

7. To run the project outside of a shell environment use: 

```bash
pipenv run python manage.py runserver
```

 or while in the shell environment use:

```bash
python manage.py runserver
```

<p><b>Africa's Talking</b></p>
<p> Africa's talking has been used as the SMS/Communication gateway for the project to enable SMSes on order or update of the orders.
1. Create an account on the site https://africastalking.com/sms.
2. Generate an api key and set it on the environment variable 'YOUR_API_KEY'.

<p><b>Endpoints</b></p>
<p>Authentication</p>
Authenticate to register as a user and interact with the API Endpoints.
URL = 'http://localhost:8000'

1.Login.
http://{URL}/accounts/login/ or http://{URL}/accounts/google/login/
2.Register
http://{URL}/accounts/signup/

2.Generate Tokens for login:
    Fields: "username", "password",

    POST:/api/token/

    POST:/api/token/refresh/  to refresh token

    ***POST:/accounts/login/: optional will still require tokens

3.Create Order
    POST:http://{URL}/api/create_order/
        Headers: Content-Type: application/json
        Authorization: Add Token
        Json payload:{
        "customer_code": "CUST123",
        "item": "Laptop",
        "amount": 500
        }
4.Update Order
    PUT,PATCH:http://{URL}/api/update_order/<int:pk>/


## <h1> Author </h1>
Built by <b>Andrew Indeche</b>