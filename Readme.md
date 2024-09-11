# Tech Treasures Challenge - Critical Minerals Exploration Dashboard

## Overview
This repository is part of the **[Tech Treasures Challenge](https://getech.com/news/getech-collaborates-with-thinkonward-to-develop-ai-powered-critical-minerals-exploration-dashboard/?utm_campaign=2024%20Challenges%20and%20Bounties&utm_content=304316993&utm_medium=social&utm_source=linkedin&hss_channel=lcp-40889185)**, a collaborative effort between Getech and ThinkOnward. The challenge focuses on developing an AI-powered dashboard for critical minerals exploration, leveraging data science and potential fields data.

## Challenge Description
The goal of the Tech Treasures Challenge is to create an innovative dashboard for mineral exploration using data science tools. Participants will work with various datasets and methodologies, focusing on critical minerals (CM) through an analysis pipeline that includes data cleaning, spatial processing, and, eventually, machine learning (ML) integration.

- **Objective:** Develop a critical minerals exploration dashboard
- **Duration:** August - September 2024
- **Submission Deadline:** End of September 2024

## Project Status
**Ongoing**
- **Data Cleaning and Preprocessing:**  
  The first part of the project is dedicated to cleaning and preparing the raster datasets for analysis. This includes:
  - Reprojection of rasters to a fixed CRS (`EPSG:4269`).
  - Cropping rasters to specific geological regions, such as the carbonatite-type deposits in British Columbia.
  - Initial data exploration focusing on radiometric data, with plans to add other geophysical data (e.g., gravimetry, magnetic total field).

- **File Structure:**  
  The repository is structured as follows:
  - `datasets/raster/`: Contains raster data, including subfolders for **originals** and **cropped_reprojected** rasters.
  - `datasets/shp/`: Shapefiles used in the project.
  - `scripts/`: Python scripts used for preprocessing, utilities, and data handling (`utilities.py` holds frequently used functions for raster processing and metadata extraction).
  - `documents/`: Holds reference documents and auxiliary files.
  - Notebooks:
    - `1_Data_Collection_Cleaning.ipynb`: Focuses on data collection, cleaning, and transformation for further analysis.
    - `geochem.ipynb`: Ongoing geochemical analysis for rare earth elements (REE) deposits [ON HOLD]

## Next steps
- **Integrating Geophysical Data:** Expand the current dataset by adding gravimetry and magnetic field data.
- **Developing Insights from Data:** Leverage the cleaned and enriched datasets to generate meaningful insights for critical mineral exploration.
- **Potential AI and ML Integration:** Explore the possibility of incorporating AI and ML models for prediction and analysis, though the current focus is primarily on data preparation and understanding.

## Contact
cvillaragamo@gmail.com

---

*This project is part of a month-long challenge and is currently under active development. Stay tuned for updates!*
