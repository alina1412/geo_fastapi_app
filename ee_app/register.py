
import ee
import json
import os
import subprocess

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def google_register(Debug):
    if Debug:
        service_account = os.environ.get("service_account")
        KEY_FILE = os.environ.get("KEY_FILE")
        bashCommand = f"gcloud auth activate-service-account {service_account} --key-file={KEY_FILE}"
        subprocess.run(bashCommand.split(), shell=True)
    else:
        service_account = os.environ.get("service_account")
        
        line = os.environ.get("json_file")
        line = json.loads(line)
        filename = '_private-key2.json'
        with open(filename, 'w') as f:
            f.write(line)
        logger.debug("wrote-----")

        logger.debug(os.path.exists(filename))
        # bashCommand = f"gcloud auth activate-service-account {service_account} --key-file={filename}"
        # subprocess.run(bashCommand.split(), shell=True)

    # ee.Initialize()
    # print("-----Success----")

# pip install --upgrade tornado
# pip install --upgrade google-api-python-client
# pip install --upgrade earthengine-api
# pip install --upgrade google-auth
# google_register()
