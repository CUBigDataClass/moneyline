import json
import csv
import boto3

region = "us-west-2"
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('nba')
bucket = 'moneyline-csv2dynamodb'
key = 'output.csv'

def lambda_handler(event, context):
    record_list = []

    try:
        csv_file = s3.get_object(Bucket=bucket, Key=key)

        record_list = csv_file['Body'].read().decode('utf-8').split('\n')

        csv_reader = csv.reader(record_list, delimiter=',', quotechar='"')
        counter = 0
        column_name = []
        table_data = []
        for row in csv_reader:
            if counter == 0:
                column_name = row
            else:
                if len(row) > 0:
                    table_data.append(
                        {column_name[x]: row[x] for x in range(len(column_name)) if len(column_name) == len(row)})

            counter += 1
        do_batch_put_item(table_data)
    except Exception as e:
        print(e)


def do_batch_put_item(table_data):
    try:
        with table.batch_writer() as writer:
            for item in table_data:
                writer.put_item(Item=item)
        # print(f"Loaded {len(table_data)} into table {table.name}")
    except Exception as e:
        print(f"[ErrorMessage]: call Batch_PUT_ITEM() failure] - Error: {e}")
