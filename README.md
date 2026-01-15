# EBAS Submissions

Tools and templates for creating EBAS-compatible NASA Ames data files for the LNM atmospheric monitoring site.

## Overview

This project provides Python scripts to generate NASA Ames 1001 format files for submission to [EBAS](https://ebas.nilu.no/) (European Monitoring and Evaluation Programme database).

## Setup

### Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Install dependencies

```bash
pip install ebas-io
```

## Usage

### Generate Radioactivity Template

```bash
python create_lnm_radioactivity_template.py
```

Creates a NASA Ames file for radioactivity measurements (Be-7, Pb-210, Cs-137, etc.).

### Generate Methane Template

```bash
python create_lnm_methane_template.py
```

Creates a NASA Ames file for methane (CH4) measurements.

## Customization

Edit the scripts to modify:

- **Station information**: coordinates, altitude, station code
- **Measurement data**: replace sample data with your actual measurements
- **Instrument details**: manufacturer, model, serial number
- **Time resolution**: hourly, daily, etc.

Example:
```python
create_methane_file(
    station_code="LNM",
    latitude=40.0150,
    longitude=-105.2705,
    altitude=1655,
    sample_data=[
        (0.0, 0.041667, 1895.2, 0.000),  # (start_day, end_day, value, flag)
        # ... your data
    ]
)
```

## File Format

Generated files follow the NASA Ames 1001 format with EBAS extensions:

```
NLHEAD 1001
Originator Name
Organization
...
Data definition:              EBAS_1.1
Station code:                 LNM
Component:                    methane
Unit:                         ppb
...
DATA
```

## Submission Process

1. **Register your station** (if new): Contact ebas@nilu.no
2. **Generate your data file** using the templates
3. **Validate** at https://ebas-submit.nilu.no/Submit-Data/Submit-your-data
4. **Submit** through the EBAS portal

## LNM Site Defaults

| Parameter | Value |
|-----------|-------|
| Station Code | LNM |
| Latitude | 40.0150 |
| Longitude | -105.2705 |
| Altitude | 1655 m |
| Lab Code | US05 |

## Supported Measurements

| Type | Component | Unit | Resolution |
|------|-----------|------|------------|
| Radioactivity | radioactivity, Be-7, Pb-210, Cs-137 | Bq/m3 | Daily |
| Methane | methane | ppb | Hourly |

## Resources

- [EBAS Submit Tool](https://ebas-submit.nilu.no/tools)
- [ebas-io Documentation](https://ebas.pages.nilu.no/ebas-io)
- [ebas-io Repository](https://git.nilu.no/ebas/ebas-io)

## License

MIT
