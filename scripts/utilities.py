import geopandas as gpd

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