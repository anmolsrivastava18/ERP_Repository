"""."""
import os
import django
import random
from django.core.files.uploadedfile import SimpleUploadedFile
from random import choice, choices, randint
import string
from datetime import date, timedelta
from django.db.models import Max
from faker import Faker
import shutil
import requests
import json
from django.core.files.uploadedfile import SimpleUploadedFile


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()


from aims.inventory.models import (
    Availability,
    Type,
    Commodity,
    UnitOfMeasure,
    Warehouse,
    Parts,
    Inward,
    Outward,
    Vendor,
    Overseasinvoice,
    Domesticinvoice,
    Product,
    Asset,
    BillOfMaterial,
)


obj = Faker()

part_type = ["Regular", "Sample", "One-time", "Tool", "ASSETAUTOOUTWARD"]
commodity_list = [
    "Sheet Metal",
    "Hardware",
    "LEDs",
    "Controllers",
    "Equipments",
    "Consumables",
    "Tools",
    "LED's",
]

uom_list = [
    "Each",
    "Meter",
    "Litre",
    "Kg",
]

availab_list = [
    "Easy",
    "On Order",
    "Critical",
]
image_path = './aims/media/image/EXIDE_Battery.jpg'


def add_part_type():
    """."""
    for i in part_type:
        typ = Type.objects.get_or_create(type_name=i)[0]
        typ.save()


def get_part_typr():
    """."""
    typ = Type.objects.get_or_create(type_name=random.choice(part_type))[0]
    typ.save()
    return typ


def add_commodity():
    """."""
    for i in commodity_list:
        commodity = Commodity.objects.get_or_create(commodity_name=i)[0]
        commodity.save()


def get_commodity():
    """."""
    commodity = Commodity.objects.get_or_create(
        commodity_name=random.choice(commodity_list))[0]
    commodity.save()
    return commodity


def add_availability():
    """."""
    for i in availab_list:
        availability = Availability.objects.get_or_create(availability=i)[0]
        availability.save()


def get_availability():
    """."""
    availability = Availability.objects.get_or_create(
        availability=random.choice(availab_list))[0]
    availability.save()
    return availability


def add_unitofmeasure():
    """."""
    for i in uom_list:
        uom = UnitOfMeasure.objects.get_or_create(uom=i)[0]
        uom.save()


def get_unitofmeasure():
    """."""
    uom = UnitOfMeasure.objects.get_or_create(
        uom=random.choice(uom_list))[0]
    uom.save()
    return uom


def add_warehouses(N=10):
    """."""
    for entry in range(N):
        warehouse_name = obj.name()
        address = obj.address()[0:30]
        city = obj.city()
        phone_number = f"9999999900{entry}"
        warehouse_email = warehouse_name + "@adonmo.com"
        incharge_name = obj.first_name()
        incharge_email = incharge_name + "@adonmo.com"
        incharge_phone_number = f"9999998800{entry}"
        aims_person = obj.first_name()
        aims_person_phone_number = f"9999978801{entry}"
        warehosues = Warehouse.objects.get_or_create(
            warehouse_name=warehouse_name,
            address=address,
            city=city,
            phone_number=phone_number,
            warehouse_email=warehouse_email,
            incharge_name=incharge_name,
            incharge_email=incharge_email,
            incharge_phone_number=incharge_phone_number,
            aims_person=aims_person,
            aims_person_phone_number=aims_person_phone_number,
        )[0]
        warehosues.save()


def get_warehouse():
    """."""
    max_id = Warehouse.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        warehouse = Warehouse.objects.filter(pk=pk).first()
        if warehouse:
            return warehouse


def add_part(N=20):
    """."""
    for entry in range(N):
        part_name = obj.name()
        part_number = obj.random_number(12)
        part_type = get_part_typr()
        part_description = part_name
        vendor_name = obj.company()
        commodity_name = get_commodity()
        weight = "10Kg"
        part_class = "A1"
        dimensions = "20*10*10"
        tech_spec = "NA"
        part_life = obj.day_of_month()
        reorder_point = obj.random_number(2)
        lead_time = obj.random_number(2)
        safety_stock = obj.random_number(2)
        availability = get_availability()
        unit_of_measure = get_unitofmeasure()
        part_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg'
        )
        part = Parts.objects.get_or_create(
            part_name=part_name,
            part_number=part_number,
            part_type=part_type,
            part_description=part_description,
            vendor_name=vendor_name,
            commodity_name=commodity_name,
            weight=weight,
            part_class=part_class,
            dimensions=dimensions,
            tech_spec=tech_spec,
            part_life=part_life,
            reorder_point=reorder_point,
            lead_time=lead_time,
            safety_stock=safety_stock,
            availability=availability,
            unit_of_measure=unit_of_measure,
            part_image=part_image,
        )[0]
        part.save()


def get_part():
    """."""
    max_id = Parts.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        part = Parts.objects.filter(pk=pk).first()
        if part:
            return part


def add_vendor(N=20):
    """."""
    for entry in range(N):
        vendor_name = obj.company()
        vendor_address = obj.address()[0:30]
        vendor_poc = obj.name()
        email1 = vendor_poc + "1@vendor.com"
        email2 = vendor_poc + "2@vendor.com"
        phone_number1 = f"9999978801{entry}"
        phone_number2 = f"9999978802{entry}"
        products_available = obj.safe_color_name()
        procured_by_adm = products_available
        vendor_since = obj.date()
        adm_poc = obj.name()
        vendor = Vendor.objects.get_or_create(
            vendor_name=vendor_name,
            vendor_address=vendor_address,
            vendor_poc=vendor_poc,
            email1=email1,
            email2=email2,
            phone_number1=phone_number1,
            phone_number2=phone_number2,
            products_available=products_available,
            procured_by_adm=procured_by_adm,
            vendor_since=vendor_since,
            adm_poc=adm_poc
        )[0]
        vendor.save()


def get_vendor():
    """."""
    max_id = Vendor.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        vendor = Vendor.objects.filter(pk=pk).first()
        if vendor:
            return vendor


def add_domesticinvoce(N=20):
    """."""
    for i in range(0, N):
        part = get_part()
        invoice_amount = randint(1, 11) * 1000
        invoice_gst = choice([18, 20, 28])
        invoice_gst_amount = invoice_amount + ((invoice_amount * invoice_gst) / 100)
        transport_charges = randint(1, 5) * 200
        total_invoice_amount = invoice_gst_amount + transport_charges
        Domesticinvoice.objects.get_or_create(
            part_number=part,
            part_name=part.part_name,
            unit_of_measure=get_unitofmeasure(),
            vendor_name=get_vendor(),
            invoice_number=obj.random_number(7),
            invoice_date=date.today() + timedelta(days=choice(range(1, 20))),
            invoice_quantity=choice(range(5, 50)),
            invoice_amount=invoice_amount,
            invoice_gst=invoice_gst,
            invoice_gst_amount=invoice_gst_amount,
            transport_charges=transport_charges,
            total_invoice_amount=total_invoice_amount,
            stage=f"stage-{randint(1,5)}"
        )


def add_inward(N=30):
    """."""
    for i in range(0, N):
        part = get_part()
        invoice_amount = randint(1, 11) * 1000
        received_date = date.today() + timedelta(days=choice(range(1, 20)))
        invoice_gst = choice([18, 20, 28])
        invoice_gst_amount = invoice_amount + ((invoice_amount * invoice_gst) / 100)
        transport_charges = randint(1, 5) * 200
        total_invoice_amount = invoice_gst_amount + transport_charges
        vendor_name = get_vendor()
        invoice_number = obj.random_number(7)
        invoice_date = date.today() + timedelta(days=choice(range(1, 20)))
        invoice_quantity = choice(range(5, 50))
        received_quantity = invoice_quantity
        defected_quantity = choice(range(5, 10))
        batch_number = obj.random_number(7)
        recived_by = obj.name()
        to_warehouse_name = get_warehouse()
        # print(part.part_type)
        inward = Inward.objects.get_or_create(
            part_type=part.part_type,
            part_number=part,
            part_name=part.part_name,
            received_date=received_date,
            vendor_name=vendor_name,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            invoice_quantity=invoice_quantity,
            received_quantity=received_quantity,
            defected_quantity=defected_quantity,
            batch_number=batch_number,
            recived_by=recived_by,
            to_warehouse_name=to_warehouse_name,
            unit_of_measure=part.unit_of_measure
        )


def add_outward(N=15):
    """."""
    for i in range(0, N):
        part = get_part()
        quantity = choice(range(5, 10))
        from_warehouse_name = get_warehouse()
        vendor_name = get_vendor()
        authorised_by = obj.name()
        verified_by = obj.name()
        outward = Outward.objects.create(
            part_type=part.part_type,
            part_number=part,
            part_name=part.part_name,
            quantity=quantity,
            from_warehouse_name=from_warehouse_name,
            vendor_name=vendor_name,
            authorised_by=authorised_by,
            verified_by=verified_by,
            mode_of_transport=str("DTDC"),
            unit_of_measure=part.unit_of_measure
        )


def add_overseasinvoice(N=15):
    """."""
    for i in range(0, N):
        part = get_part()
        vendor_name = get_vendor()
        invoice_number = obj.random_number(7)
        invoice_date = date.today() + timedelta(days=choice(range(1, 20)))
        invoice_quantity = choice(range(5, 50))
        invoice_amount = randint(1, 11) * 1000
        invoice_gst = choice([18, 20, 28])
        invoice_gst_amount = invoice_amount + ((invoice_amount * invoice_gst) / 100)
        total_invoice_amount = invoice_amount + invoice_gst_amount
        boe_number = obj.random_number(8)
        boe_date = date.today() + timedelta(days=choice(range(1, 25)))
        total_duty_amount = 2000
        fright_agency = obj.name()
        weight = obj.random_number(3)
        fright_invoice_number = obj.random_number(8)
        fright_invoice_date = date.today() + timedelta(days=choice(range(1, 25)))
        total_fright_amount = 1500
        clearance_agency = obj.name()
        clearance_invoice_number = obj.random_number(8)
        clearance_invoice_date = date.today() + timedelta(days=choice(range(1, 25)))
        local_transport_fee = 200
        total_clearance_amount = 1000
        invoice = Overseasinvoice.objects.get_or_create(
            part_number=part,
            part_name=part.part_name,
            unit_of_measure=part.unit_of_measure,
            vendor_name=get_vendor(),
            vendor_code=vendor_name.vendor_code,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            invoice_quantity=invoice_quantity,
            invoice_amount=invoice_amount,
            invoice_gst_amount=invoice_gst_amount,
            total_invoice_amount=total_invoice_amount,
            boe_number=boe_number,
            boe_date=boe_date,
            total_duty_amount=total_duty_amount,
            fright_agency=fright_agency,
            weight=weight,
            fright_invoice_number=fright_invoice_number,
            fright_invoice_date=fright_invoice_date,
            total_fright_amount=total_fright_amount,
            clearance_agency=clearance_agency,
            clearance_invoice_number=clearance_invoice_number,
            clearance_invoice_date=clearance_invoice_date,
            local_transport_fee=local_transport_fee,
            total_clearance_amount=total_clearance_amount
        )


def create_boms(N=30):
    for _ in range(0, N):
        print('.')
        parts = Parts.objects.all()
        parts_objs = set(random.choices(parts, k=obj.random_int(3, 8)))
        parts_list = []
        for part in parts_objs:
            parts_list.append(
                {"Qty": obj.random_int(1, 20),
                 "Remarks": obj.paragraph()[:50],
                 "PartName": part.part_name,
                 "PartNumber": part.part_number,
                 "BatchNumber": ""}
            )
        name = obj.name()

        c = requests.get(
            f'https://dummyimage.com/500x500/d18cd1/fff&text={name}',
            stream=True
        ).content

        BillOfMaterial.objects.get_or_create(
            bom_name=name,
            bom_description=obj.paragraph()[:100],
            parts=parts_list,
            bom_file=SimpleUploadedFile(
                name=f'{name}.png',
                content=c,
                content_type='image/png',
            ),
            remarks=obj.paragraph()[:100],
        )


def create_products(N=5):
    """."""
    for i in range(0, N):
        Product.objects.get_or_create(
            product_name=obj.name(),
            description=obj.paragraph()[:100],
        )


if __name__ == '__main__':
    print("Populating Data...")
    print("Populating Parts Types Model..")
    add_part_type()
    print("Populating Parts Commodity Model..")
    add_commodity()
    print("Populating Parts Availability Model..")
    add_availability()
    print("Populating UnitOfMeasure Model..")
    add_unitofmeasure()
    print("Populating Warehouse Model..")
    add_warehouses()
    print("Populating Vendor Model..")
    add_vendor(N=30)
    print("Populating Parts Model..")
    add_part(N=30)
    print("Populating Domesticinvoice Model..")
    add_domesticinvoce(N=30)
    print("Populating Inward Model..")
    add_inward()
    print("Populating Outward Model..")
    add_outward()
    print("populating Overseasinvoice Model..")
    add_overseasinvoice()
    print("populating BillOfMaterial Model..")
    create_boms()
    print("populating Product Model..")
    create_products()
    print("Data Population completed")
