[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1+-green.svg)](https://fastapi.tiangolo.com/)

# MODKIT API PARSER

## cara kerja API

API ini bekerja dengan cara menerima permintaan dari klien, memprosesnya, dan mengembalikan respons yang sesuai. Berikut adalah langkah-langkah umum dalam proses ini:

```mermaid
sequenceDiagram
    autonumber
    Client->>API: GET Request
    API->>API: Verify Member Auth
    API->>API: Verify Product Auth
    API->>API: Verify Module Auth
    API->>API: Query Builder
    API->>Target: Forward GET Request
    Target-->>API: Response
    API->>API: Check Response Length
    alt Response > 7000 chars
        API->>API: Trim & Optimize Text
    else Response <= 7000 chars
        API->>API: Clean Up Text
    end
    API->>API: Reshape to Plain Text
    API-->>Client: Return Plain Text Response
```

## Tech Stack

- UV : Ultra Fast Python Product manager from astral.
- Python => 3.12
- fastapi>=0.116.1",
- loguru>=0.7.3",
- loguru-config>=0.1.0",
- markdown>=3.8.2",
- watchdog>=6.0.0",
