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


class Command(BaseCommand):
    """."""

    help = 'Creating Assets with out Outwarding the used parts.'

    def add_arguments(self, parser):
        """Mandatory Arguments."""
        parser.add_argument(
            'BOMName',
            type=str,
            help="Provide a BillOfMaterial Name which was used for Asset"
        )
        parser.add_argument(
            'Quantity',
            type=int,
            help='Number of Asset to be created'
        )
        parser.add_argument(
            'ProductName',
            type=str,
            help="Provide a Product Name"
        )
        parser.add_argument(
            'WarehouseName',
            type=str,
            help='Provide a Warehouse Name in which Assets were create.'
        )
        parser.add_argument(
            'MFGDate',
            type=str,
            help="Provide a Manufactured date for Assets. '%Y-%m-%d'"
        )
        parser.add_argument(
            'Remarks', type=str,
            help="Provide remarks for Assets"
        )
        parser.add_argument(
            'AssetState', type=str,
            help="Provide state for Assets"
        )

    def handle(self, *args, **options):
        """."""
        with create_revision():
                bom_name = options['BOMName']
                try:
                    bom_name = BillOfMaterial.objects.get(
                        bom_name=bom_name
                    )
                except BillOfMaterial.DoesNotExist:
                    raise CommandError('BOM "%s" does not exist' % bom_name)
                product_name = options['ProductName']
                try:
                    product_name = Product.objects.get(
                        product_name=product_name
                    )
                except Product.DoesNotExist:
                    raise CommandError(
                        'Product "%s" does not exist' % product_name
                    )
                warehouse_name = options['WarehouseName']
                try:
                    warehouse_name = Warehouse.objects.get(
                        warehouse_name=warehouse_name
                    )
                except Warehouse.DoesNotExist:
                    raise CommandError(
                        'Warehouse "%s" does not exist' % warehouse_name
                    )
                parts = get_bom_parts(bom_name)
                total_price = cal_total_price(bom_name)
                qty = options['Quantity']
                mfg_date = options['MFGDate']
                mfg_date = datetime.strptime(mfg_date, '%Y-%m-%d').date()
                remarks = options['Remarks']
                asset_state = options['AssetState']
                for i in range(qty):
                    single_asset = Asset(
                        product_name=product_name,
                        bom_name=bom_name,
                        parts=parts,
                        total_price=total_price,
                        warehouse_name=warehouse_name,
                        remarks=remarks,
                        mfg_date=mfg_date,
                        asset_state=asset_state,
                    )
                    single_asset.save()
                    revisions.set_comment(
                        "Created via CLI With Out Outwards of parts."
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Created {} of {} Assets'.format(i + 1, qty)
                        )
                    )
