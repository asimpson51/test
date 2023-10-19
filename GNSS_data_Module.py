import numpy as np
import pandas as pd
import glob
from scipy.stats import linregress


def fit_timeseries(tlist, ylist):
    t = np.array(tlist)
    y = np.array(ylist)
    slope, intercept, r_value, p_value, std_err = linregress(t, y)
    velocity = slope
    uncertainty = std_err

    return velocity,uncertainty


def fit_velocities(filename,tname,ename,nname,uname):
    df = pd.read_csv(filename,delim_whitespace=True)
    site = filename.split('/')[-1].split('_')[0]
    v_E, u_E = fit_timeseries(df[tname], df[ename])
    v_N, u_N = fit_timeseries(df[tname], df[nname])
    v_U, u_U = fit_timeseries(df[tname], df[uname])
    velocities_df = pd.DataFrame({
        'Site': [site],
        'E-Velocity': [v_E],
        'N-Velocity': [v_N],
        'U-Velocity': [v_U],
        'E-Uncertainty': u_E,
        'N-Uncertainty': u_N,
        'U-Uncertainty': u_U
    })
        
    return velocities_df
        

def get_coordinates(filename,lat,lon,elev):
    df = pd.read_csv(filename, delim_whitespace=True)
    site = filename.split('/')[-1].split('_')[0]
    lat_mean = df[lat].mean()
    lon_mean = df[lon].mean()
    elevation_mean = df[elev].mean()
    coordinates_df = pd.DataFrame({
        'Site': site,
        'Lat': [lat_mean],
        'Lon': [lon_mean],
        'Elevation': elevation_mean
    })
    
    return coordinates_df
    
def fit_all_velocities(folder, pattern, tname, ename, nname, uname, lat, lon, elev):
    results = []
    file_paths = glob.glob(f"{folder}/{pattern}")
    
    for file_path in file_paths:
        site = file_path.split('/')[-1].split('_')[0]
        velocities = fit_velocities(file_path, tname, ename, nname, uname)
        coordinates = get_coordinates(file_path, lat, lon, elev)
        results.append([
            site,
            velocities['E-Velocity'].values[0],
            velocities['N-Velocity'].values[0],
            velocities['U-Velocity'].values[0],
            velocities['E-Uncertainty'].values[0],
            velocities['N-Uncertainty'].values[0], 
            velocities['U-Uncertainty'].values[0], 
            coordinates['Lat'].values[0], 
            coordinates['Lon'].values[0], 
            coordinates['Elevation'].values[0]
        ])
    
    all_velocities_df = pd.DataFrame(results, columns=[
        'Site',
        'E-Velocity',
        'N-Velocity',
        'U-Velocity',
        'E-Uncertainty',
        'N-Uncertainty',
        'U-Uncertainty',
        'Lat',
        'Lon',
        'Elevation'
    ])
    
    return all_velocities_df

    
    