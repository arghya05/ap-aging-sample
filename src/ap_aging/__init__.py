"""AP aging service: buckets open invoices by days past due."""
from .aging import aging_buckets

__version__ = "1.4.0"
__all__ = ["aging_buckets"]
