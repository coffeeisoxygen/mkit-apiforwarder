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

## Penjelasan

1- ketika client menerima request GET : maka akan di verifikasi
