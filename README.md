# Maintenance Tracker App

[![Build Status](https://travis-ci.org/johnmusiu/Maintenance-Tracker.svg?branch=develop-api)](https://travis-ci.org/johnmusiu/Maintenance-Tracker)
[![Coverage Status](https://coveralls.io/repos/github/johnmusiu/Maintenance-Tracker/badge.svg?branch=develop)](https://coveralls.io/github/johnmusiu/Maintenance-Tracker?branch=develop)

Maintenance Tracker App is an application that gives users the ability to reach out to operations/repairs department regarding repair or maintenance requests and monitor the status of their request.

## Hosted versions of the API

- [Heroku](https://gentle-sands-32555.herokuapp.com)
- [Documentation](https://maintrak.docs.apiary.io/)

## API Endpoints

**Base url: `/api/v2`**

| Request Type | EndPoint |Functionality|
|----------|---------------|----|
| POST | `/auth/signup` | Register a user. |
| POST | `/auth/login` | Login a user. |
| GET | `/users/requests` | Fetch all the requests of a logged in user. |
| GET | `/users/requests/<int:requestId>` |Fetch a request that belongs to a logged in user.|
| POST | `/users/requests` | Create a request. |
| PUT | `/users/requests/<int:requestId>` | Modify a request. This operation should not be possible when the admin has approved of the request. |
| GET | `/requests` | Fetch all the requests. This is available only to admin users. |
| GET | `/requests/<int:request_id>` | Fetch any of existing requests. This is available only to admin users. |
| PUT | `/requests/<int:requestId>/approve` | Approve request. This is available only to admin users. When this endpoint is called, the status of the request should be pending.
| PUT | `/requests/<int:requestId>/disapprove` | Disapprove request. This is available only to admin users. |
| PUT | `/requests/<int:requestId>/resolve` | Resolve request. This is available only to admin users. |
| POST | `/admin` | Creates an admin user. Accessible only to the super admin. |

## Usage Examples

- Users can create an account and log in.
- The users can make maintenance or repairs request.
- An admin can approve/reject a repair/maintenance request.
- The admin can mark request as resolved once it is done.
- The admin can view all maintenance/repairs requests on the application.
- The admin can filter requests.
- The user can view all his/her requests.

## Relevant links on github pages

|| [Landing page](https://johnmusiu.github.io/Maintenance-Tracker/) ||
[Admin home page](https://johnmusiu.github.io/Maintenance-Tracker/home-admin.html) ||
[User home page](https://johnmusiu.github.io/Maintenance-Tracker/home-user.html) ||

## Setting up the Project

The following steps will get this project up and running on your local enviroment.

### Prerequisites

You need to have installed:

- [Git](https://git-scm.com/)
- [Postman](https://www.getpostman.com/)
- [Postgresql](https://www.postgresql.org/) and have a user: `postgres` and a matching password.
- [Python](https://www.python.org/) 3.6
- [Pip](https://pypi.org/)

Note: You should have some basic working knowledge on the above

### Installing

1. Clone the repository

    ```git clone https://github.com/johnmusiu/Maintenance-Tracker/```

2. Change directory

    ```cd Maintenance-Tracker```

3. Checkout on develop branch

    ```git checkout develop```

4. To view UI designs navigate to the UI/ directory.

    ```cd ui/```

    Then open index.html on your browser.
5. To setup API locally, make sure you are in the base project folder `Maintenance-Tracker`

6. Set up a virtual environment and activate (`python 3.6`)

    ```pip install virtualenv```
    ```virtualenv -p python3.6 venv```
    ```source venv/bin/activate```

7. Install app dependencies

    ```pip install -r requirements.txt```

8. Set up the database and environment variables.

    ```python create_db.py```

            Provide your `postgres` user password.
            Provide a database name on which the app will run
            Ensure database setup is successful.

    ```source .env```

    ```python migration.py```

9. Run tests

    Either

    ```pytest``` or

    ```nosetests --exe --with-coverage --cover-package=api```

    The nosetests give a more comprehensive report about test coverage.

10. Run the flask app

    ```flask run```

11. Test the endpoints on postman

    For instance to signup you sent a request to `http://127.0.0.1:5000/api/v2/auth/register`

    A sample registration json request is given below:

    ```json
    {
        "first_name": "Annie",
        "last_name": "Ndindi",
        "email": "ndindis@gmail.com",
        "password": "WEeu00t",
        "confirm_password": "WEeu00t"
    }  
    ```
12. Testing admin functionality

    The super admin is:
            username: admin
            password: admin
    Login to get an access-token that can then be used to hit the `/admin` [POST] endpoint.
    The same credentials can be used on the hosted documentation to create an admin.
    After creating the admin you then have to login as an admin to have access to administrator privileges and functions.

To test without setting up local environment send requests to `https://gentle-sands-32555.herokuapp.com/api/v2/{endpoint}`  from postman.

To test without postman visit the online documentation [here](https://maintrak.docs.apiary.io/)

## Built With

- Python 3.6
- PostgeSQL
- HTML5
- CSS
- Javascript

## Contributing

1. Fork it from (https://github.com/johnmusiu/Maintenance-Tracker/fork)
2. Create your feature branch (```git checkout -b feature/some-feature```)
3. Commit your changes (```git commit -am 'Add some-feature'```)
4. Push to the branch (```git push origin feature/some-feature```)
5. Create a new Pull Request

## Author(s)

John Musiu johnmusiu@gmail.com
