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

    help = 'Creating Inwards in a batch.'

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
                if row['vendor_code'] == '#N/A':
                    row['vendor_code'] = ''
                if row['from_warehouse_code'] == '-':
                    row['from_warehouse_code'] = ''
                if row['remarks'] == '-':
                    row['remarks'] = ''
                if 'vendor_name' in row:
                    row.pop('vendor_name')
                cmd = 'python manage.py create_inwards "{received_date}" "{invoice_number}" "{invoice_date}" {invoice_quantity} {received_quantity} {defected_quantity} "{batch_number}" "{recived_by}" "{remarks}" {transport_charges} "{from_warehouse_code}" "{part_number}" "{part_type}" "{to_warehouse_code}" "{unit_of_measure}" "{vendor_code}" '.format(
                    **row
                )
                if "Order" not in row or row["Order"] == "":
                    print(cmd)
                    os.system(cmd)
                    print()

