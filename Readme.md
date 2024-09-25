# Tech Treasures Challenge - Critical Minerals Exploration Dashboard

## Overview
This repository is part of the **[Tech Treasures Challenge](https://getech.com/news/getech-collaborates-with-thinkonward-to-develop-ai-powered-critical-minerals-exploration-dashboard/?utm_campaign=2024%20Challenges%20and%20Bounties&utm_content=304316993&utm_medium=social&utm_source=linkedin&hss_channel=lcp-40889185)**. The goal is to develop an AI-powered dashboard for critical minerals exploration.

Throughout this project, several approaches were explored in the quest to build a model for predicting rare earth element (REE) deposits in British Columbia. Initial ideas focused on incorporating raster data, linear features, and various geochemical and geological attributes into ensemble models. A PCA was conducted to reduce dimensionality, and unsupervised models like K-means were applied. Unfortunately, these models did not yield significant clustering results, likely due to the complexity of the data or insufficient training samples.

A Random Forest model was later implemented, but it performed poorly, potentially due to the added complexity of multiple categories in the dataset. The analysis centered on 65 points of Critical Mineral showings, divided into mineralized and non-mineralized categories with varying confidence levels. While this seemed to provide a balanced dataset, it may have introduced more complexity than expected. Going forward, the model will be refined outside of the challenge, reducing the categories to two and utilizing the `grid_no_bc` mesh to simplify the process.

## Repository Structure
- **`datasets/`**: Contains all relevant datasets, including:
  - **raster** 
  - **shapefiles**
- **`documents/`**: Reference materials and auxiliary documents.
- **`models/`**: Any saved models used during the analysis process.
- **`scripts/`**: Python scripts for data preprocessing and utility functions.

### Notebooks:
1. **`1_Data_Collection_Cleaning.ipynb`**: Data cleaning and transformation steps.
2. **`2_Tech_Treassure_for_REE_minerals.ipynb`**: Main notebook with the analysis pipeline for REE exploration.
3. **`3_legacy.ipynb`**: Contains earlier versions and approaches that were explored but not fully implemented.

### Dashboard:
- **`dash.py`**: This file contains the Streamlit dashboard code. It visualizes the critical mineral exploration data and allows users to interact with geological layers and view predictions.
  - To run the dashboard locally:
    ```bash
    streamlit run dash.py
    ```
  - You can also access the deployed version of the dashboard [here](#) (add the deployment link).

    ```
### Map Outputs:
- **`predicted_prospectivity_map_discrete.tif`**: The resulting prospectivity map generated from the analysis.

## Key Insights:
The main focus of the project was integrating various datasets and applying Machine Learning techniques to predict areas with REE potential. While some initial results were produced, certain challenges were encountered with the available data, and further refinement is required. The dashboard represents the current state of the analysis and offers a platform to visualize the results and interact with the data.

## Contact
For any inquiries or feedback, please reach out to **cvillaragamo@gmail.com**.

---

This project was an enriching experience, though some ideas could not be fully implemented within the timeframe and computational constraints. Further work will focus on improving the model and refining the dashboard.


## Next steps
- **Integrating Geophysical Data:** Expand the current dataset by adding gravimetry and magnetic field data.
- **Developing Insights from Data:** Leverage the cleaned and enriched datasets to generate meaningful insights for critical mineral exploration.
- **Potential AI and ML Integration:** Explore the possibility of incorporating AI and ML models for prediction and analysis, though the current focus is primarily on data preparation and understanding.

## Contact
cvillaragamo@gmail.com

---