import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

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
