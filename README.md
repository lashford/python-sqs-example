# Python AWS SQS Example

Example Python App Consuming and Producing messages to AWS SQS

## Environment Setup

Follow the instructions below to configure your local machine to run and develop this example Python application.

_Note:_ The instructions are focused on MacOsx however other environments will be supported with a bit of googling.

### Local Docker Environment
The example code relies on a running SQS service, the repo contains a Docker compose file that will spin up a configured SQS using Localstack.

* Install Docker Toolbox - [Instructions](https://www.docker.com/products/docker-toolbox)

* Run the docker environment `docker-compose up`

This will launch a SQS service listening on port `4576`

### Build dependencies

* Python 3 `$ brew install python3`
* Virtual Env `$ sudo pip3 install virtualenv`

### Configure and Run

From the terminal enable & configure the application dependencies.
* `$ virtualenv env`
* `$ source env/bin/activate`
* `(env) $ pip3 install -r requirements.txt`

You can now run the application
* `(env) $ python3 sqs-example`

To leave the virtual Environment
* `(env) $ deactivate`
