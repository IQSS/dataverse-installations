"""
napkin like calculation for rough download cost estimates
prices from 5/15/2017

using 1000 convert instead of 1024
"""
from __future__ import print_function
from decimal import Decimal

ONE_MB = Decimal(10**6)
ONE_GB = ONE_MB * 1000
ONE_TB = ONE_GB * 1000
TEN_TB = ONE_TB * 10
FORTY_TB = ONE_TB * 40
ONE_HUNDRED_TB = ONE_TB * 100

LEVELS = [
    (ONE_GB, 0.000),
    (TEN_TB, 0.090),
    (FORTY_TB, 0.085),
    (ONE_HUNDRED_TB, 0.070)
]

def bytes_to_gb(num_bytes):

    return num_bytes / ONE_GB

def get_naive_price(num_bytes):
    """Naive price, up to 10GB"""
    #import ipdb; ipdb.set_trace()
    num_bytes = num_bytes - ONE_GB  #1st gb free

    if num_bytes < 0:
        return 0

    return (num_bytes / ONE_GB) * Decimal('.090')


def get_pricing(byte_size):
    """
    First 1 GB / month	$0.000 per GB
    Up to 10 TB / month	$0.090 per GB
    Next 40 TB / month	$0.085 per GB
    Next 100 TB / month	$0.070 per GB
    """
    #total_cost = 0

    for level_bytes, level_cost in LEVELS:
        bytes_at_level = byte_size - level_bytes
