"""."""
from django.core.management.base import BaseCommand, CommandError
from aims.inventory.models import (
    Warehouse,
    BillOfMaterial,
    Product,
    Asset,
)
import reversion as revisions
from reversion import create_revision
from aims.inventory.utils import (
    get_bom_parts,
    cal_total_price,
)
from datetime import datetime
import csv
import os


class Command(BaseCommand):
    """."""

    help = 'Creating Assets with out Outwarding the used parts.'

    def add_arguments(self, parser):
        """Mandatory Arguments."""
        parser.add_argument(
            'file',
            type=str,
            help="Path to excel file"
        )

    def handle(self, *args, **options):
        """."""
        with open(options['file']) as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                # bom_name = row['BOMName']
                # product_name = row['ProductName']
                # warehouse_name = row['WarehouseName']
                # qty = row['Quantity']
                # mfg_date = row['MFGDate']
                # remarks = row['Remarks']

                cmd = 'python manage.py create_assets "{BOMName}" {Quantity} "{ProductName}" "{WarehouseName}" "{MFGDate}" "{Remarks}" "{AssetState}"'.format(
                    # bom_name,
                    # product_name,
                    # warehouse_name,
                    # qty,
                    # mfg_date,
                    # remarks,
                    **row
                )
                if "Order" not in row or row["Order"] == "":
                    print(cmd)
                    os.system(cmd)
                    print()

