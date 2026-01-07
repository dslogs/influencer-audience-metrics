import os
from dotenv import load_dotenv
from pyairtable import Api
import requests
from typing import TypedDict
from models import TikTokAge, TikTokGender, TikTokLocation, LocationData, IGAge, IGGender, IGLocation

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
PROD_AIRTABLE_API_KEY = os.getenv('PROD_AIRTABLE_API_KEY')
PROD_AIRTABLE_BASE_ID = os.getenv('PROD_AIRTABLE_BASE_ID')

api = Api(AIRTABLE_API_KEY)
prod_api = Api(PROD_AIRTABLE_API_KEY)

PROD_INFLUENCER_ACCOUNTS_TABLE_ID = "tblWtH5Fy3et1fK1K"

class AudienceMetrics(TypedDict):
    influencer_id: str
    tt_age: bytes | None
    tt_age_img_type: str | None
    tt_gender: bytes | None
    tt_gender_img_type: str | None
    tt_location: bytes | None
    tt_location_img_type: str | None
    ig_age: bytes | None
    ig_age_img_type: str | None
    ig_gender: bytes | None
    ig_gender_img_type: str | None
    ig_location: bytes | None
    ig_location_img_type: str | None

def get_bytes_and_type_for_field(data):
    try:
        data_bytes = None
        image_type = None

        if data and len(data) > 0:
            first_pic = data[0]
            response = requests.get(first_pic['url'])
            data_bytes = response.content
            image_type = first_pic['type']

        return data_bytes, image_type

    except Exception as e:
        return None, None

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
    INFLUENCER_PROD_RECORD_ID = 'flde0jFS2GAXaHMxx'

    tt_location_bytes, tt_location_img_type = get_bytes_and_type_for_field(fields.get(TT_LOCATION))
    tt_gender_bytes, tt_gender_img_type = get_bytes_and_type_for_field(fields.get(TT_GENDER))
    tt_age_bytes, tt_age_img_type = get_bytes_and_type_for_field(fields.get(TT_AGE))
    ig_location_bytes, ig_location_img_type = get_bytes_and_type_for_field(fields.get(IG_LOCATION))
    ig_gender_bytes, ig_gender_img_type  = get_bytes_and_type_for_field(fields.get(IG_GENDER))
    ig_age_bytes, ig_age_img_type = get_bytes_and_type_for_field(fields.get(IG_AGE))
    influencer_id = fields.get(INFLUENCER_PROD_RECORD_ID)

    # ITS A LOOKUP IN AT SO ITS ACTUALLY AN ARRAY
    if influencer_id:
        influencer_id = influencer_id[0]

    return AudienceMetrics(
        influencer_id=influencer_id,
        tt_location=tt_location_bytes,
        tt_location_img_type=tt_location_img_type,
        tt_gender=tt_gender_bytes,
        tt_gender_img_type=tt_gender_img_type,
        tt_age=tt_age_bytes,
        tt_age_img_type=tt_age_img_type,
        ig_age=ig_age_bytes,
        ig_age_img_type=ig_age_img_type,
        ig_gender=ig_gender_bytes,
        ig_gender_img_type=ig_gender_img_type,
        ig_location=ig_location_bytes,
        ig_location_img_type=ig_location_img_type)


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

def update_influencer_ig_age(influencer_id: str, data: IGAge):
    influencer_accounts = prod_api.table(PROD_AIRTABLE_BASE_ID, PROD_INFLUENCER_ACCOUNTS_TABLE_ID)
    IG_13_TO_17 = "fldhvKdI0Dc2W3C9H"
    IG_18_TO_24 = "fldWoC6EYhS9e9bE7"
    IG_25_TO_34 = "fldezDijOJhPfKKcp"
    IG_35_TO_44 = "fldM3GbW5RfpnvGx5"
    IG_45_TO_54 = "fldokv33Lt4TlJSDU"
    IG_55_TO_64 = "fldHlknDyLl764rqP"
    IG_65_OVER  = "fldYdnIeWUWGiLUER"

    res = influencer_accounts.update(influencer_id, {
        IG_13_TO_17: data.quartile_1,
        IG_18_TO_24: data.quartile_2,
        IG_25_TO_34: data.quartile_3,
        IG_35_TO_44: data.quartile_4,
        IG_45_TO_54: data.quartile_5,
        IG_55_TO_64: data.quartile_6,
        IG_65_OVER: data.quartile_7
    })

    return res

def update_influencer_ig_gender(influencer_id: str, data: IGGender):
    influencer_accounts = prod_api.table(PROD_AIRTABLE_BASE_ID, PROD_INFLUENCER_ACCOUNTS_TABLE_ID)
    IG_MALE = 'fldt0o7BuQh1Pb5HO'
    IG_FEMALE = 'fldBJtTLMA0uRhjhN'

    res = influencer_accounts.update(influencer_id, {
        IG_MALE: data.male,
        IG_FEMALE: data.female
    })

    return res

def update_influencer_ig_location(influencer_id: str, data: IGLocation):
    influencer_accounts = prod_api.table(PROD_AIRTABLE_BASE_ID, PROD_INFLUENCER_ACCOUNTS_TABLE_ID)
    IG_PRIMARY_COUNTRY = 'fld9MWyta6WLouKar'
    IG_PRIMARY_COUNTRY_PERCENT = 'fld5d1DFcVSxl3KkI'

    IG_SECONDARY_COUNTRY = 'fldJ6LsYk0tNxKcHY'
    IG_SECONDARY_COUNTRY_PERCENT = 'fldcTCZPySSNL8MsJ'

    IG_TERTIARY_COUNTRY = 'fldriUkHehCm1llQO'
    IG_TERTIARY_COUNTRY_PERCENT = 'fldEfUGPC4tBaIWNM'

    res = influencer_accounts.update(influencer_id, {
        IG_PRIMARY_COUNTRY: data.primary.country,
        IG_PRIMARY_COUNTRY_PERCENT: data.primary.percentage,
        IG_SECONDARY_COUNTRY: data.second.country,
        IG_SECONDARY_COUNTRY_PERCENT: data.second.percentage,
        IG_TERTIARY_COUNTRY: data.third.country,
        IG_TERTIARY_COUNTRY_PERCENT: data.third.percentage
    }, typecast=True)

    return res

# res = get_influencer_metric_attachments('recDHW9EvpbgWsF3V')
# print(res)

# r = update_influencer_tt_age('recP8HESeDrmbkx24', TikTokAge(quartile_1=0.69, quartile_2=0.69, quartile_3=0.69, quartile_4=0.69, quartile_5=0.69))

# print(r)

# Test update_influencer_tt_location
# test_location_data = TikTokLocation(
#     primary=LocationData(country="United States", percentage=0.45),
#     second=LocationData(country="Canada", percentage=0.203),
#     third=LocationData(country="United Kingdom", percentage=0.152),
#     fourth=LocationData(country="Australia", percentage=0.1),
#     other=LocationData(country="Other", percentage=0.09)
# )

# r = update_influencer_tt_location('recP8HESeDrmbkx24', test_location_data)

# test_influencer_ig_age = IGAge(quartile_1=0.1, quartile_2=0.2, quartile_3=0.3, quartile_4=0.4, quartile_5=0.5, quartile_6=0.6, quartile_7=0.7)
# update_influencer_ig_age('recP8HESeDrmbkx24', test_influencer_ig_age)

# test_influencer_ig_gender = IGGender(male=0.1, female=0.1)
# update_influencer_ig_gender('recP8HESeDrmbkx24', test_influencer_ig_gender)


# test_location_data = IGLocation(
#     primary=LocationData(country="USA", percentage=0.1),
#     second=LocationData(country="CA", percentage=0.2),
#     third=LocationData(country="UK", percentage=0.3),
#     fourth=LocationData(country="Aus", percentage=0.4),
#     other=LocationData(country="Jap", percentage=0.5)
# )

# update_influencer_ig_location('recP8HESeDrmbkx24', test_location_data)

