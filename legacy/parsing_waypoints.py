import pandas as pd
from dronekit import connect, VehicleMode, LocationGlobalRelative

connection_string = ''
# Start SITL if no connection string specified
if not connection_string:
    print('Starting SITL...')
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def move_drone(location : int, df):
    if location > df.shape[0]:
        return "o no"

    point = LocationGlobalRelative(df.loc[0][location], df.loc[1][location], 10)
    vehicle.simple_goto(point, groundspeed=10)

def parse_txt_drone():
    df = pd.read_table('Coordinatess.txt', sep='\t', skiprows=[0], header=None)
    df = df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7, -1]], axis=1)
    print(df.shape)
    print(df.to_string())
    return df

def main():
    df = parse_txt_drone()
    move_drone(2, df)

if __name__ == "__main__":
    main()