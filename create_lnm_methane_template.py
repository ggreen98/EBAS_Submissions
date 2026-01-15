#!/usr/bin/env python3
"""
Create EBAS NASA Ames template file for LNM site methane (CH4) measurements.

This script generates a NASA Ames 1001 format file compatible with EBAS submissions.

Usage:
    python create_lnm_methane_template.py

The generated file can be validated at:
    https://ebas-submit.nilu.no/Submit-Data/Submit-your-data
"""

import sys
import os

# Add the venv site-packages to path for fileformats module
venv_path = os.path.join(os.path.dirname(__file__), '.venv', 'lib', 'python3.12', 'site-packages')
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

from fileformats.NasaAmes1001 import NasaAmes1001
import datetime


def create_ebas_metadata(
    station_code="LNM",
    station_name="LNM Test Site",
    latitude=40.0,
    longitude=-105.0,
    altitude=1600,
    start_date=None,
    component="methane",
    unit="ppb",
    matrix="air",
    instrument_type="cavity_ringdown_spectrometer",
    lab_code="US05",
    originator_name="Greenberg, Gabe",
    organization="Boulder AIR, Boulder, CO, , USA",
    data_level="0",
    period_code="1y",
    resolution_code="1h",
    regime="IMG",
    instrument_name=None,
    instrument_manufacturer=None,
    instrument_model=None,
    instrument_serial=None,
    calibration_scale=None,
):
    """
    Generate EBAS metadata comments for methane measurements.
    """
    if start_date is None:
        start_date = datetime.datetime.now()

    date_str = start_date.strftime("%Y%m%d%H%M%S")
    revision_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate filename according to EBAS convention
    filename = f"{station_code}.{date_str}.{revision_date}.{component}.lev{data_level}.{period_code}.{resolution_code}.{lab_code}_{instrument_type}.{lab_code}.lev{data_level}.nas"

    metadata = [
        "Data definition:              EBAS_1.1",
        "Set type code:                TI",
        "Timezone:                     UTC",
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

    # Add optional instrument details if provided
    if instrument_name:
        metadata.append(f"Instrument name:              {instrument_name}")
    if instrument_manufacturer:
        metadata.append(f"Instrument manufacturer:      {instrument_manufacturer}")
    if instrument_model:
        metadata.append(f"Instrument model:             {instrument_model}")
    if instrument_serial:
        metadata.append(f"Instrument serial number:     {instrument_serial}")
    if calibration_scale:
        metadata.append(f"Calibration scale:            {calibration_scale}")

    return metadata, filename


def create_methane_file(
    output_dir=".",
    station_code="LNM",
    station_name="LNM Test Site",
    latitude=40.0,
    longitude=-105.0,
    altitude=1600,
    start_date=None,
    sample_data=None,
    component="methane",
    unit="ppb",
    matrix="air",
    instrument_type="cavity_ringdown_spectrometer",
    lab_code="US05",
    originator_name="Greenberg, Gabe",
    organization="Boulder AIR, Boulder, CO, , USA",
    data_level="0",
    period_code="1y",
    resolution_code="1h",
    instrument_name=None,
    instrument_manufacturer=None,
    instrument_model=None,
    instrument_serial=None,
    calibration_scale="WMO CH4 X2004A",
):
    """
    Create a complete EBAS NASA Ames file for methane measurements.

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
        component: Measurement component name (typically 'methane')
        unit: Measurement unit (typically 'ppb' or 'nmol/mol')
        matrix: Sample matrix (typically 'air')
        instrument_type: Instrument type identifier
        lab_code: Laboratory code
        originator_name: Data originator name
        organization: Organization name and details
        data_level: EBAS data level
        period_code: Data period code
        resolution_code: Time resolution code
        instrument_name: Specific instrument name
        instrument_manufacturer: Instrument manufacturer
        instrument_model: Instrument model number
        instrument_serial: Instrument serial number
        calibration_scale: Calibration scale (e.g., 'WMO CH4 X2004A')

    Returns:
        Path to the created file
    """
    if start_date is None:
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)

    # Create sample data if not provided (hourly data for 24 hours)
    if sample_data is None:
        # Create 24 hours of sample data
        # Values in ppb, typical ambient CH4 is ~1900 ppb
        sample_data = [
            (i / 24.0, (i + 1) / 24.0, 1900 + (i % 12) * 2, 0.000)
            for i in range(24)
        ]

    # Create NASA Ames object
    na = NasaAmes1001()
    na.init_data()

    # Header information
    na.ONAME = originator_name
    na.ORG = organization
    na.SNAME = originator_name
    na.MNAME = f"{station_name} - {component} measurements"

    na.IVOL = 1
    na.NVOL = 1

    na.DATE = start_date
    na.RDATE = datetime.datetime.now()

    na.XNAME = "days from file reference point"

    # Variable names and scales
    na.VSCAL = [1.0, 1.0, 1.0]
    na.VNAME = [
        "end_time of measurement, days from the file reference point",
        f"{component}, {unit}",
        "numflag, no unit",
    ]

    # Special comments
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
        instrument_name=instrument_name,
        instrument_manufacturer=instrument_manufacturer,
        instrument_model=instrument_model,
        instrument_serial=instrument_serial,
        calibration_scale=calibration_scale,
    )
    na.NCOML = metadata

    # Data columns
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
    print("EBAS NASA Ames Template Generator for Methane (CH4) Data")
    print("=" * 60)
    print()

    # Example: Create a template file for LNM site methane measurements
    output_path = create_methane_file(
        output_dir=".",
        station_code="LNM",
        station_name="LNM Atmospheric Site",
        latitude=40.0150,
        longitude=-105.2705,
        altitude=1655,
        start_date=datetime.datetime(2024, 1, 1),
        component="methane",
        unit="ppb",  # or "nmol/mol" - both are equivalent
        matrix="air",
        instrument_type="cavity_ringdown_spectrometer",  # Common for CH4: CRDS, FTIR, GC-FID
        lab_code="US05",
        originator_name="Greenberg, Gabe",
        organization="Boulder AIR, Boulder, CO, , USA",
        data_level="0",
        period_code="1y",
        resolution_code="1h",  # Hourly data
        instrument_manufacturer="Picarro",  # Example
        instrument_model="G2401",  # Example
        calibration_scale="WMO CH4 X2004A",  # Standard WMO scale
        sample_data=[
            # Sample hourly data: (start_day, end_day, CH4_ppb, flag)
            # Day fractions: 0.0 = 00:00, 0.041667 = 1:00, etc.
            (0.000000, 0.041667, 1895.2, 0.000),  # 00:00-01:00
            (0.041667, 0.083333, 1897.8, 0.000),  # 01:00-02:00
            (0.083333, 0.125000, 1901.3, 0.000),  # 02:00-03:00
            (0.125000, 0.166667, 1904.1, 0.000),  # 03:00-04:00
            (0.166667, 0.208333, 1902.5, 0.000),  # 04:00-05:00
            (0.208333, 0.250000, 1898.7, 0.000),  # 05:00-06:00
            (0.250000, 0.291667, 1893.2, 0.000),  # 06:00-07:00
            (0.291667, 0.333333, 1889.5, 0.000),  # 07:00-08:00
            (0.333333, 0.375000, 1886.1, 0.000),  # 08:00-09:00
            (0.375000, 0.416667, 1884.3, 0.000),  # 09:00-10:00
            (0.416667, 0.458333, 1883.8, 0.000),  # 10:00-11:00
            (0.458333, 0.500000, 1885.2, 0.000),  # 11:00-12:00
        ]
    )

    print()
    print("NOTES FOR METHANE DATA SUBMISSION:")
    print("-" * 60)
    print("""
1. COMPONENT NAME:
   - Use 'methane' for CH4 measurements
   - EBAS recognizes this as a standard greenhouse gas

2. UNITS:
   - 'ppb' (parts per billion) - commonly used
   - 'nmol/mol' - SI equivalent, also accepted
   - 'ppm' if measuring in parts per million

3. CALIBRATION SCALE:
   - WMO CH4 X2004A is the current WMO standard scale
   - Always specify your calibration scale for traceability

4. COMMON INSTRUMENT TYPES:
   - cavity_ringdown_spectrometer (CRDS) - e.g., Picarro
   - optical_feedback_cavity_enhanced (OF-CEAS) - e.g., Los Gatos
   - ftir_spectrometer - Fourier Transform IR
   - gas_chromatograph_fid - GC with flame ionization detector

5. TIME RESOLUTION:
   - '1h' for hourly averages (most common)
   - '1mn' for minute data
   - '1d' for daily averages

6. DATA FLAGS:
   - 0.000 = Valid data
   - 0.999 = Missing data
   - See EBAS documentation for quality flags
    """)

    # Read and display the created file
    print()
    print("Generated file content:")
    print("-" * 60)
    with open(output_path, 'r') as f:
        print(f.read())


if __name__ == "__main__":
    main()
