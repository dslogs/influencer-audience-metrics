import os
from dotenv import load_dotenv
from pyairtable import Api
import requests
from typing import TypedDict

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
api = Api(AIRTABLE_API_KEY)


class InfluencerMetrics(TypedDict):
    tt_location: bytes | None


def get_influencer_metric_attachments(record_id: str) -> InfluencerMetrics:
    audience_metrics = api.table(AIRTABLE_BASE_ID, "tbleVAs7oNLDhUwAk")

    record = audience_metrics.get(record_id, use_field_ids=True)
    fields = record.get('fields')
    tt_location_field_id = 'fldSSYdaauiP4dKGk'
    attachment_array = fields.get(tt_location_field_id)

    tt_location_bytes = None
    if attachment_array and len(attachment_array) > 0:
        first_pic = attachment_array[0]
        response = requests.get(first_pic['url'])
        tt_location_bytes = response.content

    return InfluencerMetrics(tt_location=tt_location_bytes)


