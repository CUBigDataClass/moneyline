# moneyline
Team Moneyline sports betting app.

## Dockerize Dynamodb Local
create a docker network for local lambda:
    docker network create lambda-local

start local DynamoDB docker container
    docker run --network=lambda-local --name dynamo -p 8000:8000 amazon/dynamodb-local

check DynamoDB local tables
    aws dynamodb list-tables --endpoint-url http://127.0.0.1:8000

list items from the local DynamoDB table
    aws dynamodb scan --table-name USERS --endpoint-url http://127.0.0.1:8000

invoke a local Lambda function in the docker network
    sam local invoke PutNBADataFunction --event events/event.json --docker-network lambda-local

##GUI for Dynamodb local
Install: npm install -g dynamodb-admin
Use:
    1. Open a new terminal window, and execute dynamodb-admin
    2. Go to localhost:8001

