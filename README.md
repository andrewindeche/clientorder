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
<li> Clone the project using ```bash git clone https://github.com/andreindeche/clientorderservice.git'.```</li>
<li> Unzip the file and add the Project folder to your IDE/Compiler</li>
</ul>

1. Create an .env environment on the Django root folder and add the recessary environment variables. 
<p>Use <b>[env example](./env.example)</b> as a guide for environment variables.</p>

<p><b>Kubernetes</b></p>
<ul>
<li>Create a Docker Image</li>

    ```bash
     docker build -t your-django-project .
    ```
<li>Run the Docker container:</li>

    ```bash
    docker run -p 8000:8000 myproject
    ```

<li>Push image to a container registry</li>

  ```bash
  docker tag my-django-app your-username/my-django-app:latest
  docker push your-username/my-django-app:latest
  ```

<li> Create a configmap.yaml for environment variables</li>
Make sure to define your environment variables in this file.

<li>Apply Kubernetes configuration for your Kubernetes cluster</li>

    ```bash
    kubectl apply -f configmap.yaml
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

<li>If you're testing locally, you can use Minikube to create a local Kubernetes cluster</li>

    ```bash
    minikube start
    ```

    ```bash
    explorer.exe "http://192.168.39.84:30095"
    ```
</ul>

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

3. Naviagte to your Django project and use  in  the directory path: <b>[requirements](./requirements.txt)</b> to install the required django dependencies 
```bash
pipenv install -r requirements.txt
```

4. Create an .env on the Django root folder and add the recessary environment variables. 
Use [example env](backend\env.example) as a guide for environment variables </li>

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

8. To Run Tests (Tests include Security Tests): 
```bash
python manage.py test
```

9.Generate Coverage report

```bash
coverage run --source='.' manage.py test
```
```bash
coverage report
```
```bash
coverage html
```

<p><b>Africa's Talking</b></p>
<p> Africa's talking has been used as the SMS/Communication gateway for the project to enable SMSes on order or update of the orders.
1. Create an account on the site https://africastalking.com/sms.
2. Generate an api key and set it on the environment variable 'YOUR_API_KEY'.

<p><b>Endpoints</b></p>
<ul>
<li>Preferably Use POSTMAN or any API tool to test the endpoints after login.</li>
<li>Orders can only be made by authenticated users.</li>
</ul>

<p><b>Authentication</b></p>
<ul>
<li>Authenticate to register as a user and interact with the API Endpoints.</li>
<li>For logins, click on the link and authenticate on a browser.</li>
URL = 'http://localhost:8000'
</ul>

1.Login.
```bash
http://{URL}/accounts/login/ or http://{URL}/accounts/google/login/
```

2.Register
```bash
http://{URL}/accounts/signup/
```

3.View Customer code:
```bash
http://{URL}/accounts/account_page/
```

4.Logout navigate to:
```bash
http://{URL}/accounts/google/login/
```
Select Logout

5.Generate Tokens for transactions:
    <ul>
   <li> Fields: "username", "password",</li>

    <li>  POST:/api/token/ </li>

     <li> POST:/api/token/refresh/  to refresh token </li>
    </ul>

6.Create Order
```bash
    POST:http://{URL}/api/create_order/
        Headers: Content-Type: application/json
        Authorization: Add Token
        Example:Json payload:{
        "customer_code": "CUST123",
        "item": "Laptop",
        "amount": 500
        }
```

7.Update Order
```bash
   PUT:http://{URL}/api/update_order/<uuid:order_id>/</p>
```
To get UUID via Python shell for ORM :

```bash
    python3 manage.py shell
```
```bash
    from orders.models import Order
    order = Order.objects.first() 
    print(order.order_id)
```
    or start psql:

```bash
    SELECT order_id FROM orders;
```

8. Use GraphQl for querying:
    Navigate to: http://127.0.0.1:8000/graphql/

<p><b>GraphQl Mutations:</p>/<b>

Generate Token.

```bash

mutation {
  generateToken(username: "your_username", password: "your_password") {
    access
    refresh
  }
}


```

<p><b>Refresh Token.</p>/<b>

```bash
mutation {
  refreshToken(refresh: "your_refresh_token") {
    access
  }
}

```

<p><b>Create Order</p>/<b>

```bash

mutation {
  createOrder(input: {
    customerCode: "CUST216204",
    item: "Laptop",
    amount: 500.0
  }) {
    order {
      customer {
        code
      }
      item
      amount
    }
    message
    smsMessage
    smsStatus
  }
}

```

<p><b>Update Order</p>/<b>

```bash

mutation {
  updateOrder(orderId: "128a3b7f-d146-4793-a3c1-b5ee04d21316", item: "New Item Name", amount: "150.00") {
    order {
      customer {
        code
      }
      item
      amount
    }
  }
}

```

To get UUID via Python shell for ORM :

```bash
    python3 manage.py shell
```
```bash
    from orders.models import Order
    order = Order.objects.first() 
    print(order.order_id)
```
    or start psql:

```bash
    SELECT order_id FROM orders;
```

## <h1> Terraform </h1>
<p>Terraform has been used and configurations set for [Render](https://render.com/)</p>
<p>The configurations located are in: [text](terraform/main.tf).</p>

## <h1> Ansible </h1>
<p>The Ansible playbook has been written for consistent installations across local environments and can be used to configure various local machines</p>

<p>Use this command to tun a playbook:</p>

```bash
ansible-playbook -i hosts.ini local_tasks.yml
```

<p>To run as a sudo or admin user:</p>

```bash
ansible-playbook playbook.yml --ask-become-pass
```
## <h1> Author </h1>
Built by <b>Andrew Indeche</b>