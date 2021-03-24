# moneyline
Team Moneyline sports betting app.


## If you want to set up local version:


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







