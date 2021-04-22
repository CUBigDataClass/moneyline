# moneyline
Team Moneyline sports betting app.


## To set up:


### Create and populate database
- Make sure pip3 and python3 are installed on your system

- Install ansible:

Linux:
```
sudo apt install ansible
```

Unix: 
```
sudo pip install ansible
```

- Insert AWS creds into PutNBADataFunction/put_NBA_data.py and PutNBADataFunction/add_daily.py

- In the moneyline directory preform following command which will start a playbook to install requirments, create DynamoDB, insert data, create cronjob to insert data daily:
```
ansible-playbook playbook.yml
```

### Deploy Frontend
- Create Ubuntu Amazon EC2 instance with security rules allowing inbound http traffic on port 80

- ssh into your ec2 instance and preform following commands

```
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y nginx
cd /var/www
sudo git clone https://github.com/CUBigDataClass/moneyline.git
sudo bash moneyline/moneyline-app/config.sh
```

- Navigate to your ec2's domain in browser







