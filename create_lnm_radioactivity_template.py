#!/usr/bin/env python3
"""
Create EBAS NASA Ames template file for LNM site radioactivity measurements.

This script generates a NASA Ames 1001 format file compatible with EBAS submissions.
For new sites/measurements not yet in the EBAS system, you will need to:
1. Contact EBAS (ebas@nilu.no) to register the new station (LNM)
2. Request addition of radioactivity as a component if not already available
3. Submit this file for validation using the EBAS submit tool

Usage:
    python create_lnm_radioactivity_template.py

The generated file can be validated at:
    https://ebas-submit.nilu.no/Submit-Data/Submit-your-data
"""

from fileformats.NasaAmes1001 import NasaAmes1001
import datetime
import os


def create_ebas_metadata(
    station_code="LNM",
    station_name="LNM Test Site",
    latitude=40.0,
    longitude=-105.0,
    altitude=1600,
    start_date=None,
    component="radioactivity",
    unit="Bq/m3",
    matrix="air",
    instrument_type="radiation_monitor",
    lab_code="US05",
    originator_name="Greenberg, Gabe",
    organization="Boulder AIR, Boulder, CO, , USA",
    data_level="0",
    period_code="1y",
    resolution_code="1d",
    regime="IMG",
):
    """
    Generate EBAS metadata comments for the NASA Ames file header.

    Parameters:
        station_code: EBAS station code (needs to be registered with EBAS)
        station_name: Full station name
        latitude: Station latitude in decimal degrees
        longitude: Station longitude in decimal degrees
        altitude: Station altitude in meters
        start_date: Start date of measurements (datetime object)
        component: Measurement component (e.g., 'radioactivity', 'radon', 'Be-7')
        unit: Measurement unit (e.g., 'Bq/m3', 'mBq/m3')
        matrix: Sample matrix (typically 'air' for radioactivity)
        instrument_type: Type of measurement instrument
        lab_code: Laboratory code (needs to be registered with EBAS)
        originator_name: Name of data originator (Last, First)
        organization: Organization details
        data_level: EBAS data level (0=raw, 1=quality controlled, 2=final)
        period_code: Data period (e.g., '1y' for yearly file)
        resolution_code: Time resolution (e.g., '1d' for daily, '1h' for hourly)
        regime: Measurement regime (IMG=in-situ ground, etc.)

    Returns:
        List of metadata comment lines for NCOML section
    """
    if start_date is None:
        start_date = datetime.datetime.now()

    date_str = start_date.strftime("%Y%m%d%H%M%S")
    revision_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate filename according to EBAS convention
    # Format: SSSSSS.YYYYMMDDHHMMSS.YYYYMMDDHHMMSS.component.level.period.resolution.lab_instr.lab.level.nas
    filename = f"{station_code}.{date_str}.{revision_date}.{component}.lev{data_level}.{period_code}.{resolution_code}.{lab_code}_{instrument_type}.{lab_code}.lev{data_level}.nas"

    metadata = [
        f"Data definition:              EBAS_1.1",
        f"Set type code:                TI",
        f"Timezone:                     UTC",
        f"File name:                    {filename}",
        f"Startdate:                    {date_str}",
        f"Revision date:                {revision_date}",
        f"Data level:                   {data_level}",
        f"Period code:                  {period_code}",
        f"Resolution code:              {resolution_code}",
        f"Station code:                 {station_code}",
        f"Platform code:                {station_code}",
        f"Station name:                 {station_name}",
        f"Station latitude:             {latitude}",
        f"Station longitude:            {longitude}",
        f"Station altitude:             {altitude} m",
        f"Regime:                       {regime}",
        f"Component:                    {component}",
        f"Unit:                         {unit}",
        f"Matrix:                       {matrix}",
        f"Instrument type:              {instrument_type}",
        f"Laboratory code:              {lab_code}",
        f"Originator:                   {originator_name}",
        f"Organization:                 {organization}",
    ]

    return metadata, filename


def create_radioactivity_file(
    output_dir=".",
    station_code="LNM",
    station_name="LNM Test Site",
    latitude=40.0,
    longitude=-105.0,
    altitude=1600,
    start_date=None,
    sample_data=None,
    component="radioactivity",
    unit="Bq/m3",
    matrix="air",
    instrument_type="radiation_monitor",
    lab_code="US05",
    originator_name="Greenberg, Gabe",
    organization="Boulder AIR, Boulder, CO, , USA",
    data_level="0",
    period_code="1y",
    resolution_code="1d",
):
    """
    Create a complete EBAS NASA Ames file for radioactivity measurements.

    Parameters:
        output_dir: Directory to save the output file
        station_code: EBAS station code
        station_name: Full station name
        latitude: Station latitude
        longitude: Station longitude
        altitude: Station altitude in meters
        start_date: Start date of measurements (datetime object)
        sample_data: List of tuples [(start_day, end_day, value, flag), ...]
                     If None, creates template with placeholder data
        component: Measurement component name
        unit: Measurement unit
        matrix: Sample matrix
        instrument_type: Instrument type identifier
        lab_code: Laboratory code
        originator_name: Data originator name
        organization: Organization name and details
        data_level: EBAS data level
        period_code: Data period code
        resolution_code: Time resolution code

    Returns:
        Path to the created file
    """
    if start_date is None:
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)

    # Create sample data if not provided
    if sample_data is None:
        # Create 10 days of sample data
        sample_data = [
            (i, i + 1, 0.5 + i * 0.01, 0.000)  # (start_day, end_day, value, flag)
            for i in range(10)
        ]

    # Create NASA Ames object
    na = NasaAmes1001()
    na.init_data()

    # Header information
    na.ONAME = originator_name
    na.ORG = organization
    na.SNAME = originator_name  # Submitter (can be different)
    na.MNAME = f"{station_name} - {component} measurements"

    na.IVOL = 1
    na.NVOL = 1

    na.DATE = start_date
    na.RDATE = datetime.datetime.now()

    na.XNAME = "days from file reference point"

    # Variable names and scales
    # Format: description, unit=XXX (EBAS specific format for variable names)
    na.VSCAL = [1.0, 1.0, 1.0]  # Scale factors
    na.VNAME = [
        "end_time of measurement, days from the file reference point",
        f"{component}, {unit}",
        f"numflag, no unit",
    ]

    # Special comments (typically empty for standard files)
    na.SCOML = []

    # Generate EBAS metadata
    metadata, filename = create_ebas_metadata(
        station_code=station_code,
        station_name=station_name,
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
        start_date=start_date,
        component=component,
        unit=unit,
        matrix=matrix,
        instrument_type=instrument_type,
        lab_code=lab_code,
        originator_name=originator_name,
        organization=organization,
        data_level=data_level,
        period_code=period_code,
        resolution_code=resolution_code,
    )
    na.NCOML = metadata

    # Data columns: [X, V1, V2, V3, ...]
    # X = start_time (independent variable)
    # V1 = end_time
    # V2 = measurement value
    # V3 = flag (0.000 = valid)
    start_times = [row[0] for row in sample_data]
    end_times = [row[1] for row in sample_data]
    values = [row[2] for row in sample_data]
    flags = [row[3] for row in sample_data]

    na.DATA = [start_times, end_times, values, flags]

    # Write to file
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w') as f:
        na.write(f)

    print(f"Created EBAS NASA Ames file: {output_path}")
    return output_path


def main():
    """Main function to create template file."""

    print("=" * 60)
    print("EBAS NASA Ames Template Generator for Radioactivity Data")
    print("=" * 60)
    print()

    # Example: Create a template file for LNM site
    output_path = create_radioactivity_file(
        output_dir=".",
        station_code="LNM",
        station_name="LNM Radioactivity Site",
        latitude=40.0150,      # Adjust to actual coordinates
        longitude=-105.2705,   # Adjust to actual coordinates
        altitude=1655,         # Adjust to actual altitude in meters
        start_date=datetime.datetime(2024, 1, 1),
        component="radioactivity",  # May need to use specific isotope like "Be-7", "Pb-210", "Cs-137"
        unit="Bq/m3",               # or "mBq/m3" for lower activity
        matrix="air",
        instrument_type="gamma_spectrometer",  # Adjust to actual instrument
        lab_code="US05",            # Needs to be registered with EBAS
        originator_name="Greenberg, Gabe",
        organization="Boulder AIR, Boulder, CO, , USA",
        data_level="0",             # Raw data
        period_code="1y",           # One year of data
        resolution_code="1d",       # Daily resolution
        sample_data=[
            # Sample data: (start_day, end_day, value_Bq_m3, flag)
            # Day 0 = January 1, 2024
            (0, 1, 0.52, 0.000),
            (1, 2, 0.48, 0.000),
            (2, 3, 0.55, 0.000),
            (3, 4, 0.51, 0.000),
            (4, 5, 0.49, 0.000),
            (5, 6, 0.53, 0.000),
            (6, 7, 0.47, 0.000),
            (7, 8, 0.54, 0.000),
            (8, 9, 0.50, 0.000),
            (9, 10, 0.52, 0.000),
        ]
    )

    print()
    print("IMPORTANT NOTES FOR NEW SITES/MEASUREMENTS:")
    print("-" * 60)
    print("""
1. REGISTER YOUR STATION:
   Before submitting data, you must register your station with EBAS.
   Contact: ebas@nilu.no
   Required information:
   - Station name and code
   - Geographic coordinates (latitude, longitude, altitude)
   - Station type and setting
   - Contact person information

2. REGISTER YOUR COMPONENT:
   If 'radioactivity' is not in EBAS's controlled vocabulary, you may need
   to use a more specific component name like:
   - Be-7 (Beryllium-7)
   - Pb-210 (Lead-210)
   - Cs-137 (Cesium-137)
   - Rn-222 (Radon-222)
   Or request addition of your specific measurement.

3. VALIDATE YOUR FILE:
   Use the EBAS submit tool to validate your file:
   https://ebas-submit.nilu.no/Submit-Data/Submit-your-data

4. FLAG CODES:
   - 0.000 = Valid data
   - See EBAS documentation for other flag codes

5. DATA LEVELS:
   - Level 0: Raw data
   - Level 1: Quality controlled
   - Level 2: Final/published data
    """)

    # Read and display the created file
    print()
    print("Generated file content:")
    print("-" * 60)
    with open(output_path, 'r') as f:
        print(f.read())


if __name__ == "__main__":
    main()
