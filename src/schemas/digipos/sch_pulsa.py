"""module untuk skema pembelian Pulsa API Digipos ASL.

documentasi from digipos ASL:
    -List Denom
        - http://localhost:10003/list_denom?username=WIR6289504&to=08123456789&payment_method=LINKAJA&amount=5000
            - Note: optional &up_harga=xxxxx
    -Trx Pulsa
        -http://localhost:10003/pulsa?username=WIR6289504&pin=[pin]&payment_method=NGR&to=08123456789&amount=5000&type=FIX&idtrx=[trxid]
            - Note: optional check=1 untuk pengecekan
            - Note: type = FIX/BULK, idtrx = idtransaksi server

sample request GET:
cek harga awal pulsa
http://10.0.0.3:10003/list_denom?username=WIR6289504&to=081295221639&payment_method=LINKAJA&amount=5000&json=1&up_harga=100

postpaid pulsa:

LINKAJA
check:
    -http://10.0.0.3:10003/pulsa?username=WIR6289504&pin=123465&payment_method=LINKAJA&to=081295221639&amount=5000&up_harga=100&type=BULK&idtrx=1234&json=1&check=1
bayar:
    -http://10.0.0.3:10003/pulsa?username=WIR6289504&pin=123465&payment_method=LINKAJA&to=081295221639&amount=5000&up_harga=100&type=BULK&idtrx=1234&json=1

NGRS
check:
    -http://10.0.0.3:10003/pulsa?username=WIR6289504&pin=123465&payment_method=NGRS&to=081295221639&amount=5000&up_harga=100&type=FIX&idtrx=1234&json=1&check=1
bayar:
    -http://10.0.0.3:10003/pulsa?username=WIR6289504&pin=123465&payment_method=NGRS&to=081295221639&amount=5000&up_harga=100&type=FIX&idtrx=1234&json=1
"""
