import matplotlib.pyplot as plt
import datetime
import os

class DataVisualizer:
    """
    Handles plotting of space weather data.
    """
    def __init__(self):
        print("[DataVisualizer] Initialized.")

    def plot_solar_flares(self, flares_data: list, save_path: str = None):
        """
        Plots solar flare intensities over time.
        """
        if not flares_data:
            print("[DataVisualizer] No solar flare data to plot.")
            return None

        dates = []
        intensities = [] # We'll map X, M, C, B, A to numerical values
        
        # Mapping flare classes to a numerical scale for plotting
        # Higher number means higher intensity
        flare_intensity_map = {'A': 1, 'B': 2, 'C': 3, 'M': 4, 'X': 5}
        
        for flare in flares_data:
            try:
                # Use peakTime for plotting
                dt_object = datetime.datetime.fromisoformat(flare['peakTime'].replace('Z', '+00:00'))
                dates.append(dt_object)
                
                # Get the main class (e.g., 'X' from 'X1.0')
                class_type = flare.get('classType', 'A')[0].upper()
                intensities.append(flare_intensity_map.get(class_type, 0)) # Default to 0 for unknown/invalid
            except (ValueError, KeyError) as e:
                print(f"[DataVisualizer] Skipping malformed flare data: {flare} - Error: {e}")
                continue

        if not dates:
            print("[DataVisualizer] No valid flare data points to plot after parsing.")
            return None

        # Sort data by date
        sorted_data = sorted(zip(dates, intensities))
        dates, intensities = zip(*sorted_data)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(dates, intensities, marker='o', linestyle='-', color='orange', label='Solar Flare Intensity')
        ax.set_title('Solar Flare Activity Over Time', color='white')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Intensity Class (A=1 to X=5)', color='white')
        ax.set_yticks(list(flare_intensity_map.values()))
        ax.set_yticklabels(list(flare_intensity_map.keys()))
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Improve date formatting on x-axis
        fig.autofmt_xdate()

        # Set plot background to dark and text to light for consistency
        fig.patch.set_facecolor('#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['right'].set_color('#2B2B2B')
        ax.spines['top'].set_color('#2B2B2B')
        ax.legend(facecolor='#3C3C3C', edgecolor='white', labelcolor='white')


        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, facecolor=fig.get_facecolor())
            print(f"[DataVisualizer] Solar flare plot saved to {save_path}")
            plt.close(fig) # Close the plot to free memory
            return save_path
        else:
            plt.show()
            return None # If not saved, return None
            
    def plot_geomagnetic_storms(self, gst_data: list, save_path: str = None):
        """
        Plots Geomagnetic Storm Kp-index over time.
        """
        if not gst_data:
            print("[DataVisualizer] No geomagnetic storm data to plot.")
            return None

        dates = []
        kp_indices = []

        for gst in gst_data:
            try:
                # Use startTime for plotting
                dt_object = datetime.datetime.fromisoformat(gst['startTime'].replace('Z', '+00:00'))
                dates.append(dt_object)
                
                # Get max Kp index from each storm event
                max_kp = 0
                for kp_comp in gst.get('allKpIndex', []):
                    max_kp = max(max_kp, kp_comp.get('kpIndex', 0))
                kp_indices.append(max_kp)

            except (ValueError, KeyError) as e:
                print(f"[DataVisualizer] Skipping malformed GST data: {gst} - Error: {e}")
                continue
        
        if not dates:
            print("[DataVisualizer] No valid GST data points to plot after parsing.")
            return None

        # Sort data by date
        sorted_data = sorted(zip(dates, kp_indices))
        dates, kp_indices = zip(*sorted_data)

        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(dates, kp_indices, marker='x', linestyle='--', color='cyan', label='Kp-Index')
        ax.set_title('Geomagnetic Storm Activity (Kp-Index)', color='white')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Kp-Index', color='white')
        ax.set_yticks(range(0, 10)) # Kp-index ranges from 0 to 9
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Improve date formatting on x-axis
        fig.autofmt_xdate()

        # Set plot background to dark and text to light for consistency
        fig.patch.set_facecolor('#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['right'].set_color('#2B2B2B')
        ax.spines['top'].set_color('#2B2B2B')
        ax.legend(facecolor='#3C3C3C', edgecolor='white', labelcolor='white')

        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, facecolor=fig.get_facecolor())
            print(f"[DataVisualizer] Geomagnetic storm plot saved to {save_path}")
            plt.close(fig)
            return save_path
        else:
            plt.show()
            return None

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    print("--- Testing DataVisualizer Module ---")
    visualizer = DataVisualizer()
    
    # Dummy flare data
    dummy_flares = [
        {"classType": "X3.0", "peakTime": "2025-06-25T10:00Z"},
        {"classType": "M5.0", "peakTime": "2025-06-20T15:30Z"},
        {"classType": "C1.0", "peakTime": "2025-06-18T08:00Z"},
        {"classType": "A1.0", "peakTime": "2025-06-10T11:00Z"},
        {"classType": "X1.5", "peakTime": "2025-06-28T12:00Z"},
    ]

    # Dummy GST data
    dummy_gsts = [
        {"startTime": "2025-06-15T01:00Z", "allKpIndex": [{"kpIndex": 4}, {"kpIndex": 5}]},
        {"startTime": "2025-06-16T18:00Z", "allKpIndex": [{"kpIndex": 3}]},
        {"startTime": "2025-06-22T05:00Z", "allKpIndex": [{"kpIndex": 7}, {"kpIndex": 6}]},
        {"startTime": "2025-06-26T09:00Z", "allKpIndex": [{"kpIndex": 2}]},
    ]

    # Define paths relative to the current script for testing
    current_dir = os.path.dirname(__file__)
    reports_dir = os.path.join(os.path.dirname(current_dir), "reports")
    
    flare_plot_path = os.path.join(reports_dir, "test_solar_flares_plot.png")
    gst_plot_path = os.path.join(reports_dir, "test_geomagnetic_storms_plot.png")

    print("\n--- Plotting Solar Flares ---")
    visualizer.plot_solar_flares(dummy_flares, save_path=flare_plot_path)

    print("\n--- Plotting Geomagnetic Storms ---")
    visualizer.plot_geomagnetic_storms(dummy_gsts, save_path=gst_plot_path)

    print("--- DataVisualizer Test Finished ---")