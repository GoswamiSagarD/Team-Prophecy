import os
import json
import google
from google.cloud import storage
from google.cloud import compute_v1

import functions_framework

from google.oauth2 import service_account
import google.auth.transport.requests

#HERE, WE MUST USE FLASK FOR THE CLOUD STORAGE BUCKET
# -> This comes from timvink's website: timvink.nl/google-cloud-functions
storage_creds = os.getcwd()+os.sep+"src"+os.sep+"prop"+os.sep+"tprophecy-378622-f2ee16c043fa.json"
snapshot_info = os.getcwd()+os.sep+"src"+os.sep+"prop"+os.sep+"cec_instance_snapshot.json"
gcloud_template_info = json.loads(os.getcwd()+os.sep+"src"+os.sep+"prop"+os.sep+"gcp_template_info.json")
creds = service_account.Credentials.from_service_account_file(filename=storage_creds)
"""
def create_instance_from_template() -> compute_v1.Instance:
    print("Starting instance process...")
    inst_cli = compute_v1.InstancesClient(credentials=creds)
"""

#The main purpose of this function is really just to get our ec2 instance started if we don't have it already
@functions_framework.cloud_event
def assess_file_entrypoint(cloud_event):
    print("Assessing File Entrypoint...")
    try:
        store_cli = storage.Client(project=gcloud_template_info["project_id"], credentials=creds)
        # CONNECT TO BUCKET (so that way all data can be yeeted to the newly created data instance)
        bucket_name = "cec_wl_upload_1"

        """EXPLICITLY FOR HANDLING BUCKETS"""
        #May need to remove; the data provided is likely going to be under cloud_event,
        # so no need to reference entire bucket
        t_prop_bucket = store_cli.get_bucket(bucket_name)
        CEC_data_available = t_prop_bucket.list_blobs()
        if CEC_data_available.num_results == 0:
            return
        #If we are able to find it, we should be ok to check for our compute instance
        """EXPLICITLY FOR starting our snapshot (only if it exists first)"""
        #This is a later process, we don't need to worry about it immediately
        client_instance = None

        try:
            print("Checking for recent snapshots...")
            client_instance_cli = compute_v1.InstancesClient(creds)
            req_params = str(json.loads(snapshot_info))
            cli_retrieval = client_instance_cli.insert(request=f"POST https://www.googleapis.com/compute/beta/projects/tprophecy-378622/zones/us-central1-a/instances {req_params}")
            if cli_retrieval.status == 200:
                client_instance = cli_retrieval
                print("Successful snapshot retrieval...")
            else:
                print("Unsuccessful snapshot retrieval...")
        except Exception as e:
            print(f"Could not find a snapshot, and received the following error: {e}")


        #If our snapshot doesn't exist, we have nothing to worry about and we can create our instance type...
        #if client_instance is None:
        #    client_instance = create_instance_from_template()

    except Exception as e:
        print(f"This was the error that we encountered: {e}")
    finally:
        if store_cli is not None:
            store_cli.close()

    #NOTE: THIS WORKS!!!
    #all_blobs = t_prop_bucket.list_blobs()
    #for a in all_blobs:
    #    a.delete()

    """EXPLICITLY FOR HANDLING THE CREATION OF INSTANCE TYPES"""
