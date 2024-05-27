from dataclasses import dataclass

@dataclass
class Airport:
    ID: int
    IATA_CODE: str
    AIRPORT: str
    CITY: str
    STATE: str
    COUNTRY: str
    LATITUDE: float
    LONGITUDE: float
    TIMEZONE_OFFSET: float
    def __str__(self):
        return f"{self.ID}-{self.IATA_CODE}-{self.AIRPORT}"

    def __hash__(self):
        return hash(self.ID)