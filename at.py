import os
from dotenv import load_dotenv
from pyairtable import Api
import requests
from typing import TypedDict
from models import TikTokAge, TikTokGender, TikTokLocation, LocationData

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
PROD_AIRTABLE_API_KEY = os.getenv('PROD_AIRTABLE_API_KEY')
PROD_AIRTABLE_BASE_ID = os.getenv('PROD_AIRTABLE_BASE_ID')

api = Api(AIRTABLE_API_KEY)
prod_api = Api(PROD_AIRTABLE_API_KEY)

PROD_INFLUENCER_ACCOUNTS_TABLE_ID = "tblWtH5Fy3et1fK1K"

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


def update_influencer_tt_age(influencer_id: str, data: TikTokAge):
    influencer_accounts = prod_api.table(PROD_AIRTABLE_BASE_ID, PROD_INFLUENCER_ACCOUNTS_TABLE_ID)
    TT_18_TO_24 = "fld1bkDoHgR8ijGgR"
    TT_25_TO_34 = "fldnIJgkN7gv1PUxs"
    TT_35_TO_44 = "fld0DH9IyMm6CK2wx"
    TT_45_TO_54 = "fldz4LZX1YCIv3VTm"
    TT_55_OVER  = "fldDVF3Y0WJ69WDVB"

    res = influencer_accounts.update(influencer_id, {
        TT_18_TO_24: data.quartile_1,
        TT_25_TO_34: data.quartile_2,
        TT_35_TO_44: data.quartile_3,
        TT_45_TO_54: data.quartile_4,
        TT_55_OVER: data.quartile_5
    })

    return res

def update_influencer_tt_gender(influencer_id: str, data: TikTokGender):
    influencer_accounts = prod_api.table(PROD_AIRTABLE_BASE_ID, PROD_INFLUENCER_ACCOUNTS_TABLE_ID)
    TT_MALE = 'fldhkUhORcfrod4JS'
    TT_FEMALE = 'fld9q3R8MHk49Z4gZ'

    res = influencer_accounts.update(influencer_id, {
        TT_MALE: data.male,
        TT_FEMALE: data.female
    })

    return res

def update_influencer_tt_location(influencer_id: str, data: TikTokLocation):
    influencer_accounts = prod_api.table(PROD_AIRTABLE_BASE_ID, PROD_INFLUENCER_ACCOUNTS_TABLE_ID)
    TT_PRIMARY_COUNTRY = 'fldGCg8z5KhN0AroR'
    TT_PRIMARY_COUNTRY_PERCENT = 'fldnMgu911D7ndhRY'

    TT_SECONDARY_COUNTRY = 'fldEESHzCRJzB0XaQ'
    TT_SECONDARY_COUNTRY_PERCENT = 'fldE95CXCl1WjAHpX'

    TT_TERTIARY_COUNTRY = 'fldrA8BQfZFmsaPrx'
    TT_TERTIARY_COUNTRY_PERCENT = 'fldJWZmcd9sOZj0Rz'



    res = influencer_accounts.update(influencer_id, {
       TT_PRIMARY_COUNTRY: data.primary.country,
       TT_PRIMARY_COUNTRY_PERCENT: data.primary.percentage,
       TT_SECONDARY_COUNTRY: data.second.country,
       TT_SECONDARY_COUNTRY_PERCENT: data.second.percentage,
       TT_TERTIARY_COUNTRY: data.third.country,
       TT_TERTIARY_COUNTRY_PERCENT: data.third.percentage
    },  typecast=True)

    return res

# res = get_influencer_metric_attachments('recDHW9EvpbgWsF3V')
# print(res)

# r = update_influencer_tt_age('recP8HESeDrmbkx24', TikTokAge(quartile_1=0.69, quartile_2=0.69, quartile_3=0.69, quartile_4=0.69, quartile_5=0.69))

# print(r)

# Test update_influencer_tt_location
test_location_data = TikTokLocation(
    primary=LocationData(country="United States", percentage=0.45),
    second=LocationData(country="Canada", percentage=0.203),
    third=LocationData(country="United Kingdom", percentage=0.152),
    fourth=LocationData(country="Australia", percentage=0.1),
    other=LocationData(country="Other", percentage=0.09)
)

r = update_influencer_tt_location('recP8HESeDrmbkx24', test_location_data)
