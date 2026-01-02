import os
from dotenv import load_dotenv
from pyairtable import Api
import requests
from typing import TypedDict

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

api = Api(AIRTABLE_API_KEY)


class AudienceMetrics(TypedDict):
    tt_age: bytes | None
    tt_gender: bytes | None
    tt_location: bytes | None
    ig_age: bytes | None
    ig_gender: bytes | None
    ig_location: bytes | None


def get_influencer_metric_attachments(record_id: str) -> AudienceMetrics:
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

    return AudienceMetrics(
        tt_location=tt_location_bytes,
        tt_gender=None,
        tt_age=None,
        ig_age=None,
        ig_gender=None,
        ig_location=None)


