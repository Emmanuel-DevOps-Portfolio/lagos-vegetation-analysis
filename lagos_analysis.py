import ee
import geemap
import matplotlib.pyplot as plt
import numpy as np

ee.Initialize(project='gee-lagos-portfolio')

# ── Area of Interest ──────────────────────────────────────────
lagos = ee.Geometry.Rectangle([3.1, 6.4, 3.6, 6.75])

# ── Helper: scale Landsat 8 bands ────────────────────────────
def scale_bands(image):
    optical = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    return image.addBands(optical, None, True)

def get_collection(start, end):
    return (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
              .filterBounds(lagos)
              .filterDate(start, end)
              .filter(ee.Filter.lt('CLOUD_COVER', 10))
              .map(scale_bands)
              .median())

# ── Compute Indices ───────────────────────────────────────────
def compute_indices(start, end):
    img = get_collection(start, end)

    nir  = img.select('SR_B5')
    red  = img.select('SR_B4')
    swir = img.select('SR_B6')

    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
    ndbi = swir.subtract(nir).divide(swir.add(nir)).rename('NDBI')

    # Water mask
    water_mask = ndvi.gt(-0.1)
    return (ndvi.updateMask(water_mask),
            ndbi.updateMask(water_mask))

print("Processing 2015 imagery...")
ndvi_2015, ndbi_2015 = compute_indices('2015-01-01', '2015-12-31')

print("Processing 2024 imagery...")
ndvi_2024, ndbi_2024 = compute_indices('2024-01-01', '2024-12-31')

# ── Change Layers ─────────────────────────────────────────────
ndvi_change = ndvi_2024.subtract(ndvi_2015).rename('NDVI_Change')
ndbi_change = ndbi_2024.subtract(ndbi_2015).rename('NDBI_Change')

# ── Statistics ────────────────────────────────────────────────
print("Calculating statistics...")

def get_mean(image):
    result = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=lagos,
        scale=30,
        maxPixels=1e9
    )
    return result.getInfo()

ndvi_2015_mean = get_mean(ndvi_2015).get('NDVI', 0)
ndvi_2024_mean = get_mean(ndvi_2024).get('NDVI', 0)
ndbi_2015_mean = get_mean(ndbi_2015).get('NDBI', 0)
ndbi_2024_mean = get_mean(ndbi_2024).get('NDBI', 0)

print(f"\n{'='*45}")
print(f"  LAGOS LAND COVER CHANGE — 2015 vs 2024")
print(f"{'='*45}")
print(f"  Mean NDVI 2015 : {ndvi_2015_mean:.4f}")
print(f"  Mean NDVI 2024 : {ndvi_2024_mean:.4f}")
print(f"  NDVI Change    : {ndvi_2024_mean - ndvi_2015_mean:.4f}  {'↓ vegetation loss' if ndvi_2024_mean < ndvi_2015_mean else '↑ vegetation gain'}")
print(f"{'─'*45}")
print(f"  Mean NDBI 2015 : {ndbi_2015_mean:.4f}")
print(f"  Mean NDBI 2024 : {ndbi_2024_mean:.4f}")
print(f"  NDBI Change    : {ndbi_2024_mean - ndbi_2015_mean:.4f}  {'↑ urban expansion' if ndbi_2024_mean > ndbi_2015_mean else '↓ urban decrease'}")
print(f"{'='*45}\n")

# ── Bar Chart ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle('Lagos Land Cover Change — 2015 vs 2024', fontsize=14)

axes[0].bar(['2015', '2024'], [ndvi_2015_mean, ndvi_2024_mean],
            color=['green', 'red'], width=0.4)
axes[0].set_title('Mean NDVI (Vegetation)')
axes[0].set_ylabel('NDVI Value')
axes[0].set_ylim(0, 0.5)

axes[1].bar(['2015', '2024'], [ndbi_2015_mean, ndbi_2024_mean],
            color=['blue', 'orange'], width=0.4)
axes[1].set_title('Mean NDBI (Built-up Area)')
axes[1].set_ylabel('NDBI Value')

plt.tight_layout()
plt.savefig('lagos_change_chart.png', dpi=150)
print("Chart saved as lagos_change_chart.png")

# ── Interactive Map ───────────────────────────────────────────
print("Building interactive map...")
Map = geemap.Map(center=[6.55, 3.35], zoom=11)

ndvi_vis  = {'min': 0,    'max': 0.7,  'palette': ['red', 'yellow', 'green']}
ndbi_vis  = {'min': -0.3, 'max': 0.3,  'palette': ['green', 'white', 'orange']}
change_vis = {'min': -0.3, 'max': 0.3, 'palette': ['red', 'white', 'green']}

Map.addLayer(ndvi_2015,   ndvi_vis,   'NDVI 2015',              False)
Map.addLayer(ndvi_2024,   ndvi_vis,   'NDVI 2024',              False)
Map.addLayer(ndvi_change, change_vis, 'NDVI Change 2015–2024',  True)
Map.addLayer(ndbi_2015,   ndbi_vis,   'NDBI 2015',              False)
Map.addLayer(ndbi_2024,   ndbi_vis,   'NDBI 2024',              False)
Map.addLayer(ndbi_change, change_vis, 'NDBI Change 2015–2024',  False)

Map.addLayerControl()
Map.save('lagos_analysis_map.html')
print("Map saved as lagos_analysis_map.html")
print("\nAll done! Open lagos_analysis_map.html in your browser.")
