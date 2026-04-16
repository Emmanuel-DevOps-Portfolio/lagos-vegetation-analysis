# Lagos Vegetation & Urban Change Analysis (2015–2024)

A remote sensing analysis of land cover change in Lagos, Nigeria using 
Google Earth Engine, Landsat 8 imagery, and Python.

## Study Area
Lagos, Nigeria — one of Africa's fastest growing megacities.
Bounding box: 3.1, 6.4, 3.6, 6.75

## Objectives
Quantify vegetation change using NDVI (Normalized Difference Vegetation Index)
Detect urban expansion using NDBI (Normalized Difference Built-up Index)
Compare land cover between 2015 and 2024 using Landsat 8 cloud-free composites

## Key Findings

| Metric | 2015 | 2024 | Change |
|--------|------|------|--------|
| Mean NDVI (Vegetation) | 0.3664 | 0.3876 | +0.0212 |
| Mean NDBI (Built-up) | -0.0834 | -0.0501 | +0.0333 |

Urban expansion confirmed. NDBI increased by 0.033, indicating 
significant growth in built-up surfaces across Lagos between 2015 and 2024.

Vegetation dynamics. A marginal NDVI increase suggests urban greening 
and peri-urban vegetation regrowth partially offset core vegetation loss, 
consistent with Lagos's rapid but uneven urban development pattern.

## Methodology
1. Filtered Landsat 8 Collection 2 imagery for cloud cover < 10%
2. Applied surface reflectance scaling factors
3. Computed NDVI and NDBI for annual cloud-free composites
4. Applied water mask (NDVI > -0.1) to exclude lagoon and ocean
5. Calculated mean index values over the study area
6. Visualised spatial change patterns using geemap

## Tools & Libraries
Google Earth Engine — satellite data access
geemap — interactive GEE mapping in Python
Landsat 8 Collection 2 Level 2 (USGS)
Python: earthengine-api, matplotlib, numpy

## Setup & Usage

```bash
git clone https://github.com/YOUR_USERNAME/lagos-vegetation-analysis.git
cd lagos-vegetation-analysis

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

earthengine authenticate

python3 lagos_analysis.py
```

## Outputs
lagos_analysis_map.html — Interactive map with 6 toggleable layers
lagos_change_chart.png — Bar chart comparing NDVI and NDBI values

## Author
Emmanuel Ulu — Geologist & Cloud/DevOps Engineer  
MSc Geoinformatics Applicant, Trier University