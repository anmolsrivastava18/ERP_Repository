"""."""
from django.core.management.base import BaseCommand
from django.db.models import (
    Sum,
)
from aims.inventory.models import (
    AveragePrice,
    Parts,
    Domesticinvoice,
    Overseasinvoice,
)


class Command(BaseCommand):
    """."""

    help = 'Calculate the AveragePrice of a Parts'

    def handle(self, *args, **options):
        """
        Calculate the Average Price of all Parts.

        Calculat the Sum of the total_invoice_amount and invoice_quantity of
        each part from Domestic and Overseas invoice models.
        Below is the output of Domestic
        {
            'part_number': 1, 'sum_of_total_invoice_amts': Decimal('3200.000'),
            'sum_of_invoice_qty': Decimal('22.000')
        }
        {
            'part_number': 2,
            'sum_of_total_invoice_amts': Decimal('2000.000'),
            'sum_of_invoice_qty': Decimal('10.000')
        }
        Below is the Output of Overseas
        {
            'part_number': 1, 'sum_of_total_invoice_amts': Decimal('3200.000'),
            'sum_of_invoice_qty': Decimal('22.000')
        }
        {
            'part_number': 4,
            'sum_of_total_invoice_amts': Decimal('2000.000'),
            'sum_of_invoice_qty': Decimal('20.000')
        }
        Mearge both the dicts as below
        {
            'part_number': 1, 'sum_of_total_invoice_amts': Decimal('6400.000'),
            'sum_of_invoice_qty': Decimal('44.000')
        }
        {
            'part_number': 2,
            'sum_of_total_invoice_amts': Decimal('2000.000'),
            'sum_of_invoice_qty': Decimal('10.000')
        }
        {
            'part_number': 4,
            'sum_of_total_invoice_amts': Decimal('2000.000'),
            'sum_of_invoice_qty': Decimal('20.000')
        }

        Save the average price to the AveragePrice Model.
        """
        domestic = list((
            Domesticinvoice.objects.values("part_number")
            .order_by("part_number")
            .annotate(
                sum_of_total_invoice_amts=Sum("total_invoice_amount"),
                sum_of_invoice_qty=Sum("invoice_quantity")
            )
        ))
        overseas = (
            Overseasinvoice.objects.values("part_number")
            .order_by("part_number")
            .annotate(
                sum_of_total_invoice_amts=Sum("total_amount"),
                sum_of_invoice_qty=Sum("invoice_quantity")
            )
        )
        parts_price = {}
        part_all = Parts.objects.values_list('pk', flat=True)
        for part in part_all:
            for rd in domestic:
                if part == rd['part_number']:
                    # print(rd)
                    if part not in parts_price:
                        parts_price[part] = [
                            rd['sum_of_total_invoice_amts'],
                            rd['sum_of_invoice_qty']
                        ]
                    else:
                        newrd_amount = (
                            parts_price[part][0] + rd['sum_of_total_invoice_amts']
                        )
                        newrd_qty = parts_price[part][1] + rd['sum_of_invoice_qty']
                        parts_price[part] = [newrd_amount, newrd_qty]

            for ro in overseas:
                if part == ro['part_number']:
                    if part not in parts_price:
                        parts_price[part] = [
                            ro['sum_of_total_invoice_amts'],
                            ro['sum_of_invoice_qty']
                        ]
                    else:
                        newro_amount = (
                            parts_price[part][0] + ro['sum_of_total_invoice_amts']
                        )
                        newrd_num = parts_price[part][1] + ro['sum_of_invoice_qty']
                        parts_price[part] = [newro_amount, newrd_num]

        for part in parts_price:
            obj = AveragePrice.objects.create(
                part_number=Parts.objects.get(pk=part),
                average_price=parts_price[part][0] / parts_price[part][1]
            )
            obj.save()

        self.stdout.write(self.style.SUCCESS("Calculated Average Price for every part."))
