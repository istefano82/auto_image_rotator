# flaskSaas

![License](http://img.shields.io/:license-mit-blue.svg)

A fork of [Max Halford's](https://github.com/MaxHalford) [flask-boilerplate](https://github.com/MaxHalford/flask-boilerplate). I've noticed SaaS bootstraps/boilerplates being sold upwards of $1,000 per year and I think that's fucking ridiculous. This project will be my attempt to make a great starting point for your next big business as easy and efficent as possible.

## Features

- [x] User account sign up, sign in, password reset, all through asynchronous email confirmation.
- [x] Form generation.
- [x] Error handling.
- [x] HTML macros and layout file.
- [x] "Functional" file structure.
- [x] Python 3.x compliant.
- [x] Asynchronous AJAX calls.
- [x] Administration panel.
- [x] Logging.
- [ ] Stripe subscriptions. (WIP)
- [ ] RESTful API for payments.
- [ ] Simple RESTful API to communicate with your app.

## Libraries

### Backend

- [Flask](http://flask.pocoo.org/), obviously.
- [Flask-Login](https://flask-login.readthedocs.org/en/latest/) for the user accounts.
- [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) interacting with the database.
- [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/) and [WTForms](https://wtforms.readthedocs.org/en/latest/) for the form handling.
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/) for sending mails.
- [itsdangerous](http://pythonhosted.org/itsdangerous/) for generating random tokens for the confirmation emails.
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.org/en/latest/) for generating secret user passwords.
- [Flask-Admin](https://flask-admin.readthedocs.org/en/latest/) for building an administration interface.
- [Flask-Script](https://flask-script.readthedocs.io/en/latest/) for managing the app.
- [structlog](http://structlog.readthedocs.io/en/stable/) for logging.
- [Flask-DebugToolBar](https://flask-debugtoolbar.readthedocs.io/en/latest/) for adding a performance toolbar in development.
- [gunicorn](http://gunicorn.org/) for acting as a reverse-proxy for Nginx.
- [Flask-Stripe](http://stripe.com/) for subscription billing.

### Frontend

- [Semantic UI](http://semantic-ui.com/) for the global style. Very similar to [Bootstrap](http://getbootstrap.com/).
- [Leaflet JS](http://leafletjs.com/) for the map. I only added it for the sake of the example.

## Structure

I did what most people recommend for the application's structure. Basically, everything is contained in the `app/` folder.

- There you have the classic `static/` and `templates/` folders. The `templates/` folder contains macros, error views and a common layout.
- I added a `views/` folder to separate the user and the website logic, which could be extended to the the admin views.
- The same goes for the `forms/` folder, as the project grows it will be useful to split the WTForms code into separate files.
- The `models.py` script contains the SQLAlchemy code, for the while it only contains the logic for a `users` table.
- The `toolbox/` folder is a personal choice, in it I keep all the other code the application will need.
- Management commands should be included in `manage.py`. Enter `python manage.py -?` to get a list of existing commands.
- I added a Makefile for setup tasks, it can be quite useful once a project grows.


## Setup

### Vanilla

- Create .env file in the app root directory with the variables needed in the
 config_common.py

- Install the requirements and setup the development environment.

	`make install && make dev`

- Create the database.

	`python manage.py initdb`

- Run the application.

	`python manage.py runserver`

- Navigate to `localhost:5000`.

## Configuration

The goal is to keep most of the application's configuration in a single file called `config.py`. I added a `config_dev.py` and a `config_prod.py` who inherit from `config_common.py`. The trick is to symlink either of these to `config.py`. This is done in by running `make dev` or `make prod`.

I have included a working Gmail account to confirm user email addresses and reset user passwords, although in production you should't include the file if you push to GitHub because people can see it. The same goes for API keys, you should keep them secret. You can read more about secret configuration files [here](https://exploreflask.com/configuration.html).

Read [this](http://flask.pocoo.org/docs/0.10/config/) for information on the possible configuration options.

## Export Deep learning model for TF serving

### Create model docker container
* Navigate to /model_serve_docker
* Update tf_serving_build_model.py to build model and load saved weights
* Generate TF serving files and Docker file run `% python tf_serving_build_model
.py`
* generate model docker container - `docker build -t tf-serving-heroku-1.11 .`
### Test docker locally
* `docker run -p 8501:8501 -e PORT=8501 -t tf-serving-heroku-1.11`
* Update test client `test_model_docker.py` Model URL for local test 
`full_url = "localhost:8501/v1/models/tf_serving_keras_mobilenet/versions/1
:predict"
* Run test client - `python test_model_docker.py`

### Export TF model to Heroku
* Login to container registry `% heroku container:login`
* OPtional if not alread done
  * heroku create {APP NAME} - i.e `heroku create image-rotation-detector`
* Push docker image to Heroku
  * `heroku  container:push web -a ${YOUR_APP_NAME}` - i.e `heroku  container:push web -a image-rotation-detector`
  * `heroku container:release web -a ${YOUR_APP_NAME}` - i.e `heroku container:release web -a ${image-rotation-detector`
* Test app with REST Request
  * Update test client `test_model_docker.py` Model URL for local test 
`full_url = "https://image-rotation-detector.herokuapp.com/v1/models/tf_serving_keras_mobilenet/versions/1:predict""

## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.
