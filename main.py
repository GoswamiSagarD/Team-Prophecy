import os
import Code.src.dataengineering.webscraping.cec_webscrape as wb
import Code.src.dataengineering.csvgathering.csv_read as cr
import Code.src.cloud_functions.trigger.read_cloud_storage as rcs

if __name__ == '__main__':
    print("Starting main function...")
    #wb.init()
    #cr.initializeCSVFiles()
    rcs.assess_file_entrypoint()
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT",8080)))

"""
#USING FLASK SO THAT WAY THIS CAN OPERATE AS A SERVER FOR THE TIME BEING
from flask import Flask

app = Flask(__name__)

@app.route("/")
def init_route():
    return "Starting gcloud instance"
"""