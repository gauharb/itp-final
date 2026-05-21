import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from services.inventory import InventoryService, ProductNotFoundError
from services.report import ReportService
from utils.file_handler import FileHandler
from utils.validators import (
    prompt_int,
    prompt_float,
    prompt_nonempty,
    prompt_date,
    confirm,
    format_price,
    format_id,
    log_action
)