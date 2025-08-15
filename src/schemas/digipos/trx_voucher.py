from src.schemas.digipos.trx_paketdata import DigiposOptionalMarkupParams
from src.schemas.sch_trxbase import TrxWithMemberAuth


class DigiposReqListVoucher(TrxWithMemberAuth, DigiposOptionalMarkupParams):
    """Request model for Digipos voucher transaction.

    pada voucher ngga ada filter filter kolom
    """

    pass
