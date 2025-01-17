from src.get_geodetails import get_location_details
import swisseph as swe
from typing import Dict, Tuple

class AstrologyCalculator:
    def __init__(self):
        swe.set_ephe_path()
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", 
            "Leo", "Virgo", "Libra", "Scorpio", 
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        self.planets = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN
        }

    def get_zodiac_sign(self, degree: float) -> str:
        normalized_degree = degree % 360
        sign_index = int(normalized_degree // 30)
        return self.zodiac_signs[sign_index]

    def calculate_julian_day(self, year: int, month: int, day: int, 
                             hour: int, minute: int, timezone: float) -> float:
        hour_utc = hour - timezone
        return swe.julday(year, month, day, hour_utc + minute / 60.0)

    def calculate_planet_position(self, jd: float, planet_id: int) -> Tuple[float, str]:
        try:
            result = swe.calc_ut(jd, planet_id)[0]
            degree = result[0]
            sign = self.get_zodiac_sign(degree)
            return degree, sign
        except swe.Error as e:
            raise ValueError(f"Error calculating planetary position: {e}")

    def calculate_ascendant(self, jd: float, latitude: float, longitude: float) -> Tuple[float, str]:
        try:
            houses = swe.houses(jd, latitude, longitude, b'P')[0]
            degree = houses[0]
            sign = self.get_zodiac_sign(degree)
            return degree, sign
        except swe.Error as e:
            raise ValueError(f"Error calculating ascendant: {e}")

    def calculate_horoscope(self, name: str, birth_data: Dict) -> Dict:
        try:
            jd = self.calculate_julian_day(
                birth_data['year'], birth_data['month'], birth_data['day'],
                birth_data['hour'], birth_data['minute'], birth_data['timezone']
            )
            horoscope = {'Name': name, 'Birth Data': birth_data}

            for planet_name, planet_id in self.planets.items():
                degree, sign = self.calculate_planet_position(jd, planet_id)
                horoscope[planet_name] = {
                    'sign': sign,
                    'degree': f"{degree:.2f}°"
                }

            asc_degree, asc_sign = self.calculate_ascendant(
                jd, birth_data['latitude'], birth_data['longitude']
            )
            horoscope['Ascendant'] = {
                'sign': asc_sign,
                'degree': f"{asc_degree:.2f}°"
            }

            return horoscope

        except Exception as e:
            raise ValueError(f"Error generating horoscope: {str(e)}")

    def display_horoscope(self, horoscope: Dict) -> None:
        print("\n=== Horoscope Analysis ===")
        print(f"Name: {horoscope['Name']}")
        print("\nBirth Details:")
        for key, value in horoscope['Birth Data'].items():
            print(f"{key.capitalize()}: {value}")
        
        print("\nPlanetary Positions:")
        for planet in self.planets.keys():
            if planet in horoscope:
                print(f"{planet:8}: {horoscope[planet]['sign']:12} at {horoscope[planet]['degree']}")
        
        print(f"\nAscendant: {horoscope['Ascendant']['sign']} at {horoscope['Ascendant']['degree']}")

if __name__ == "__main__":
    calculator = AstrologyCalculator()

    city = "Haldwani"
    country = "INDIA"
    birth_time = {
        'year': 1990,
        'month': 7,
        'day': 15,
        'hour': 10,
        'minute': 30
    }

    try:
        location_details = get_location_details(city, country)
        birth_data = {**birth_time, **location_details}
        horoscope = calculator.calculate_horoscope("John Doe", birth_data)
        calculator.display_horoscope(horoscope)
    except ValueError as e:
        print(f"Error: {e}")
