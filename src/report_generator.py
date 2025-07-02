# astro_med_ai/src/report_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import datetime

class PDFReportGenerator:
    """
    Generates a PDF report of the mission risk analysis.
    """
    def __init__(self):
        print("[PDFReportGenerator] Initialized.")
        self.styles = getSampleStyleSheet()

        # Define custom styles by inheriting from existing ones using the .add() method.
        # Ensure custom names are unique to avoid KeyError for already defined styles.
        
        # Custom Heading1
        self.styles.add(ParagraphStyle(
            name='Heading1AstroMed', # Using a unique name 'AstroMed' suffix
            parent=self.styles['h1'], # Inherit from default h1
            alignment=TA_CENTER,
            spaceAfter=14,
            textColor=colors.darkblue
        ))
        
        # Custom BodyText (inherits from 'Normal')
        self.styles.add(ParagraphStyle(
            name='BodyTextAstroMed', # Using a unique name 'AstroMed' suffix
            parent=self.styles['Normal'], # Inherit from Normal
            spaceAfter=6,
            leading=14,
            alignment=TA_LEFT
        ))

        # Custom BoldBodyText (inherits from our custom BodyTextAstroMed style)
        self.styles.add(ParagraphStyle(
            name='BoldBodyTextAstroMed', # Using a unique name 'AstroMed' suffix
            parent=self.styles['BodyTextAstroMed'], # Inherit from our custom body text
            fontName='Helvetica-Bold'
        ))

    def generate_report(self,
                        mission_data: dict,
                        risk_score: float,
                        risk_category: str,
                        flare_plot_path: str = None,
                        gst_plot_path: str = None):
        """
        Generates a PDF report summarizing mission details, risk, and space weather.

        Args:
            mission_data (dict): Dictionary containing mission details.
            risk_score (float): Calculated risk score.
            risk_category (str): Categorized risk (Low, Moderate, High, Extreme).
            flare_plot_path (str): Path to the generated solar flare plot image.
            gst_plot_path (str): Path to the generated geomagnetic storm plot image.
        """
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        report_filename = f"AstroMedAI_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(reports_dir, report_filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []

        # Title
        story.append(Paragraph("AstroMedAI Mission Risk Assessment Report", self.styles['Heading1AstroMed']))
        story.append(Spacer(1, 0.2 * inch))

        # Date of Report
        story.append(Paragraph(f"<b>Date:</b> {datetime.date.today().strftime('%Y-%m-%d')}", self.styles['BodyTextAstroMed']))
        story.append(Spacer(1, 0.1 * inch))

        # Mission Details
        story.append(Paragraph("<u>Mission Details:</u>", self.styles['BoldBodyTextAstroMed']))
        for key, value in mission_data.items():
            if key == "start_date" or key == "end_date":
                # Assuming start_date and end_date are datetime objects, format them
                if isinstance(value, datetime.date):
                     value = value.strftime("%Y-%m-%d")
                elif isinstance(value, str): # If they are already strings, just use them
                    pass
                else: # Fallback for unexpected types
                    value = str(value)
            story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", self.styles['BodyTextAstroMed']))
        story.append(Spacer(1, 0.2 * inch))

        # Risk Assessment
        story.append(Paragraph("<u>Radiation Risk Assessment:</u>", self.styles['BoldBodyTextAstroMed']))
        story.append(Paragraph(f"<b>Calculated Risk Score:</b> {risk_score:.2f}%", self.styles['BodyTextAstroMed']))
        story.append(Paragraph(f"<b>Risk Category:</b> <font color='{self._get_category_color(risk_category)}'>{risk_category.upper()}</font>", self.styles['BodyTextAstroMed']))
        story.append(Spacer(1, 0.2 * inch))
        
        story.append(Paragraph("<i>Note: This risk assessment is based on a simplified model and current space weather data from NASA's DONKI API. Actual risks may vary.</i>", self.styles['BodyTextAstroMed']))
        story.append(Spacer(1, 0.2 * inch))

        # Space Weather Data Visualizations
        story.append(Paragraph("<u>Space Weather Visualizations:</u>", self.styles['BoldBodyTextAstroMed']))
        story.append(Spacer(1, 0.1 * inch))
        
        if flare_plot_path and os.path.exists(flare_plot_path):
            try:
                img = Image(flare_plot_path, width=5.5*inch, height=3.5*inch)
                story.append(Paragraph("<b>Solar Flare Activity:</b>", self.styles['BodyTextAstroMed']))
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"<i>Could not load Solar Flare plot: {e}</i>", self.styles['BodyTextAstroMed']))
                print(f"[PDFReportGenerator] Error loading flare plot: {e}")
        else:
            story.append(Paragraph("<i>No Solar Flare plot available.</i>", self.styles['BodyTextAstroMed']))
            
        if gst_plot_path and os.path.exists(gst_plot_path):
            try:
                img = Image(gst_plot_path, width=5.5*inch, height=3.5*inch)
                story.append(Paragraph("<b>Geomagnetic Storm Activity (Kp-Index):</b>", self.styles['BodyTextAstroMed']))
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"<i>Could not load Geomagnetic Storm plot: {e}</i>", self.styles['BodyTextAstroMed']))
                print(f"[PDFReportGenerator] Error loading GST plot: {e}")
        else:
            story.append(Paragraph("<i>No Geomagnetic Storm plot available.</i>", self.styles['BodyTextAstroMed']))
            
        story.append(Spacer(1, 0.2 * inch))

        # Build PDF
        try:
            doc.build(story)
            print(f"[PDFReportGenerator] Report successfully generated at: {filepath}")
            return filepath
        except Exception as e:
            print(f"[PDFReportGenerator] Error generating PDF report: {e}")
            return None

    def _get_category_color(self, category: str) -> str:
        """Returns a color hex string based on risk category."""
        category_map = {
            "Low": "#28a745",       # Green
            "Moderate": "#ffc107",  # Yellow/Orange
            "High": "#fd7e14",      # Orange-red
            "Extreme": "#dc3545"    # Red
        }
        return category_map.get(category, "#6c757d") # Default to gray

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    print("--- Testing PDFReportGenerator Module ---")
    generator = PDFReportGenerator()

    # Dummy Data
    dummy_mission_data = {
        "mission_name": "Mars Reconnaissance",
        "duration_days": 600,
        "orbit_type": "Mars Transit",
        "shielding_level": "Moderate",
        "crew_size": 4,
        "start_date": datetime.date(2026, 3, 1),
        "end_date": datetime.date(2027, 10, 21),
    }
    dummy_risk_score = 75.5
    dummy_risk_category = "High"

    # Create dummy plots for testing
    temp_reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(temp_reports_dir, exist_ok=True)
    
    dummy_flare_plot_path = os.path.join(temp_reports_dir, "dummy_flare_plot.png")
    dummy_gst_plot_path = os.path.join(temp_reports_dir, "dummy_gst_plot.png")

    try:
        from matplotlib import pyplot as plt
        plt.figure(figsize=(6, 4))
        plt.plot([1, 2, 3], [4, 5, 6])
        plt.title("Dummy Flare Plot")
        plt.savefig(dummy_flare_plot_path)
        plt.close()

        plt.figure(figsize=(6, 4))
        plt.plot([1, 2, 3], [6, 5, 4])
        plt.title("Dummy GST Plot")
        plt.savefig(dummy_gst_plot_path)
        plt.close()
        print("Generated dummy plots for testing PDF.")
    except ImportError:
        print("Matplotlib not installed. Skipping dummy plot generation for PDF test.")
        dummy_flare_plot_path = None
        dummy_gst_plot_path = None
        
    generated_filepath = generator.generate_report(
        dummy_mission_data,
        dummy_risk_score,
        dummy_risk_category,
        flare_plot_path=dummy_flare_plot_path,
        gst_plot_path=dummy_gst_plot_path
    )

    if generated_filepath:
        print(f"Report generated successfully: {generated_filepath}")
        # Clean up dummy plots
        if os.path.exists(dummy_flare_plot_path):
            os.remove(dummy_flare_plot_path)
        if os.path.exists(dummy_gst_plot_path):
            os.remove(dummy_gst_plot_path)
    else:
        print("Failed to generate report.")
    
    print("--- PDFReportGenerator Test Finished ---")