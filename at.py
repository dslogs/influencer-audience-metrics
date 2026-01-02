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

def get_bytes_for_field(data)-> bytes | None:
    try:

        data_bytes = None
        if data and len(data) > 0:
            first_pic = data[0]
            response = requests.get(first_pic['url'])
            data_bytes = response.content
        return data_bytes
    
    except Exception as e:
        return None

def get_influencer_metric_attachments(record_id: str) -> AudienceMetrics:
    audience_metrics = api.table(AIRTABLE_BASE_ID, "tbleVAs7oNLDhUwAk")

    record = audience_metrics.get(record_id, use_field_ids=True)
    fields = record.get('fields')

    TT_LOCATION = 'fldSSYdaauiP4dKGk'
    TT_GENDER = 'fldEaCfV6uy6Y1F6F'
    TT_AGE = 'fldQPfFg8M9GHtDcH'
    IG_LOCATION  = 'fld8xW2muxZJwdV58'
    IG_GENDER = 'fldZvtxBTQW3mZYzn'
    IG_AGE = 'fldTsq1MgZnzPgeAq'

    tt_location_bytes = get_bytes_for_field(fields.get(TT_LOCATION))
    tt_gender_bytes = get_bytes_for_field(fields.get(TT_GENDER))
    tt_age_bytes = get_bytes_for_field(fields.get(TT_AGE))
    ig_location_bytes = get_bytes_for_field(fields.get(IG_LOCATION))
    ig_gender_bytes = get_bytes_for_field(fields.get(IG_GENDER))
    ig_age_bytes = get_bytes_for_field(fields.get(IG_AGE))

    return AudienceMetrics(
        tt_location=tt_location_bytes,
        tt_gender=tt_gender_bytes,
        tt_age=tt_age_bytes,
        ig_age=ig_age_bytes,
        ig_gender=ig_gender_bytes,
        ig_location=ig_location_bytes)



res = get_influencer_metric_attachments('recDHW9EvpbgWsF3V')
print(res)