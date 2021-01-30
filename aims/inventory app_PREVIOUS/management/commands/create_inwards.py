"""."""
from django.core.management.base import BaseCommand, CommandError
from aims.inventory.models import (
    Inward,
    UnitOfMeasure,
    Vendor,
    Warehouse,
    Parts,
    Type,
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
            'received_date',
            type=str,
            help="%Y-%m-%d"
        )
        parser.add_argument(
            'invoice_number',
            type=str,
            help=''
        )
        parser.add_argument(
            'invoice_date',
            type=str,
            help="%Y-%m-%d"
        )
        parser.add_argument(
            'invoice_quantity',
            type=int,
            help=''
        )
        parser.add_argument(
            'received_quantity',
            type=int,
            help=''
        )
        parser.add_argument(
            'defected_quantity',
            type=int,
            help=''
        )
        parser.add_argument(
            'batch_number',
            type=str,
            help=''
        )
        parser.add_argument(
            'recived_by',
            type=str,
            help=''
        )
        parser.add_argument(
            'remarks',
            type=str,
            help=''
        )
        parser.add_argument(
            'transport_charges',
            type=int,
            help=''
        )
        parser.add_argument(
            'from_warehouse_code',
            type=str,
            help=''
        )
        parser.add_argument(
            'part_number',
            type=str,
            help=''
        )
        parser.add_argument(
            'part_type',
            type=str,
            help=''
        )
        parser.add_argument(
            'to_warehouse_code',
            type=str,
            help=''
        )
        parser.add_argument(
            'unit_of_measure',
            type=str,
            help=''
        )
        parser.add_argument(
            'vendor_code',
            type=str,
            help=''
        )

    def handle(self, *args, **options):
        """."""
        with create_revision():
            from_warehouse_code = options['from_warehouse_code']
            if from_warehouse_code:
                try:
                    from_warehouse_code = Warehouse.objects.get(
                        warehouse_code=from_warehouse_code
                    )
                except Warehouse.DoesNotExist:
                    raise CommandError(
                        'Warehouse "%s" does not exist' % from_warehouse_code
                    )
            else:
                from_warehouse_code = None

            to_warehouse_code = options['to_warehouse_code']
            try:
                to_warehouse_code = Warehouse.objects.get(
                    warehouse_code=to_warehouse_code
                )
            except Warehouse.DoesNotExist:
                raise CommandError(
                    'Warehouse "%s" does not exist' % to_warehouse_code
                )

            vendor_code = options['vendor_code']
            if vendor_code:
                try:
                    vendor_code = Vendor.objects.get(
                        vendor_code=vendor_code
                    )
                except Vendor.DoesNotExist:
                    raise CommandError(
                        'Vendor "%s" does not exist' % vendor_code
                    )
            else:
                vendor_code = None

            unit_of_measure = options['unit_of_measure']
            try:
                unit_of_measure = UnitOfMeasure.objects.get(
                    uom=unit_of_measure
                )
            except UnitOfMeasure.DoesNotExist:
                raise CommandError(
                    'UnitOfMeasure "%s" does not exist' % unit_of_measure
                )

            part_number = options['part_number']
            try:
                part_number = Parts.objects.get(
                    part_number=part_number
                )
            except Parts.DoesNotExist:
                raise CommandError(
                    'Parts "%s" does not exist' % part_number
                )

            part_type = options['part_type']
            try:
                part_type = Type.objects.get(
                    type_name=part_type
                )
            except Type.DoesNotExist:
                raise CommandError(
                    'Type "%s" does not exist' % part_type
                )

            received_date = options['received_date']
            invoice_number = options['invoice_number']
            invoice_date = options['invoice_date']
            invoice_quantity = options['invoice_quantity']
            received_quantity = options['received_quantity']
            defected_quantity = options['defected_quantity']
            batch_number = options['batch_number']
            recived_by = options['recived_by']
            remarks = options['remarks']
            transport_charges = options['transport_charges']

            inward = Inward(
                from_warehouse_name=from_warehouse_code,
                to_warehouse_name=to_warehouse_code,
                vendor_name=vendor_code,
                unit_of_measure=unit_of_measure,

                received_date=received_date,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                invoice_quantity=invoice_quantity,
                received_quantity=received_quantity,
                defected_quantity=defected_quantity,
                batch_number=batch_number,
                recived_by=recived_by,
                remarks=remarks,
                transport_charges=transport_charges,
                part_number=part_number,
                part_type=part_type,
            )
            inward.save()
            revisions.set_comment(
                "Created via CLI."
            )
            self.stdout.write(
                self.style.SUCCESS('Created Inward')
            )
