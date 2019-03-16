from multiprocessing import Process
from snowplow_tracker import Subject, Tracker, AsyncEmitter
from snowplow_tracker import SelfDescribingJson
from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonschema import validate
from datetime import datetime
from time import sleep
import jsonschema
import psycopg2
import urllib
import json
import os

# Retrieve env variables
host = os.getenv('DB_HOSTNAME')
name = os.getenv('DB_NAME')
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Postgres
connect_string = "host={host} dbname={dbname} user={user} password={password}".format(host=host,dbname=name,user=user,password=password)


client_calls_sql = """INSERT INTO caps.client_calls(received_timestamp,ip_address,response_code,raw_data,environment,namespace,app_id,device_created_timestamp,event_data_json)
                      VALUES(%s,%s,%s,%s,%s,%s,%s,TO_TIMESTAMP(%s::decimal/1000),%s) RETURNING request_id ;"""

snowplow_no_call_sql = """INSERT INTO caps.snowplow_calls(request_id)
                                    VALUES(%s) RETURNING snowplow_send_id ;"""

snowplow_select_uncalled = """SELECT * FROM caps.snowplow_calls WHERE try_number IS NULL ;"""

snowplow_calls_sql = """INSERT INTO caps.snowplow_calls(request_id, sent_timestamp, snowplow_response, try_number)
                        VALUES(%s, %s, %s, %s) RETURNING snowplow_send_id ;"""

# POST body JSON validation schema
post_schema = json.load(open('post_schema.json', 'r'))

# Create a connection to postgres, and execute a query
# Returns the first column for that insertion, which was the postgres generated identifier
def db_query(sql,execute_tuple,all=False):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute(sql,execute_tuple)
    if all:
        fetch = cur.fetchall()
    else:
        fetch = cur.fetchone()
    conn.commit()
    cur.close()
    return fetch

def plows():
    while True:
        sleep(10)
        rows = db_query(snowplow_select_uncalled,None,True)
        for row in rows:
            snowplow_id = row[0]
            request_id = row[1]
            query = db_query("SELECT environment,namespace,app_id,device_created_timestamp,event_data_json FROM caps.client_calls WHERE request_id = {}".format(request_id),None)
            environment = query[0]
            namespace = query[1]
            app_id = query[2]
            device_created_timestamp = query[3]
            event_data_json = json.loads(query[4])
            # print("{} {} {} {}".format(environment,namespace,app_id,device_created_timestamp))

def serve():
    server_address = ('0.0.0.0', 443)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()   

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        received_timestamp = datetime.now()
        ip_address = self.client_address[0]

        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')

        # Test that the post_data is JSON
        try:
            json_object = json.loads(post_data)
        except (json.decoder.JSONDecodeError,ValueError) as e:
            response_code = 400
            self.send_response(response_code, 'POST body is not parsable as JSON.')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            post_tuple = (received_timestamp,ip_address,response_code,post_data,None,None,None,None,None)
            request_id = db_query(client_calls_sql,post_tuple)[0]
            return
            
        # Test that the JSON matches the expeceted schema
        try:
            jsonschema.validate(json_object, post_schema)
        except (jsonschema.ValidationError, jsonschema.SchemaError ) as e:
            response_code = 400
            self.send_response(response_code, 'POST JSON is not compliant with schema.')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            post_tuple = (received_timestamp,ip_address,response_code,post_data,None,None,None,None,None)
            request_id = db_query(client_calls_sql,post_tuple)[0]
            return

        # TODO: test that the input device_created_timestamp is in ms
        device_created_timestamp = json_object['dvce_created_tstamp']
        if device_created_timestamp < 99999999999: # 11 digits, Sat Mar 03 1973 09:46:39 UTC
            # it's too small to be in seconds
            response_code = 400
            self.send_response(response_code, 'Device Created Timestamp is not in milliseconds.')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            post_tuple = (received_timestamp,ip_address,response_code,post_data,None,None,None,None,None)
            request_id = db_query(client_calls_sql,post_tuple)[0]
            return


        # Input POST is JSON and validates to schema
        response_code = 200
        self.send_response(response_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        post_tuple = (
            received_timestamp,
            ip_address,
            response_code,
            post_data,
            json_object['env'],
            json_object['namespace'],
            json_object['app_id'],
            json_object['dvce_created_tstamp'],
            json.dumps(json_object['event_data_json']))
        request_id = db_query(client_calls_sql, post_tuple)[0]

        # TODO: 
        # Insert this request_id into caps.snowplow_calls
        # Send to Snowplow and insert the response to caps.snowplow_calls referencing request_id
        snowplow_tuple = (str(request_id),)
        snowplow_id = db_query(snowplow_no_call_sql, snowplow_tuple)[0]

Process(target=serve).start()
Process(target=plows).start()