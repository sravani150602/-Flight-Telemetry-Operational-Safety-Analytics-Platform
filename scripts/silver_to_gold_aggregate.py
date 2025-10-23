import pandas as pd
from datetime import datetime

print("=== GOLD LAYER: Creating Business Analytics ===\n")

# Load cleaned Silver data
print("Loading Silver layer data...")
silver_file = "../silver/flights_cleaned_20251021.csv"
df = pd.read_csv(silver_file)

print(f"Loaded {len(df)} clean flight records\n")

# =======================
# AGGREGATION 1: Flight Summary by Country
# =======================
print("Creating aggregation: Flights by Country...")
country_summary = df.groupby('origin_country').agg({
    'icao24': 'count',
    'baro_altitude': ['mean', 'max'],
    'velocity': ['mean', 'max'],
    'on_ground': 'sum'
}).round(2)

country_summary.columns = ['total_flights', 'avg_altitude_m', 'max_altitude_m', 
                           'avg_velocity_ms', 'max_velocity_ms', 'flights_on_ground']
country_summary = country_summary.reset_index()
country_summary = country_summary.sort_values('total_flights', ascending=False)

print(country_summary.head(10))
print()

# Save
country_output = "../gold/flight_summary_by_country.csv"
country_summary.to_csv(country_output, index=False)
print(f"✅ Saved: {country_output}\n")

# =======================
# AGGREGATION 2: Flight Statistics Overview
# =======================
print("Creating aggregation: Overall Flight Statistics...")
overall_stats = {
    'date': datetime.now().strftime('%Y-%m-%d'),
    'total_flights': len(df),
    'flights_in_air': len(df[df['on_ground'] == False]),
    'flights_on_ground': len(df[df['on_ground'] == True]),
    'unique_countries': df['origin_country'].nunique(),
    'avg_altitude_m': round(df['baro_altitude'].mean(), 2),
    'max_altitude_m': round(df['baro_altitude'].max(), 2),
    'avg_velocity_ms': round(df['velocity'].mean(), 2),
    'max_velocity_ms': round(df['velocity'].max(), 2),
    'complete_records': len(df[df['data_quality'] == 'complete']),
    'incomplete_records': len(df[df['data_quality'] == 'incomplete'])
}

stats_df = pd.DataFrame([overall_stats])
print(stats_df.T)
print()

# Save
stats_output = "../gold/daily_flight_statistics.csv"
stats_df.to_csv(stats_output, index=False)
print(f"✅ Saved: {stats_output}\n")

# =======================
# AGGREGATION 3: Top 20 Most Active Flights
# =======================
print("Creating aggregation: Most Active Callsigns...")
active_flights = df[df['callsign'].notna()].groupby('callsign').agg({
    'icao24': 'first',
    'origin_country': 'first',
    'baro_altitude': 'mean',
    'velocity': 'mean'
}).round(2).reset_index()

active_flights.columns = ['callsign', 'icao24', 'origin_country', 
                          'avg_altitude_m', 'avg_velocity_ms']
active_flights = active_flights.head(20)

print(active_flights.head(10))
print()

# Save
active_output = "../gold/top_active_flights.csv"
active_flights.to_csv(active_output, index=False)
print(f"✅ Saved: {active_output}\n")

print("="*60)
print("🎉 GOLD LAYER CREATION COMPLETE!")
print("="*60)
print("\nGenerated Files:")
print("1. flight_summary_by_country.csv - Aggregated stats by country")
print("2. daily_flight_statistics.csv - Overall daily metrics")
print("3. top_active_flights.csv - Most active callsigns")