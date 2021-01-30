"""."""
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reversion.admin import VersionAdmin
from ..inventory.models import (
    Parts,
    Type,
    Commodity,
    Availability,
    UnitOfMeasure,
    Warehouse,
    Vendor,
    Inward,
    Outward,
    Overseasinvoice,
    Domesticinvoice,
    AveragePrice,
    BillOfMaterial,
    Product,
    Asset,
    IndividualDomesticinvoice)


# Register your models here.
class PartsAdmin(admin.ModelAdmin):
    """."""

    list_display = [
        'part_name',
        'part_number',
        'part_type',
        'part_description',
        'vendor_name',
        'commodity_name',
        'weight',
        'part_class',
        'dimensions',
        'tech_spec',
        'part_life',
        'reorder_point',
        'lead_time',
        'safety_stock',
        'availability',
        'unit_of_measure',
        'remarks',
        'slug',
        'updated',
        'timestamp'
    ]
    prepopulated_fields = {"slug": ("part_number",)}

    class Meta:
        """."""

        model = Parts


class TypeAdmin(admin.ModelAdmin):
    """."""

    list_display = ['type_name', 'description']

    class Meta:
        """."""

        model = Type


class CommodityAdmin(admin.ModelAdmin):
    """."""

    list_display = ['commodity_name', 'description']

    class Meta:
        """."""

        model = Commodity


class AvailabilityAdmin(admin.ModelAdmin):
    """."""

    list_display = ['availability', 'description']

    class Meta:
        """."""

        model = Availability


class UnitOfMeasureAdmin(admin.ModelAdmin):
    """."""

    list_display = ['uom', 'description']

    class Meta:
        """."""

        model = UnitOfMeasure


class WarehouseAdmin(admin.ModelAdmin):
    """."""

    list_display = [
        'warehouse_name',
        'warehouse_code',
        'address',
        'city',
        'phone_number',
        'warehouse_email',
        'incharge_name',
        'incharge_email',
        'incharge_phone_number',
        'remarks',
    ]

    class Meta:
        """."""

        model = Warehouse


class VendorAdmin(admin.ModelAdmin):
    """."""

    list_display = [
        'vendor_name',
        'vendor_code',
        'vendor_address',
        'vendor_poc',
        'email1',
        'email2',
        'phone_number1',
        'phone_number2',
        'products_available',
        'procured_by_adm',
        'vendor_since',
        'adm_poc',
        'remarks'
    ]

    class Meta:
        """."""

        model = Vendor


class InwardResource(resources.ModelResource):
    """Inward Export Import Resource Class."""

    class Meta:
        """."""

        model = Inward
        fields = [
            'id',
            'part_type',
            'part_number',
            'part_name',
            'unit_of_measure',
            'received_date',
            'vendor_name',
            'from_warehouse_name',
            'invoice_number',
            'invoice_date',
            'invoice_quantity',
            'received_quantity',
            'defected_quantity',
            'batch_number',
            'recived_by',
            'to_warehouse_name',
            'remarks',
        ]


class InwardAdmin(ImportExportModelAdmin):
    """Inward Adimn Register."""

    resource_class = InwardResource

    list_display = [
        'part_type',
        'part_number',
        'part_name',
        'unit_of_measure',
        'received_date',
        'vendor_name',
        'from_warehouse_name',
        'invoice_number',
        'invoice_date',
        'invoice_quantity',
        'received_quantity',
        'defected_quantity',
        'batch_number',
        'recived_by',
        'to_warehouse_name',
        'remarks',
    ]


class OutwardResource(resources.ModelResource):
    """Outward Export Import Resource Class."""

    class Meta:
        """."""

        model = Outward
        fields = [
            'id',
            'part_type',
            'part_number',
            'part_name',
            'unit_of_measure',
            'quantity',
            'batch_number',
            'from_warehouse_name',
            'outward_receipt_number',
            'to_warehouse_name',
            'vendor_name',
            'authorised_by',
            'verified_by',
            'mode_of_transport',
            'transport_charges',
            'remarks',
        ]


class OutwardAdmin(ImportExportModelAdmin):
    """."""

    resource_class = OutwardResource
    list_display = [
        'part_type',
        'part_number',
        'part_name',
        'unit_of_measure',
        'quantity',
        'batch_number',
        'from_warehouse_name',
        'outward_receipt_number',
        'to_warehouse_name',
        'vendor_name',
        'authorised_by',
        'verified_by',
        'mode_of_transport',
        'transport_charges',
        'remarks',
    ]


class OverseasinvoiceResource(resources.ModelResource):
    """."""

    class Meta:
        """."""

        model = Overseasinvoice
        fields = [
            "id",
            "part_number",
            "part_name",
            "unit_of_measure",
            "vendor_name",
            "vendor_code",
            "invoice_number",
            "invoice_date",
            "invoice_quantity",
            "invoice_amount",
            "invoice_gst",
            "invoice_gst_amount",
            "bank_charges",
            "total_invoice_amount",
            "boe_number",
            "boe_date",
            "bcd",
            "bcd_amount",
            "customs_gst",
            "customs_gst_amount",
            "customs_fine_amount",
            "intrest_amount",
            "total_duty_amount",
            "fright_agency",
            "weight",
            "fright_invoice_number",
            "fright_invoice_date",
            "fright_charges_taxable",
            "fright_gst",
            "fright_gst_amount",
            "fright_charges_nontaxable",
            "total_fright_amount",
            "clearance_agency",
            "clearance_invoice_number",
            "clearance_invoice_date",
            "clearance_charges_taxable",
            "clearance_gst",
            "clearance_gst_amount",
            "clearance_charges_nontaxable",
            "local_transport_fee",
            "total_clearance_amount",
            "total_amount",
            "price_per_part",
            "stage",
            "remarks",
        ]


class OverseasinvoiceAdmin(ImportExportModelAdmin):
    """."""

    resource_class = OverseasinvoiceResource
    list_display = [
        "part_number",
        "part_name",
        "unit_of_measure",
        "vendor_name",
        "vendor_code",
        "invoice_number",
        "invoice_date",
        "invoice_quantity",
        "invoice_amount",
        "invoice_gst",
        "invoice_gst_amount",
        "bank_charges",
        "total_invoice_amount",
        "boe_number",
        "boe_date",
        "bcd",
        "bcd_amount",
        "customs_gst",
        "customs_gst_amount",
        "customs_fine_amount",
        "intrest_amount",
        "total_duty_amount",
        "fright_agency",
        "weight",
        "fright_invoice_number",
        "fright_invoice_date",
        "fright_charges_taxable",
        "fright_gst",
        "fright_gst_amount",
        "fright_charges_nontaxable",
        "total_fright_amount",
        "clearance_agency",
        "clearance_invoice_number",
        "clearance_invoice_date",
        "clearance_charges_taxable",
        "clearance_gst",
        "clearance_gst_amount",
        "clearance_charges_nontaxable",
        "local_transport_fee",
        "total_clearance_amount",
        "total_amount",
        "price_per_part",
        "stage",
        "remarks",
    ]


class DomesticinvoiceAdmin(VersionAdmin, admin.ModelAdmin):
    """."""

    list_display = [
        'invoice_number',
        'invoice_date',
        'vendor_name',
        'total_invoice_amount',
        'transport_charges',
        'Invoice_parts',
        'remarks',
        'domestic_invoice'
    ]

    class Meta:
        """."""

        model = Domesticinvoice


class IndividualDomesticinvoiceResource(resources.ModelResource):
    """Domesticinvoice Export Import Resource Class."""

    class Meta:
        """."""

        model = IndividualDomesticinvoice
        fields = [
            'id',
            'part_number',
            'part_name',
            'unit_of_measure',
            'vendor_name',
            'invoice_number',
            'invoice_date',
            'invoice_quantity',
            'invoice_amount',
            'gst_percent',
            'gst_amount',
            'total_amount',
            'price_per_part',
            'remarks',
        ]


class IndividualDomesticinvoiceAdmin(ImportExportModelAdmin):
    """."""

    resource_class = IndividualDomesticinvoice
    list_display = [
        'part_number',
        'part_name',
        'unit_of_measure',
        'vendor_name',
        'invoice_number',
        'invoice_date',
        'invoice_quantity',
        'invoice_amount',
        'gst_percent',
        'gst_amount',
        'total_amount',
        'price_per_part',
        'remarks',
    ]


class AveragePriceAdmin(admin.ModelAdmin):
    """."""

    list_display = [
        'id',
        'part_number',
        'average_price',
        'updated',
        'timestamp',
    ]

    class Meta:
        """."""

        model = AveragePrice


class BillOfMaterialAdmin(VersionAdmin, admin.ModelAdmin):
    """."""

    list_display = [
        'bom_name',
        'bom_description',
        'parts',
        'bom_file',
        'remarks',
    ]

    class Meta:
        """."""

        model = BillOfMaterial


class ProductAdmin(admin.ModelAdmin):
    """."""

    list_display = [
        'product_name',
        'description',
    ]

    class Meta:
        """."""

        model = Product


@admin.register(Asset)
class AssetAdmin(VersionAdmin, admin.ModelAdmin):
    """."""

    list_display = [
        'asset_id',
        'product_name',
        'bom_name',
        # 'parts',
        'warehouse_name',
        'quantity',
        'asset_state',
        'total_price',
        'remarks'
    ]

    class Meta:
        """."""

        model = Asset


admin.site.register(Parts, PartsAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Inward, InwardAdmin)
admin.site.register(Outward, OutwardAdmin)
admin.site.register(Overseasinvoice, OverseasinvoiceAdmin)
admin.site.register(Domesticinvoice, DomesticinvoiceAdmin)
admin.site.register(AveragePrice, AveragePriceAdmin)
admin.site.register(BillOfMaterial, BillOfMaterialAdmin)
admin.site.register(Product, ProductAdmin)
