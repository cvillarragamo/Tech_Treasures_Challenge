import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib as plt
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
from shapely.geometry import mapping
import os
from rasterio.plot import show
from ipywidgets import interact, Dropdown

def read_shapefile(path):
    """
    Reads a shapefile and returns it as a GeoDataFrame.
    while printing important information about the shapefile.

    Parameters:
    path (str): The path to the shapefile.
    
    Returns:
    gpd.GeoDataFrame: The contents of the shapefile as a GeoDataFrame.
    """
    try:
        #Number of records, column names and geometry type
        gdf = gpd.read_file(path)
        geom_type= gdf.geom_type.unique()

        print(f"Shapefile loaded with {len(gdf)} records\nColumns: {len(gdf.columns.tolist())}\nGeometry type: {geom_type}")
        
        return gdf
    except Exception as e:
        print(f"Error reading shapefile: {e}")
        return None
    
def to_geodataframe(path, lat_col, lon_col):
    """
    Reads a CSV or XLSX file, converts it into a GeoDataFrame based on latitude and longitude columns.

    Parameters:
    path (str): The path to the file (CSV or XLSX).
    lat_col (str): The name of the latitude column.
    lon_col (str): The name of the longitude column.

    Returns:
    gpd.GeoDataFrame: The resulting GeoDataFrame with geometry based on lat/lon.
    """
         
    try:
        #Determine the file type and load the DF
        if path.endswith('.csv'):
            try:
                df=pd.read_csv(path)
            except UnicodeDecodeError:
                print("Error reading the file with utf-8. Trying with 'latin1' encoding...")
                df=pd.read_csv(path,encoding='latin1')


        elif path.endswith('.xlxs'):
            df=pd.read_excel(path)
        else:
            print(f"Unsupported file format: {path}")
            return None
            
    
    
    #Convert DF to GeoDF
        geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df, geometry= geometry)
        gdf.set_crs(epsg=4269, inplace=True)
        print(f"GeoDataFrame created with {len(gdf)} records\nGeometry type: {gdf.geom_type.unique()}\nCRS={gdf.crs}")
        return gdf
       
    except Exception as e:
        print(f"Error creating GeoDataFrame: {e}")
        return None


                 
def check_transform_crs(gdf, target_crs='EPSG:4269'):
    """
    Check the coordinate reference system (CRS) of a GeoDataFrame and transform it
    to the target CRS if it is different.
    
    Parameters:
        gdf (geopandas.GeoDataFrame): The GeoDataFrame to check and transform.
        target_crs (str): The target CRS to which the GeoDataFrame should be transformed if needed.

    Returns:
        geopandas.GeoDataFrame: The GeoDataFrame with the CRS adjusted to the target CRS.
    """
    current_crs = gdf.crs.to_string()
    if current_crs != target_crs:
        print(f'Transforming from {current_crs} to {target_crs}.')
        return gdf.to_crs(target_crs)
    else:
        print('CRS is already correct.')
        return gdf
################################################## ~~~~~~~~~~~~~~~~~~~~~~ ###################################
### RASTER processing ####################


def process_and_reproject_rasters(raster_paths, polygon_gdf, output_directory, target_crs='EPSG:4269'):
    """
    Processes a list of rasters by ensuring they all have the CRS EPSG:4269,
    reprojects if necessary, and crops the rasters using a reference polygon.

    Args:
    raster_paths (list of str): Paths to the raster files.
    polygon_shapefile (str): Path to the shapefile containing the cropping polygon.
    output_directory (str): Directory where the cropped and reprojected rasters will be saved.
    target_crs (str): The target CRS to standardize all rasters (default 'EPSG:4269').
    """
    
    # Get the polygon as a geometric object
    geometry = polygon_gdf.iloc[0].geometry
    geojson = [mapping(geometry)]
    
    for raster_path in raster_paths:
        with rasterio.open(raster_path) as src:
            src_crs = src.crs
            if src_crs != target_crs:
                # Calculate the transformation needed and the new dimensions
                transform, width, height = calculate_default_transform(
                    src.crs, target_crs, src.width, src.height, *src.bounds)
                kwargs = src.meta.copy()
                kwargs.update({
                    'crs': target_crs,
                    'transform': transform,
                    'width': width,
                    'height': height
                })
                
                # Reproject the raster
                reprojected_path = f"{output_directory}/reprojected_{os.path.basename(raster_path)}"
                with rasterio.open(reprojected_path, 'w', **kwargs) as dst:
                    for i in range(1, src.count + 1):
                        reproject(
                            source=rasterio.band(src, i),
                            destination=rasterio.band(dst, i),
                            src_transform=src.transform,
                            src_crs=src.crs,
                            dst_transform=transform,
                            dst_crs=target_crs,
                            resampling=Resampling.nearest)
                raster_path = reprojected_path
            
            # Crop the raster using the polygon
            with rasterio.open(raster_path) as src:
                out_image, out_transform = mask(src, geojson, crop=True)
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform
                })
                
                output_path = f"{output_directory}/cropped_{os.path.basename(raster_path)}"
                with rasterio.open(output_path, "w", **out_meta) as dest:
                    dest.write(out_image)

    print("All rasters processed to CRS EPSG:4269 and cropped as specified.")


## Plotting Rasters

def plot_raster(raster_path, poi):
    """
    Plot a raster file with a point of interest overlay.
    
    Args:
    raster_path (str): The path to the raster file.
    poi (GeoDataFrame): A GeoDataFrame containing the point of interest with geometry and label.
    
    Displays a raster plot with a point of interest marked on it.
    """
    with rasterio.open(raster_path) as src:
        fig, ax = plt.subplots(figsize=(10, 7))
        show(src, ax=ax, title=os.path.basename(raster_path))
        
        ##Point of interest
        x, y = poi.geometry.x.iloc[0], poi.geometry.y.iloc[0]
        ax.scatter(x, y, color='blue', marker='o', s=70) 
        ax.text(x, y, "Wicheeda", fontsize=10, ha='left', va='top', color='blue')
        
        plt.show()

def list_rasters(directory):
    """
    List all TIFF files in a specified directory.

    Args:
    directory (str): The directory path that contains TIFF files.

    Returns:
    dict: A dictionary mapping file names to their full paths.
    """
    return {os.path.basename(f): os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.tif')}

def interactive_plot_raster(directory, poi):
    """
    Create an interactive raster plot selector with a predefined point of interest.

    Args:
    directory (str): The directory from which to list and select raster files.
    poi (GeoDataFrame): The GeoDataFrame containing the point of interest data.
    
    Displays a dropdown widget to select different raster files for plotting.
    """
    rasters = list_rasters(directory)
    if rasters:
        raster_dropdown = Dropdown(options=list(rasters.keys()))
        def update_plot(change):
            plot_raster(rasters[change.new], poi)
        raster_dropdown.observe(update_plot, names='value')
        display(raster_dropdown)
        plot_raster(list(rasters.values())[0], poi)  # Plot the first raster initially
    else:
        print("No TIFF files found in the specified directory.")