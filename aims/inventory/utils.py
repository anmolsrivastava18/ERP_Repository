"""Contains Helper Methods for the Views."""
from django.core.exceptions import ObjectDoesNotExist
from ..inventory.models import (
    Parts,
    AveragePrice,
    BillOfMaterial,
)


def get_bom_parts(bom_name):
    """."""
    parts = BillOfMaterial.objects.get(bom_name=str(bom_name)).parts
    return parts


def get_avg_price_of_part(part_number):
    """Get Average Price of given Part."""
    parts_obj = Parts.objects.get(part_number=part_number)
    try:
        value = AveragePrice.objects.filter(
            part_number=parts_obj).latest('average_price').average_price
    except ObjectDoesNotExist:
        # Return 0 if average price of a part is not found.
        value = 0
    return {"avg_price": value}


def part_wise_prices(bom_name):
    """
    Returns
    -------
    The part wise prices for the BOM as a list of dicts of the format:
        [
            {
                "PartNumber": "...",
                "Qty": <float>,
                "AvgPrice": <float>,
            },
            ...
        ]
    """
    bom_parts = get_bom_parts(bom_name=bom_name)
    part_prices = []
    for part in bom_parts:
        part_number = part['PartNumber']
        part_qty = part['Qty']
        avg_price = get_avg_price_of_part(part_number)
        part_prices.append({
            "PartNumber": part_number,
            "Qty": float(part_qty),
            "AvgPrice": float(avg_price['avg_price']),
        })
    return part_prices


def cal_total_price(bom):
    """Calculate the total Price of the Asset for a given BOM Parts."""
    return sum([
        part['Qty'] * part['AvgPrice']
        for part in part_wise_prices(bom_name=bom)
    ])
