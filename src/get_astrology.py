from src.get_horoscope import AstrologyCalculator
from src.get_geodetails import get_location_details
import google.generativeai as genai

import os

# Configure the Gemini API
genai.configure(api_key="AIzaSyBzWZlpLRF83w969LXpLsPofILiQg_Sen8")

class GetAstrology:
    def __init__(self):
        self.calculator = AstrologyCalculator()

    def fetch_horoscope(self, name: str, birth_data: dict, city: str, country: str) -> dict:
        """
        Fetches a detailed horoscope using the provided name, birth details, city, and country.

        Args:
            name (str): The name of the individual.
            birth_data (dict): A dictionary containing year, month, day, hour, and minute.
            city (str): The city of birth.
            country (str): The country of birth.

        Returns:
            dict: The complete horoscope details.
        """
        try:
            # Get location details (latitude, longitude, timezone)
            location_details = get_location_details(city, country)
            birth_data.update(location_details)  # Merge with birth_data

            # Calculate horoscope
            horoscope = self.calculator.calculate_horoscope(name, birth_data)
            return horoscope
        except ValueError as e:
            return {"error": str(e)}

    def generate_detailed_description(self, horoscope: dict) -> str:
        """
        Uses Generative AI to create a detailed description of the horoscope.

        Args:
            horoscope (dict): The raw horoscope data.

        Returns:
            str: A detailed horoscope description.
        """

        try:
            prompt = f"You are a  Vedic Astrologer. Create a detailed horoscope description for the following data:\n{horoscope}"
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating description: {str(e)}"
# Example usage
if __name__ == "__main__":
    astrology = GetAstrology()

    # Input data
    name = "Devaki Adhikari"
    city = "Nainital"
    country = "India"
    birth_data = {
        'year': 1971,
        'month': 5,
        'day': 3,
        'hour': 21,
        'minute': 00
    }

    # Get horoscope
    horoscope_details = astrology.fetch_horoscope(name, birth_data, city, country)

    if "error" not in horoscope_details:
        print("\n=== Horoscope Details ===")
        for key, value in horoscope_details.items():
            print(f"{key}: {value}")

        # Generate detailed description using Generative AI
        detailed_description = astrology.generate_detailed_description(horoscope_details)
        print("\n=== Detailed Horoscope Description ===")
        print(detailed_description)
    else:
        print("Error:", horoscope_details["error"])