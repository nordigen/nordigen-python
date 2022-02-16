
from typing import Dict, Optional


class DataFilter:

    def filter_payload(self, data: Optional[Dict]) -> Dict:
        """
        Filter falsy values from dictionary

        Args:
            data (Optional[Dict]): data dict

        Returns:
            Dict: filtered dictionary
        """
        if data is None:
            return {}

        return {k: v for (k,v) in data.items() if v}

