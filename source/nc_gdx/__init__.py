import json
import sys
import traceback
from flask import Config
import pika
import requests
from .configuration import configuration
from .gdx_ import *


class GDX(object):


    def __init__(self):
        self.config = Config(__name__)


    def on_execute_gdx(self,
            channel,
            method_frame,
            header_frame,
            body):

        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:

            # Execute GDX command. Required information:
            # - Script to execute
            #
            # Assumptions:
            # - Input data accessible from script directory

            pass


            ### body = body.decode("utf-8")
            ### sys.stdout.write("{}\n".format(body))
            ### sys.stdout.flush()
            ### data = json.loads(body)
            ### plan_uri = data["uri"]
            ### workspace_name = data["workspace"]
            ### response = requests.get(plan_uri)

            ### assert response.status_code == 200, response.text

            ### plan = response.json()["plan"]
            ### pathname = plan["pathname"]
            ### status = plan["status"]
            ### skip_registration = False


            ### if status != "uploaded":
            ###     sys.stderr.write("Skipping plan because 'status' is not "
            ###         "'uploaded', but '{}'".format(status))
            ###     sys.stderr.flush()
            ###     skip_registration = True


            ### if not skip_registration:

            ###     assert status == "uploaded", status

            ###     layer_name = register_raster(
            ###         pathname,
            ###         workspace_name,
            ###         geoserver_uri=self.config["NC_GEOSERVER_URI"],
            ###         geoserver_user=self.config["NC_GEOSERVER_USER"],
            ###         geoserver_password=self.config["NC_GEOSERVER_PASSWORD"])

            ###     # Mark plan as 'registered'.
            ###     payload = {
            ###         "layer_name": layer_name,
            ###         "status": "registered"
            ###     }
            ###     response = requests.patch(plan_uri, json=payload)

            ###     assert response.status_code == 200, response.text


        except Exception as exception:

            sys.stderr.write("{}\n".format(traceback.format_exc()))
            sys.stderr.flush()


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def run(self,
            host):

        self.credentials = pika.PlainCredentials(
            self.config["NC_RABBITMQ_DEFAULT_USER"],
            self.config["NC_RABBITMQ_DEFAULT_PASS"]
        )
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitmq",
            virtual_host=self.config["NC_RABBITMQ_DEFAULT_VHOST"],
            credentials=self.credentials,
            # Keep trying for 8 minutes.
            connection_attempts=100,
            retry_delay=5  # Seconds
        ))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)

        self.channel.queue_declare(
            queue="execute_gdx",
            durable=True)
        self.channel.basic_consume(
            self.on_execute_gdx,
            queue="execute_gdx")

        try:
            sys.stdout.write("Start consuming...\n")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...\n")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = GDX()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app
