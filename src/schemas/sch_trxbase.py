"""Core Schemas untuk Transaksi.

Dipakai semua domain, bisa di-extend sesuai kebutuhan masing-masing.
"""

from typing import Self

from pydantic import BaseModel, Field


class TrxBaseModel(BaseModel):
    """Field dasar transaksi (wajib di semua domain)."""

    memberid: str = Field(..., description="ID member yang akan bertransaksi")
    dest: str = Field(..., description="Tujuan transaksi")
    product: str = Field(..., description="Produk yang akan di-transaksikan")
    trxid: str | None = Field(None, description="ID transaksi dari member")


class TrxAuthFields(BaseModel):
    """Field untuk otentikasi transaksi (opsional per domain)."""

    pin: str | None = Field(None, description="PIN verifikasi transaksi")
    password: str | None = Field(None, description="Password verifikasi transaksi")
    sign: str | None = Field(None, description="Signature verifikasi transaksi")


class TrxResponse(BaseModel):
    """Standarisasi response transaksi ke client."""

    refid: str = Field(..., description="Reference ID transaksi (trxid atau refid)")
    status: str = Field(
        ..., description="Status transaksi, misalnya 'SUCCESS' atau 'FAILED'"
    )
    dest: str = Field(..., description="Tujuan transaksi")
    message: str = Field(..., description="Pesan human-readable untuk client")
    raw_message: str | None = Field(None, description="Pesan asli dari service/domain")

    @classmethod
    def build(
        cls,
        refid: str,
        status: str,
        dest: str,
        product: str,
        raw_message: str | None = None,
    ) -> Self:
        """Factory method untuk bikin response dengan format standar."""
        formatted_message = (
            f"Transaksi {product} ke {dest} status {status.upper()} "
            f"output: {raw_message or ''}"
        ).strip()
        return cls(
            refid=refid,
            status=status.upper(),
            dest=dest,
            message=formatted_message,
            raw_message=raw_message,
        )
