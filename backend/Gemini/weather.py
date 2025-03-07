from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Tuple, Dict
from dataclasses import dataclass

@dataclass
class SeasonDates:
    spring: Tuple[int, int]
    summer: Tuple[int, int]
    autumn: Tuple[int, int]
    winter: Tuple[int, int]

class WeatherAPI:
    def __init__(self):
        # Initialize season dates
        self.SEASON_DATES = {
            "northern": SeasonDates(
                spring=(3, 20),
                summer=(6, 21),
                autumn=(9, 22),
                winter=(12, 21)
            ),
            "southern": SeasonDates(
                spring=(9, 22),
                summer=(12, 21),
                autumn=(3, 20),
                winter=(6, 21)
            )
        }

    def get_season(self, timezone: str = "UTC", hemisphere: str = "northern") -> str:
        """
        Get the current season based on timezone and hemisphere.
        
        Args:
            timezone: String representing the timezone (e.g., "America/New_York")
            hemisphere: Either "northern" or "southern"
        
        Returns:
            String representing the current season
        
        Raises:
            ValueError: If hemisphere is invalid or timezone is not found
        """
        # Validate hemisphere
        hemisphere = hemisphere.lower()
        if hemisphere not in ["northern", "southern"]:
            raise ValueError("Hemisphere must be either 'northern' or 'southern'")

        # Get current date in specified timezone
        try:
            current_date = datetime.now(ZoneInfo(timezone))
        except Exception:
            raise ValueError(f"Invalid timezone: {timezone}")

        month = current_date.month
        day = current_date.day
        current = (month, day)

        # Get season dates for specified hemisphere
        dates = self.SEASON_DATES[hemisphere]

        # Check which season it is
        if self._is_between(current, dates.winter, dates.spring):
            return "Winter"
        elif self._is_between(current, dates.spring, dates.summer):
            return "Spring"
        elif self._is_between(current, dates.summer, dates.autumn):
            return "Summer"
        elif self._is_between(current, dates.autumn, dates.winter):
            return "Autumn"
        else:
            return "Winter"  # Default to winter for dates after winter start

    def _is_between(self, current: Tuple[int, int], start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """
        Check if current date falls between start and end dates.
        Handles year wrap-around cases.
        """
        def _to_days(date_tuple: Tuple[int, int]) -> int:
            """Convert (month, day) to days since start of year"""
            month, day = date_tuple
            days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return sum(days_in_month[:month]) + day

        current_days = _to_days(current)
        start_days = _to_days(start)
        end_days = _to_days(end)

        if start_days <= end_days:
            return start_days <= current_days < end_days
        else:  # Date range crosses year boundary
            return current_days >= start_days or current_days < end_days

if __name__ == "__main__":
    # Example usage
    try:
        weather = WeatherAPI()
        season = weather.get_season("America/New_York", "northern")
        print(f"Current season: {season}")
    except ValueError as e:
        print(f"Error: {e}")