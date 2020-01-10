import sqlite3

fuel_types = ("regular", "midgrade", "premium")
time_filters = ("weekly", "monthly", "annually")

def getFuelPrice(**kwargs):
    conn = sqlite3.connect("fuelPrice.db")
    cur = conn.cursor()
        
    cur.execute(
        f"""SELECT Time, "{kwargs['area']}"
            FROM "{kwargs['fuel_type']}:{kwargs['period']}";"""
        )
    data = cur.fetchall()
        
    conn.close()
    return data


def getRecentFuelPrice(fuel_type):
    conn = sqlite3.connect("fuelPrice.db")
    cur = conn.cursor()
        
    cur.execute(
        f"""SELECT *
            FROM "{fuel_type}:weekly"
            WHERE Time = (SELECT MAX(Time) FROM "{fuel_type}:weekly");"""
        )
    data = cur.fetchall()
        
    conn.close()
    return data[0]


def getAnnualFuelPrices(fuel_type):
    conn = sqlite3.connect("fuelPrice.db")
    cur = conn.cursor()
        
    cur.execute(
        f"""SELECT *
            FROM "{fuel_type}:annually"
            ORDER BY Time;"""
        )
    data = cur.fetchall()
        
    conn.close()
    return data


def get_price_for_nearest_date(**kwargs):
    conn = sqlite3.connect("fuelPrice.db")
    cur = conn.cursor()
        
    cur.execute(
        f"""SELECT Time, "{kwargs['area']}", Date_diff
            FROM
            (
                SELECT Time, "{kwargs['area']}", ABS(julianday(Time)-julianday("{kwargs['date']}")) AS Date_diff
                FROM "{kwargs['fuel_type']}:weekly"
                WHERE "{kwargs['area']}" is not NULL
                ORDER BY date_diff
                Limit 1
            )T;"""
        )
    data = cur.fetchall()
        
    conn.close()
    return data[0]


def get_schema():
    conn = sqlite3.connect("fuelPrice.db")
    cur = conn.cursor()  
    
    cur.execute(f"PRAGMA table_info('midgrade:annually');")
    data = ['-'.join(data[1].split()) for data in cur.fetchall()]
    
    conn.close()
    return data
