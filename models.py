from pydantic import BaseModel


class TikTokAge(BaseModel):
    quartile_1: float # 18 - 24
    quartile_2: float # 25 - 34
    quartile_3: float # 35 - 44
    quartile_4: float # 45 - 54
    quartile_5: float # 55 +


class TikTokGender(BaseModel):
    male: float
    female: float


class LocationData(BaseModel):
    country: str
    percentage: float


class TikTokLocation(BaseModel):
    primary: LocationData
    second: LocationData
    third: LocationData
    fourth: LocationData
    other: LocationData


class IGAge(BaseModel):
    quartile_1: float # 13 - 17
    quartile_2: float # 18 - 24
    quartile_3: float # 25 - 34
    quartile_4: float # 35 - 44
    quartile_5: float # 45 - 54
    quartile_6: float # 55 - 64
    quartile_7: float # 65+


class IGGender(BaseModel):
    male: float
    female: float


class IGLocation(BaseModel):
    primary: LocationData
    second: LocationData
    third: LocationData
    fourth: LocationData
    other: LocationData
