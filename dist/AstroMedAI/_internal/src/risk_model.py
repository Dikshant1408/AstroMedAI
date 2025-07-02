import datetime

class SpaceRadiationRiskModel:
    """
    Calculates a simplified space radiation risk score based on mission parameters
    and solar flare activity.
    """

    # Base risk factors per day for different orbit types (conceptual values)
    BASE_RISK_PER_DAY = {
        "LEO": 0.005,           # Low Earth Orbit (some shielding from Earth's magnetosphere)
        "GEO": 0.015,           # Geosynchronous Earth Orbit (more exposed than LEO)
        "Lunar Orbit": 0.05,    # Outside Earth's magnetosphere, but often shorter missions
        "Mars Transit": 0.1     # Deep space, long duration, highly exposed to GCRs and SPEs
    }

    # Shielding effectiveness (conceptual reduction factors applied to total risk)
    SHIELDING_FACTOR = {
        "Minimal": 1.0, # No reduction (e.g., thin spacecraft skin)
        "Moderate": 0.7, # 30% reduction (e.g., standard habitation module)
        "High": 0.4     # 60% reduction (e.g., storm shelter, water shielding)
    }

    # Impact of solar flares based on their X-ray intensity class (conceptual added risk percentage)
    FLARE_IMPACT_BASE = {
        "X": 25.0, # High intensity X-class flare adds significant risk
        "M": 12.0, # Medium intensity M-class flare adds moderate risk
        "C": 5.0,  # Low intensity C-class flare adds minor risk
        "B": 0.0,
        "A": 0.0
    }
    
    MIN_FLARE_CLASS_FOR_RISK = "C" # Only C-class or higher impact risk

    def __init__(self):
        print("[RiskModel] Initialized SpaceRadiationRiskModel.")

    def _get_flare_risk_contribution(self, flare_intensity_class: str) -> float:
        """
        Determines the risk contribution from a single solar flare based on its X-ray class.
        """
        if not flare_intensity_class or not isinstance(flare_intensity_class, str):
            return 0.0
        
        main_class = flare_intensity_class[0].upper()
        
        if main_class in self.FLARE_IMPACT_BASE and \
           list(self.FLARE_IMPACT_BASE.keys()).index(main_class) >= \
           list(self.FLARE_IMPACT_BASE.keys()).index(self.MIN_FLARE_CLASS_FOR_RISK):
            return self.FLARE_IMPACT_BASE.get(main_class, 0.0)
        
        return 0.0

    def calculate_risk(self,
                       duration_days: int,
                       orbit_type: str,
                       shielding_level: str,
                       solar_flare_data: list = None) -> tuple[float, str]:
        """
        Calculates the space radiation risk score.

        Args:
            duration_days (int): Duration of the mission in days.
            orbit_type (str): Type of orbit ("LEO", "GEO", "Lunar Orbit", "Mars Transit").
            shielding_level (str): Level of shielding ("Minimal", "Moderate", "High").
            solar_flare_data (list): List of dictionaries, each representing a flare event.

        Returns:
            tuple[float, str]: A tuple containing the total risk score (0-100%) and a risk category string.
        """
        if duration_days <= 0:
            return 0.0, "No Risk (Duration 0)"

        if orbit_type not in self.BASE_RISK_PER_DAY:
            raise ValueError(f"Invalid orbit type: {orbit_type}. Expected one of: {list(self.BASE_RISK_PER_DAY.keys())}")
        if shielding_level not in self.SHIELDING_FACTOR:
            raise ValueError(f"Invalid shielding level: {shielding_level}. Expected one of: {list(self.SHIELDING_FACTOR.keys())}")

        base_risk_percentage = duration_days * self.BASE_RISK_PER_DAY[orbit_type]
        print(f"[RiskModel] Base risk for {duration_days} days in {orbit_type}: {base_risk_percentage:.2f}%")

        flare_risk_contribution = 0.0
        if solar_flare_data:
            for flare in solar_flare_data:
                intensity = flare.get('classType')
                if intensity:
                    flare_risk_contribution += self._get_flare_risk_contribution(intensity)
            print(f"[RiskModel] Total flare contribution (unshielded): {flare_risk_contribution:.2f}%")

        unshielded_total_risk = base_risk_percentage + flare_risk_contribution

        total_risk_score = unshielded_total_risk * self.SHIELDING_FACTOR[shielding_level]
        print(f"[RiskModel] Risk after {shielding_level} shielding: {total_risk_score:.2f}%")

        total_risk_score = min(total_risk_score, 100.0)
        total_risk_score = max(total_risk_score, 0.0)

        if total_risk_score < 20:
            risk_category = "Low"
        elif total_risk_score < 50:
            risk_category = "Moderate"
        elif total_risk_score < 80:
            risk_category = "High"
        else:
            risk_category = "Extreme"

        print(f"[RiskModel] Final calculated risk: {total_risk_score:.2f}% ({risk_category})")
        return total_risk_score, risk_category

# Example Usage for testing this module independently
if __name__ == "__main__":
    print("--- Testing SpaceRadiationRiskModel Module ---")
    model = SpaceRadiationRiskModel()

    dummy_flares = [
        {"classType": "X3.0", "peakTime": "2025-06-25T10:00Z"},
        {"classType": "M5.0", "peakTime": "2025-06-20T15:30Z"},
        {"classType": "C1.0", "peakTime": "2025-06-18T08:00Z"},
        {"classType": "B2.0", "peakTime": "2025-06-10T11:00Z"},
    ]

    score1, category1 = model.calculate_risk(365, "LEO", "Moderate", solar_flare_data=[])
    print(f"Test 1 (LEO, 1yr, Moderate, No Sig Flares): {score1:.2f}% ({category1})\n")

    score2, category2 = model.calculate_risk(730, "Mars Transit", "Minimal", solar_flare_data=dummy_flares)
    print(f"Test 2 (Mars, 2yr, Minimal, With Flares): {score2:.2f}% ({category2})\n")

    score3, category3 = model.calculate_risk(30, "Lunar Orbit", "High", solar_flare_data=dummy_flares)
    print(f"Test 3 (Lunar, 30d, High, With Flares): {score3:.2f}% ({category3})\n")

    score4, category4 = model.calculate_risk(0, "LEO", "Minimal")
    print(f"Test 4 (Zero Duration): {score4:.2f}% ({category4})\n")

    try:
        model.calculate_risk(100, "Invalid Orbit", "Moderate")
    except ValueError as e:
        print(f"Test 5 (Invalid Orbit): Caught expected error: {e}\n")

    print("--- SpaceRadiationRiskModel Test Finished ---")