import os
from dotenv import load_dotenv
from pyairtable import Api
import requests

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
api = Api(AIRTABLE_API_KEY)

if __name__ == "__main__":

    audience_metrics = api.table(AIRTABLE_BASE_ID, "tbleVAs7oNLDhUwAk")
    records = audience_metrics.all(use_field_ids=True)
    print(records)

    for record in records:
        fields = record.get('fields')
        tt_location = 'fldSSYdaauiP4dKGk'
        attachment_array = fields.get(tt_location)
        if attachment_array and len(attachment_array) > 0:
            first_pic = attachment_array[0]
            response = requests.get(first_pic['url'])
            image_bytes = response.content


    # print(records)
