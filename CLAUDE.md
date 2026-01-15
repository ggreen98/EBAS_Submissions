# EBAS Submissions Project

## Project Overview
This project creates and manages data submissions to EBAS (European Monitoring and Evaluation Programme database) for the LNM atmospheric monitoring site.

## EBAS Library (ebas-io)

### Installation
```bash
# Install to venv
.venv/bin/python -m pip install ebas-io
```

### Import Structure
```python
# The package is 'ebas-io' on PyPI but imports as 'ebas'
import ebas

# Key classes for NASA Ames file handling
from ebas.io.file.nasa_ames import EbasNasaAmes

# Low-level NASA Ames 1001 format (for creating files from scratch)
from fileformats.NasaAmes1001 import NasaAmes1001
```

### Creating NASA Ames Files from Scratch
The `EbasNasaAmes` class is primarily for reading/validating existing files. For creating new files (especially for new sites/measurements not in EBAS), use `NasaAmes1001` directly:

```python
from fileformats.NasaAmes1001 import NasaAmes1001
import datetime

na = NasaAmes1001()
na.init_data()

# Required header fields
na.ONAME = "Last, First"           # Originator name
na.ORG = "Organization, City, State, , Country"  # Organization
na.SNAME = "Last, First"           # Submitter name
na.MNAME = "Site - measurements"   # Mission/experiment name
na.IVOL = 1                        # Volume number
na.NVOL = 1                        # Total volumes
na.DATE = datetime.datetime(2024, 1, 1)   # Start date (datetime object!)
na.RDATE = datetime.datetime.now()        # Revision date
na.XNAME = "days from file reference point"

# Variable definitions
na.VSCAL = [1.0, 1.0, 1.0]  # Scale factors for each variable
na.VNAME = [
    "end_time of measurement, days from the file reference point",
    "component_name, unit",
    "numflag, no unit",
]

# Metadata comments (EBAS-specific format)
na.SCOML = []  # Special comments (usually empty)
na.NCOML = [   # Normal comments - EBAS metadata
    "Data definition:              EBAS_1.1",
    "Set type code:                TI",
    "Timezone:                     UTC",
    # ... more metadata fields
]

# Data: [X_column, V1_column, V2_column, ...]
# X = independent variable (start_time in days)
# V1, V2, ... = dependent variables
na.DATA = [start_times, end_times, values, flags]

# Write to file
with open('output.nas', 'w') as f:
    na.write(f)
```

## NASA Ames 1001 File Format

### Structure
```
NLHEAD 1001                          <- Number of header lines + format code
ONAME                                <- Originator name
ORG                                  <- Organization
SNAME                                <- Submitter name
MNAME                                <- Mission/experiment name
IVOL NVOL                            <- Volume info
DATE RDATE                           <- Start date and revision date
DX                                   <- Time interval (0 for irregular)
XNAME                                <- Independent variable name
NV                                   <- Number of dependent variables
VSCAL(1) ... VSCAL(NV)              <- Scale factors
VMISS(1) ... VMISS(NV)              <- Missing value codes
VNAME(1)                            <- Variable 1 name
...
VNAME(NV)                           <- Variable NV name
NSCOML                              <- Number of special comment lines
SCOML lines...                      <- Special comments
NNCOML                              <- Number of normal comment lines
NCOML lines...                      <- Normal comments (EBAS metadata here!)
DATA...                             <- Data rows
```

### EBAS Metadata Fields (in NCOML section)
Required fields:
- `Data definition:` - Always "EBAS_1.1"
- `Set type code:` - "TI" for time series
- `Timezone:` - Usually "UTC"
- `File name:` - EBAS naming convention
- `Startdate:` - Format YYYYMMDDHHMMSS
- `Revision date:` - Format YYYYMMDDHHMMSS
- `Data level:` - 0 (raw), 1 (QC), 2 (final)
- `Period code:` - e.g., "1y", "1mo"
- `Resolution code:` - e.g., "1h", "1d", "1mn"
- `Station code:` - EBAS station identifier
- `Station name:` - Full station name
- `Station latitude/longitude/altitude:`
- `Regime:` - e.g., "IMG" (in-situ ground)
- `Component:` - Measurement type
- `Unit:` - Measurement unit
- `Matrix:` - Sample matrix (usually "air")
- `Instrument type:` - Instrument identifier
- `Laboratory code:` - Lab identifier

## LNM Site Configuration

Default values for LNM site:
```python
station_code = "LNM"
station_name = "LNM Atmospheric Site"
latitude = 40.0150
longitude = -105.2705
altitude = 1655  # meters
lab_code = "US05"
organization = "Boulder AIR, Boulder, CO, , USA"
regime = "IMG"  # In-situ ground measurements
```

## Measurement Templates

### Radioactivity
- Script: `create_lnm_radioactivity_template.py`
- Component: "radioactivity" (or specific isotope: Be-7, Pb-210, Cs-137, Rn-222)
- Unit: "Bq/m3" or "mBq/m3"
- Resolution: typically "1d" (daily)
- Instrument types: gamma_spectrometer, radiation_monitor

### Methane (CH4)
- Script: `create_lnm_methane_template.py`
- Component: "methane"
- Unit: "ppb" or "nmol/mol"
- Resolution: typically "1h" (hourly)
- Instrument types: cavity_ringdown_spectrometer, gas_chromatograph_fid, ftir_spectrometer
- Calibration scale: "WMO CH4 X2004A"

## Common EBAS Components and Units

| Component | Common Units | Notes |
|-----------|--------------|-------|
| methane | ppb, nmol/mol | Greenhouse gas |
| carbon_dioxide | ppm, umol/mol | Greenhouse gas |
| ozone | ppb, nmol/mol, ug/m3 | Requires std temp/pressure |
| nitrogen_dioxide | ppb, ug/m3 | |
| carbon_monoxide | ppb, nmol/mol | |
| sulfur_dioxide | ppb, ug/m3 | |
| pm10, pm2.5, pm1 | ug/m3 | Particulate matter |
| Be-7, Pb-210, Cs-137 | Bq/m3, mBq/m3 | Radioactivity |

## Flag Codes
- `0.000` - Valid data
- `0.999` - Missing data
- See EBAS documentation for quality control flags

## Submission Process

1. **Register station** (if new): Contact ebas@nilu.no
2. **Create data file** using templates
3. **Validate** at https://ebas-submit.nilu.no/Submit-Data/Submit-your-data
4. **Submit** through the EBAS portal

## Useful Links
- EBAS Submit Tool: https://ebas-submit.nilu.no/tools
- EBAS Data Templates: https://ebas-submit.nilu.no/Submit-Data/Data-templates
- ebas-io Documentation: https://ebas.pages.nilu.no/ebas-io
- ebas-io Git Repository: https://git.nilu.no/ebas/ebas-io

## File Naming Convention
```
STATION.STARTDATE.REVDATE.COMPONENT.LEVEL.PERIOD.RESOLUTION.LAB_INSTR.LAB.LEVEL.nas
```
Example:
```
LNM.20240101000000.20240115120000.methane.lev0.1y.1h.US05_crds.US05.lev0.nas
```
