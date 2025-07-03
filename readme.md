# AstroMedAI: Space Health & Radiation Risk Assessment

![AstroMedAI GUI Screenshot](image_de16bc.png)
*(Example Screenshot of the AstroMedAI Graphical User Interface)*

## Table of Contents
1.  [Introduction](#introduction)
2.  [Features](#features)
3.  [How It Works](#how-it-works)
    * [Core Modules](#core-modules)
4.  [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Running the Application](#running-the-application)
5.  [Usage Guide](#usage-guide)
    * [Mission Parameters](#mission-parameters)
    * [Space Weather Data](#space-weather-data)
    * [Radiation Risk Assessment](#radiation-risk-assessment)
    * [Space Weather Visualizations](#space-weather-visualizations)
    * [PDF Report Generation](#pdf-report-generation)
    * [Local Data Input (Drag-and-Drop)](#local-data-input-drag-and-drop)
    * [AstroMed Quiz](#astromed-quiz)
6.  [Project Structure](#project-structure)
7.  [Built With](#built-with)
8.  [Future Enhancements](#future-enhancements)
9.  [License](#license)
10. [Contact](#contact)

## 1. Introduction

AstroMedAI is a desktop application developed in Python designed for the preliminary assessment of space radiation risk for crewed missions. It integrates real-time space weather data with user-defined mission parameters to calculate a simplified radiation risk score, visualize space weather events, generate comprehensive reports, and provide an educational quiz mode.

The primary goal of AstroMedAI is to empower mission planners, space health professionals, and space enthusiasts with a tool to quickly understand and estimate potential radiation exposure risks, thereby fostering informed decision-making and raising awareness about space environmental hazards.

## 2. Features

* **Intuitive GUI:** User-friendly interface for inputting mission parameters and viewing results, built with `tkinter`.
* **NASA DONKI API Integration:** Fetches up-to-date data on Solar Flares (FLR), Coronal Mass Ejections (CMEs), and Geomagnetic Storms (GST) from NASA's Space Weather Database Of Notifications, Knowledge, and Information.
* **Radiation Risk Model:** Calculates a simplified mission-specific radiation risk percentage (0-100%) based on duration, orbit type, shielding level, and observed space weather events.
* **Risk Categorization:** Clearly categorizes the calculated risk into "Low," "Moderate," "High," or "Extreme" with color-coded indicators for quick assessment.
* **Space Weather Visualization:** Generates `matplotlib` plots for solar flare intensity and geomagnetic storm Kp-indices over your chosen mission timeframe, helping visualize event severity.
* **PDF Report Generation:** Creates professional PDF summaries of the mission assessment, including all input parameters, risk results, and embedded space weather plots, using `ReportLab`.
* **Local Data Input (Drag-and-Drop):** Supports dragging and dropping local `.json` files (formatted similarly to DONKI API responses) onto the application for custom data analysis.
* **AstroMed Quiz:** An interactive educational quiz mode on space health and radiation to test and expand user knowledge.
* **Standalone Application:** Can be packaged into a standalone executable using PyInstaller.

## 3. How It Works

AstroMedAI functions by orchestrating several interconnected Python modules, each handling a specific part of the risk assessment and presentation process.

### Core Modules

* **`src/astro_med_ai_gui.py`**: The main application script. It initializes the Tkinter GUI, manages user input, orchestrates calls to other modules (API fetch, risk calculation, visualization, reporting, quiz), and displays all results. This is the primary entry point for the application.
* **`src/api_handler.py`**: Responsible for communication with NASA's DONKI API. It sends requests to retrieve space weather data for the specified date range and processes the API responses.
* **`src/risk_model.py`**: Contains the core algorithm for calculating the simplified space radiation risk. It takes into account mission parameters (duration, orbit, shielding) and integrates the fetched solar flare data to produce a risk percentage and category.
* **`src/visualization.py`**: Uses the `matplotlib` library to generate graphical representations of the fetched space weather data (e.g., solar flare intensity plots, geomagnetic storm Kp-index plots). These plots aid in visual analysis.
* **`src/report_generator.py`**: Leverages the `ReportLab` library to dynamically create PDF documents. It compiles mission details, the calculated risk assessment, and embeds the generated space weather plots into a professional, printable report.
* **`src/quiz_mode.py`**: Implements the interactive multiple-choice quiz. It manages questions, user answers, provides feedback, and keeps track of scores, offering an educational component to the application.

## 4. Getting Started

Follow these steps to set up and run AstroMedAI on your local machine.

### Prerequisites

* **Python 3.8+**: The application is developed in Python.
* **Git** (optional, but recommended for cloning the repository).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/AstroMedAI.git](https://github.com/your-username/AstroMedAI.git)
    cd AstroMedAI
    ```
    *(Replace `https://github.com/your-username/AstroMedAI.git` with the actual URL of your repository.)*

2.  **Create a virtual environment:**
    It's highly recommended to use a virtual environment to isolate project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    With your virtual environment activated, install all required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To start the AstroMedAI GUI:

```bash
python -m src.astro_med_ai_gui
