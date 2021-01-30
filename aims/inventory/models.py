"""All AIMS Models."""
from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
)
import datetime
from django.utils.text import slugify
from django.urls import reverse
import uuid
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_save
from django.utils.functional import cached_property


# Create your models here.
def gen_vendor_code():
    """Generate Vendor code."""
    last_vendor = Vendor.objects.all().count()
    return f"AV{last_vendor + 1:04}"


def gen_warehouse_code():
    """Generate warehouse code."""
    last_warehouse = Warehouse.objects.all().count()
    return f"AW{last_warehouse + 1:03}"


def get_parts(bom_name):
    """."""
    parts = BillOfMaterial.objects.get(bom_name=bom_name).parts
    return parts


def gen_orn():
    """.Generate Outward Receipt Number."""
    now_time = datetime.datetime.now()
    return "AORN/" + now_time.strftime("%d%m%Y/%H%M%S")


def gen_asset_id(warehouse_name):
    """Generate Asset ID."""
    warehouse_code = warehouse_name.warehouse_code
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    tmp_id = ("{}-{}-{}").format(
        warehouse_code, current_year, current_month
    )
    current_count = Asset.objects.filter(asset_id__startswith=tmp_id).count()
    # print("============", current_count, tmp_id, datetime.datetime.now())
    return ("{}-{}").format(tmp_id, f"{current_count + 1:05}")


class Type(models.Model):
    """Types Model."""

    type_name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Type',
        help_text='Name of the Type'
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Description',
        help_text='Description',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.type_name

    def __str__(self):
        """."""
        return self.type_name

    class Meta:
        """."""

        db_table = "Type"
        ordering = ["updated"]
        permissions = [('full_details_type', 'Can View Full Details Type')]


class Commodity(models.Model):
    """Commodity Model."""

    commodity_name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Commodity',
        help_text='Name of the Commodity'
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Description',
        help_text='Description',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.commodity_name

    def __str__(self):
        """."""
        return self.commodity_name

    class Meta:
        """."""

        db_table = "Commodity"
        ordering = ["updated"]
        permissions = [('full_details_commodity', 'Can View Full Details Commodity')]


class Availability(models.Model):
    """Availability Model"""

    availability = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Availability',
        help_text='Availability Status'
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Description',
        help_text='Description',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.availability

    def __str__(self):
        """."""
        return self.availability

    class Meta:
        """."""

        db_table = "Availability"
        ordering = ["updated"]
        permissions = [('full_details_availability', 'Can View Full Details Availability')]


class UnitOfMeasure(models.Model):
    """Types Model."""

    uom = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Unit Of Measure',
        help_text='Unit Of Measure for Parts',
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Description',
        help_text='Description',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.uom

    def __str__(self):
        """."""
        return self.uom

    class Meta:
        """."""

        db_table = "UnitOfMeasure"
        ordering = ["updated"]
        permissions = [('full_details_unitofmeasure', 'Can View Full Details UnitOfMeasure')]


class Parts(models.Model):
    """Parts Model."""

    part_name = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=100,
        verbose_name='Part Name',
    )

    part_number = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=12,
        validators=[MinLengthValidator(12)],
        verbose_name="Part Number",
        help_text='Unique Part Number'
    )

    part_type = models.ForeignKey(
        Type,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    part_description = models.CharField(
        max_length=500,
        verbose_name='Part Description',
    )

    vendor_name = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Vendor Name',
    )

    commodity_name = models.ForeignKey(
        Commodity,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    weight = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Weight',
    )

    part_class = models.CharField(
        blank=True,
        max_length=60,
        verbose_name='Part Class',
    )

    dimensions = models.CharField(
        blank=True,
        max_length=60,
        verbose_name='Part Dimensions',
    )

    tech_spec = models.CharField(
        blank=True,
        max_length=120,
        verbose_name='Tech Specifications',
    )

    part_life = models.CharField(
        blank=True,
        max_length=120,
        verbose_name='Part Life',
    )

    reorder_point = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Reorder Point",
    )

    lead_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Lead time (in Days)",
    )

    safety_stock = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Safety Stock",
    )

    availability = models.ForeignKey(
        Availability,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
    )

    part_usermanual = models.FileField(
        null=True,
        blank=True,
        upload_to='documents/',
        verbose_name='Part Documents',
        help_text='Any Documents Related to Part'
    )

    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.part_number

    def __str__(self):
        """."""
        return self.part_number

    def save(self, *args, **kwargs):
        """."""
        self.slug = slugify(self.part_number)
        super(Parts, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """."""
        return reverse('parts-detail', args=(self.slug,))

    class Meta:
        """."""

        db_table = "Part"
        ordering = ["updated"]
        permissions = [('full_details_parts', 'Can View Full Details Part')]


class Warehouse(models.Model):
    """Warehouse Model."""

    warehouse_name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Warehouse Name',
    )

    warehouse_code = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=10,
        default=gen_warehouse_code,
        editable=False,
        verbose_name='Warehouse Code',
    )

    address = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=120,
        verbose_name='Warehouse address',
    )

    city = models.CharField(
        null=False,
        blank=False,
        max_length=120,
        verbose_name='Warehouse City',
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17, blank=False, null=False,
    )  # validators should be a list

    warehouse_email = models.EmailField(verbose_name='Warehouse Email', )

    incharge_name = models.CharField(
        null=False,
        blank=False,
        max_length=120,
        verbose_name='Warehouse incharge',
    )

    incharge_email = models.EmailField(
        verbose_name='Warehouse Incharge Email'
    )

    incharge_phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name="Incharge's Contact No.",
    )

    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        """."""
        return self.warehouse_name

    def __str__(self):
        """."""
        return self.warehouse_name

    def save(self, *args, **kwargs):
        """."""
        self.slug = slugify(self.warehouse_code)
        super(Warehouse, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """."""
        return reverse('warehouse-detail', args=(self.slug,))

    class Meta:
        """."""

        db_table = "Warehouse"
        ordering = ["updated"]
        permissions = [('full_details_warehouse', 'Can View Full Details Warehouse')]


class Vendor(models.Model):
    """."""

    vendor_name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Vendor Name',
        help_text='Vendor Name',
    )
    vendor_code = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=10,
        default=gen_vendor_code,
        editable=False,
        verbose_name='Vendor Code',
        help_text='Vendor Code',
    )
    vendor_address = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=120,
        verbose_name='Vendor address',
        help_text='Vendor address',
    )
    vendor_poc = models.CharField(
        null=False,
        blank=False,
        max_length=120,
        verbose_name='Vendor POC',
        help_text='Vendor Point of Contact',
    )
    email1 = models.EmailField(verbose_name='Vendor Email-1', )
    email2 = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Vendor Email-2', )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number1 = models.CharField(
        null=False,
        blank=False,
        validators=[phone_regex],
        max_length=17,
        verbose_name='Vendor phone number 1',
    )  # validators should be a list
    phone_number2 = models.CharField(
        validators=[phone_regex],
        max_length=17, blank=True,
        verbose_name='Vendor phone number 2',
    )  # validators should be a list
    products_available = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        verbose_name='Type of Products Available',
        help_text='Type of Products Available',
    )
    procured_by_adm = models.CharField(
        null=False,
        blank=False,
        max_length=120,
        verbose_name='Components Procured by ADM',
        help_text='Components Procured by ADM',
    )
    vendor_since = models.DateField(
        auto_now=False
    )
    adm_poc = models.CharField(
        null=False,
        blank=False,
        max_length=120,
        verbose_name='ADM POC',
        help_text='ADM Point of Contact',
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='Warehouse Remarks',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        """."""
        return self.vendor_name

    def __str__(self):
        """."""
        return self.vendor_name

    def save(self, *args, **kwargs):
        """."""
        self.slug = slugify(self.vendor_code)
        super(Vendor, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """."""
        return reverse('vendor-detail', args=(self.slug,))

    class Meta:
        """."""

        db_table = "Vendor"
        ordering = ["updated"]
        permissions = [('full_details_vendor', 'Can View Full Details Vendor')]


class Inward(models.Model):
    """Inward Model."""

    part_type = models.ForeignKey(
        Type,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    part_number = models.ForeignKey(
        Parts,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
    )
    part_name = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Part Name',
        help_text='Name of the Part'
    )
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    received_date = models.DateField(
        verbose_name="In Date",
        help_text='Parts Inward Date'
    )
    vendor_name = models.ForeignKey(
        Vendor,
        null=True,
        blank=True,
        unique=False,
        on_delete=models.PROTECT,
        help_text='Select Vendor Name if Part is Procured'
    )
    # https://stackoverflow.com/questions/22538563/
    # django-reverse-accessors-for-foreign-keys-clashing
    from_warehouse_name = models.ForeignKey(
        Warehouse,
        null=True,
        blank=True,
        unique=False,
        on_delete=models.PROTECT,
        related_name="inward_from_warehouse_name",
        help_text='Select Warehouse Name if Part is internal transferred',
    )
    invoice_number = models.CharField(
        null=False,
        blank=False,
        max_length=40,
        verbose_name='Invoice Number',
        help_text='Invoice Number',
    )
    invoice_date = models.DateField(
        verbose_name="Invoice Date",
        help_text='Invoice Date'
    )
    invoice_quantity = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=0 if unit_of_measure == 'Each' else 2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Invoice Quantity',
        help_text='Invoice Quantity'
    )
    received_quantity = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=0 if unit_of_measure == 'Each' else 2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Received Quantity',
        help_text='Quantity Received'
    )
    defected_quantity = models.DecimalField(
        default=0,
        decimal_places=0 if unit_of_measure == 'Each' else 2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Defected Items Quantity',
        help_text='Defected Quantity Received'
    )
    batch_number = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Batch Number if any',
        help_text='Batch Number if any',
    )
    recived_by = models.CharField(
        null=False,
        blank=False,
        max_length=40,
        verbose_name='Items Received By',
        help_text='Enter Person Name',
    )
    # https://stackoverflow.com/questions/22538563/
    # django-reverse-accessors-for-foreign-keys-clashing
    to_warehouse_name = models.ForeignKey(
        Warehouse,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        help_text='Warehouse Name in which Part Inwarding',
        related_name="inward_to_warehouse_name",
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='Part Remarks',
    )
    transport_charges = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Transport Charges',
        help_text='Transport Charges if any'
    )
    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        """."""
        super(Inward, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """."""
        return reverse('inward-detail', args=(self.slug,))

    class Meta:
        """."""

        db_table = "Inward"
        ordering = ["updated"]
        permissions = [('full_details_inward', 'Can View Full Details Inward')]


class Outward(models.Model):
    """Outward"""

    part_type = models.ForeignKey(
        Type,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    part_number = models.ForeignKey(
        Parts,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
    )
    part_name = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Part Name',
        help_text='Name of the Part'
    )
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    quantity = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Quantity',
        help_text='Quantity'
    )
    batch_number = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Batch Number if any',
        help_text='Batch Number if any',
    )
    # https://stackoverflow.com/questions/22538563/
    # django-reverse-accessors-for-foreign-keys-clashing
    from_warehouse_name = models.ForeignKey(
        Warehouse,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        related_name="outward_from_warehouse_name",
        help_text="Warehouse from which part is being sent/outward",
    )
    outward_receipt_number = models.CharField(
        null=False,
        blank=False,
        max_length=40,
        default=gen_orn,
        verbose_name='Outward Receipt Number',
        help_text='Outward Receipt Number',
    )
    vendor_name = models.ForeignKey(
        Vendor,
        null=True,
        blank=True,
        unique=False,
        on_delete=models.PROTECT,
        help_text='Select Vendor Name if Part is sent to Vendor'
    )

    authorised_by = models.CharField(
        null=False,
        blank=False,
        max_length=20,
        verbose_name='Authorised By',
        help_text='Authorised User Name',
    )
    verified_by = models.CharField(
        null=False,
        blank=False,
        max_length=20,
        verbose_name='Verified By',
        help_text='Verified User Name',
    )
    # https://stackoverflow.com/questions/22538563/
    # django-reverse-accessors-for-foreign-keys-clashing
    to_warehouse_name = models.ForeignKey(
        Warehouse,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="outward_to_warehouse_name",
        help_text='Select Warehouse Name if Part is internal transfered',
    )
    mode_of_transport = models.CharField(
        max_length=120,
        verbose_name='Mode of Transport',
        help_text='Mode of Transport',
    )
    transport_charges = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Transport Charges',
        help_text='Transport Charges if any'
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='Part Remarks',
    )
    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.outward_receipt_number

    def __str__(self):
        """."""
        return self.outward_receipt_number

    def get_absolute_url(self):
        """."""
        return reverse('outward-detail', args=(self.slug,))

    class Meta:
        """."""

        db_table = "Outward"
        ordering = ["updated"]
        permissions = [('full_details_outward', 'Can View Full Details Outward')]


class Overseasinvoice(models.Model):
    """."""

    part_number = models.ForeignKey(
        Parts,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name='Part Number',
    )
    part_name = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Part Name',
        help_text='Name of the Part'
    )
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Unit of Measure',
    )
    vendor_name = models.ForeignKey(
        Vendor,
        null=True,
        blank=True,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name='Vendor Name',
    )
    vendor_code = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        editable=False,
        default=0,  # Overwritten during save
        verbose_name='Vendor Code',
        help_text='Vendor Code',
    )
    invoice_number = models.CharField(
        null=False,
        blank=False,
        max_length=40,
        verbose_name='Invoice Number',
        help_text='Invoice Number',
    )
    invoice_date = models.DateField(
        verbose_name="Invoice Date",
        help_text='Invoice Date'
    )
    invoice_quantity = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Invoice Quantity',
        help_text='Invoice Quantity'
    )
    invoice_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Invoice Amount',
        help_text='Invoice Amount'
    )
    invoice_gst = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Invoice GST %',
        help_text='Invoice GST Percentage'
    )
    invoice_gst_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Invoice GST Amount',
        help_text='Invoice GST Amount'
    )
    bank_charges = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Bank Charges',
        help_text='Bank Charges if any'
    )
    total_invoice_amount = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Invoice Amount',
        help_text='Sum of the Invoice amount + Invoice GST Amount + Banck Charges'
    )
    overseas_invoice = models.FileField(
        null=True,
        blank=True,
        upload_to='overseasinvoice/',
        verbose_name='Invoice',
        help_text='Invoice Related to this record'
    )
    # Customs Duty Fields
    boe_number = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='BOE Number',
        help_text='Bill of Entry Number',
    )
    boe_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="BOE Date",
        help_text='Bill of Entry Date'
    )
    bcd = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='BCD Percentage',
        help_text='Basic Customs Duty Percentage'
    )
    bcd_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='BCD Amount',
        help_text='Basic Customs Duty Amount'
    )
    customs_gst = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Customs GST %',
        help_text='Customs GST Percentage'
    )
    customs_gst_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Customs GST Amount',
        help_text='Customs GST Amount'
    )
    customs_fine_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Customs Fine Amount',
        help_text='Customs Fine Amount if any'
    )
    intrest_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Interest Amount',
        help_text='Interest Amount if any'
    )
    total_duty_amount = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Duty Amount',
        help_text='Sum of the BCD amount + Customs GST Amount + Fine Amount + Intrest Amount'
    )
    customs_invoice = models.FileField(
        null=True,
        blank=True,
        upload_to='overseasinvoice/customs',
        verbose_name='Customs Invoice',
        help_text='Customs Invoice Related to this record'
    )
    # Freight Fields
    fright_agency = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Freight Agency',
        help_text='Freight Agency Company Name',
    )
    weight = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='weight',
        help_text='Weight',
    )
    fright_invoice_number = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Freight Invoice Number',
        help_text='Freight Invoice Number',
    )
    fright_invoice_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Freight Invoice Date",
        help_text='Freight Invoice Date'
    )
    fright_charges_taxable = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Freight Charges Taxable',
        help_text='Taxable Freight Charges'
    )
    fright_gst = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Freight GST %',
        help_text='Freight GST Percentage'
    )
    fright_gst_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Freight GST Amount',
        help_text='Freight GST Amount'
    )
    fright_charges_nontaxable = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Freight Charges Non Taxable',
        help_text='Non Taxable Freight Charges'
    )
    total_fright_amount = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Freight Amount',
        help_text='Total Freight Amount'
    )
    fright_invoice = models.FileField(
        null=True,
        blank=True,
        upload_to='overseasinvoice/fright',
        verbose_name='Fright Invoice',
        help_text='Fright Invoice Related to this record'
    )
    # Clearance Fields
    clearance_agency = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Clearance Agency',
        help_text='Clearance Agency Company',
    )
    clearance_invoice_number = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Clearance Invoice Number',
        help_text='Clearance Invoice Number',
    )
    clearance_invoice_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Clearance Invoice Date",
        help_text='Clearance Invoice Date'
    )
    clearance_charges_taxable = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Clearance Charges Taxable',
        help_text='Taxable Clearance Charges'
    )
    clearance_gst = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Clearance GST %',
        help_text='Clearance GST Percentage'
    )
    clearance_gst_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Clearance GST Amount',
        help_text='Clearance GST Amount'
    )
    clearance_charges_nontaxable = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Clearance Charges Non Taxable',
        help_text='Non Taxable Clearance Charges'
    )
    local_transport_fee = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Local Transport Fee',
        help_text='Local Transport Fee'
    )
    total_clearance_amount = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Clearance Amount',
        help_text='Total Clearance Amount'
    )
    total_amount = models.DecimalField(
        default=0,  # Overwritten during save
        decimal_places=2,
        max_digits=12,
        editable=False,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Amount',
        help_text='Total Amount'
    )
    clearance_invoice = models.FileField(
        null=True,
        blank=True,
        upload_to='overseasinvoice/clearance',
        verbose_name='Clearance Invoice',
        help_text='Clearance Invoice Related to this record'
    )
    price_per_part = models.DecimalField(
        default=0,  # Overwritten during save
        editable=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Price per Part',
        help_text='Price per Part'
    )
    stage = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        verbose_name='Invoice Stage',
        help_text='Invoice Stage',
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='Part Remarks',
    )
    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        """Calculate sum before saving."""
        self.total_amount = self.calculate_sum()
        self.price_per_part = self.total_amount / self.invoice_quantity
        self.vendor_code = self.get_vendor_code()
        super(Overseasinvoice, self).save(*args, **kwargs)

    def calculate_sum(self):
        """Calculate a numeric value for the model instance."""
        return (
            self.total_invoice_amount + self.total_duty_amount +
            self.total_fright_amount + self.total_clearance_amount
        )

    def get_vendor_code(self, *args, **kwargs):
        """."""
        return self.vendor_name.vendor_code

    def get_absolute_url(self):
        """."""
        return reverse('overseasinvoice-detail', args=(self.slug,))

    def __unicode__(self):
        """."""
        return str(self.slug)

    def __str__(self):
        """."""
        return str(self.slug)

    class Meta:
        """."""

        db_table = "Overseasinvoice"
        ordering = ["updated"]
        permissions = [('full_details_overseasinvoice', 'Can View Full Details Overseasinvoice')]


class Domesticinvoice(models.Model):
    """."""

    invoice_number = models.CharField(
        null=False,
        blank=False,
        max_length=40,
        verbose_name='Invoice Number',
    )

    invoice_date = models.DateField(
        verbose_name="Invoice Date",
    )

    vendor_name = models.ForeignKey(
        Vendor,
        null=True,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name='Vendor Name',
    )

    total_invoice_amount = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Invoice Amount',
        help_text='Invoice amount + GST Amount'
    )

    transport_charges = models.DecimalField(
        null=False,
        blank=False,
        default=0,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Transport Charges',
    )

    Invoice_parts = JSONField(
        null=False,
        blank=False,
        default=dict
    )

    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='Invoice Remarks',
    )

    domestic_invoice = models.FileField(
        null=False,
        upload_to='domesticinvoice/',
        verbose_name='Invoice',
        help_text='Invoice Related to this record'
    )
    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        """."""
        return reverse('domesticinvoice-detail', args=(self.slug,))

    def __unicode__(self):
        """."""
        return str(self.slug)

    def __str__(self):
        """."""
        return str(self.slug)

    class Meta:
        """."""

        db_table = "Domesticinvoice"
        ordering = ["updated"]
        permissions = [('full_details_domesticinvoice', 'Can View Full Details Domesticinvoice')]


class IndividualDomesticinvoice(models.Model):
    part_number = models.ForeignKey(
        Parts,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name='Part Number',
    )

    part_name = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Part Name',
    )

    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Unit of Measure',
    )

    vendor_name = models.ForeignKey(
        Vendor,
        null=True,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name='Vendor Name',
    )

    invoice_number = models.CharField(
        null=False,
        blank=False,
        max_length=40,
        verbose_name='Invoice Number',
    )

    invoice_date = models.DateField(
        verbose_name="Invoice Date",
    )

    invoice_quantity = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Invoice Quantity',
    )

    invoice_amount = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Amount',
    )

    gst_percent = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='GST %',
    )

    gst_amount = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='GST Amount',
    )

    total_amount = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total Amount',
        help_text='Amount + GST Amount'
    )

    price_per_part = models.DecimalField(
        default=0,
        editable=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Price per Part',
    )

    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
    )

    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        """Calculate sum before saving."""
        self.price_per_part = self.total_amount / self.invoice_quantity
        super(IndividualDomesticinvoice, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """."""
        return reverse('individual_domestic_invoice-detail', args=(self.slug,))

    def __unicode__(self):
        """."""
        return str(self.slug)

    def __str__(self):
        """."""
        return str(self.slug)

    class Meta:
        """."""

        db_table = "IndividualDomesticinvoice"
        ordering = ["updated"]
        permissions = [('full_details_domesticinvoice', 'Can View Full Details Domesticinvoice')]


class AveragePrice(models.Model):
    """This Model Holds the Average Price of the each part."""

    part_number = models.ForeignKey(
        Parts,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name='Part Number',
    )
    average_price = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Average Price',
        help_text='Average Price of a part'
    )
    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return str(self.slug)

    def __str__(self):
        """."""
        return str(self.slug)

    class Meta:
        """."""

        db_table = "AveragePrice"
        ordering = ["updated"]
        permissions = [('full_details_averageprice', 'Can View Full Details AveragePrice')]


class BillOfMaterial(models.Model):
    bom_name = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=100,
        verbose_name='BOM Name',
        help_text='BOM name'
    )

    bom_description = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='BOM Description',
        help_text='BOM description'
    )

    parts = JSONField(
        null=False,
        blank=False,
        default=dict
    )

    bom_file = models.FileField(
        null=True,
        blank=True,
        upload_to='documents/',
        verbose_name='BOM Document',
        help_text='Any Documents Related to BOM'
    )

    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='BOM Remarks',
    )
    slug = models.SlugField(unique=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.bom_name

    def __str__(self):
        """."""
        return self.bom_name

    def get_absolute_url(self):
        """."""
        return reverse('bom-detail', args=(self.slug,))

    @cached_property
    def parts_with_prices(self):
        # Can't import globally as it might result in a circular import
        from ..inventory.utils import part_wise_prices
        part_prices = part_wise_prices(self.bom_name)
        prices = {
            part['PartNumber']: {
                'Price': part['AvgPrice'] * part['Qty'],
                'PricePerUnit': part['AvgPrice']
            }
            for part in part_prices
        }
        return [
            dict(part, **prices[part['PartNumber']])
            for part in self.parts
        ]

    @cached_property
    def price(self):
        # Can't import globally as it might result in a circular import
        from ..inventory.utils import cal_total_price
        return cal_total_price(self.bom_name)

    class Meta:
        """."""

        db_table = "BillOfMaterials"
        ordering = ["updated"]
        permissions = [('full_details_billofmaterial', 'Can View Full Details BillOfMaterials')]


class Product(models.Model):
    """Types Model."""

    product_name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Product Name',
        help_text='Name of the Product'
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Description',
        help_text='Description',
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return self.product_name

    def __str__(self):
        """."""
        return self.product_name

    class Meta:
        """."""

        db_table = "Product"
        ordering = ["updated"]
        permissions = [('full_details_product', 'Can View Full Details Product')]


class Asset(models.Model):
    """Assets Model."""

    asset_id = models.CharField(
        unique=True,
        max_length=100,
        editable=False,
    )
    product_name = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        unique=False,
        verbose_name="Product Name",
        on_delete=models.PROTECT,
    )
    bom_name = models.ForeignKey(
        BillOfMaterial,
        null=False,
        blank=False,
        unique=False,
        verbose_name="BOM Name",
        on_delete=models.PROTECT,
    )
    parts = JSONField(
        null=False,
        blank=False,
        default=dict,
        verbose_name='Parts Used Details',
    )
    warehouse_name = models.ForeignKey(
        Warehouse,
        null=False,
        blank=False,
        unique=False,
        on_delete=models.PROTECT,
        verbose_name="Warehouse Name",
        help_text='Select Warehouse Name where the part is in.',
    )
    mfg_date = models.DateField(
        verbose_name="Mfg Date",
        help_text='Mfg Date'
    )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name='Quantity',
        help_text='Quantity'
    )
    Asset_CHOICES = (
        ("On Lease", "Lease"),
        ("Warehouse Change", "Warehouse Change"),
        ("In warehouse", "In warehouse"),
    )
    asset_state = models.CharField(
        default="In warehouse",
        max_length=100,
        verbose_name="Asset State",
        choices=Asset_CHOICES
    )
    total_price = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=20,
        verbose_name='Total Price',
        help_text='Total Raw Material Cost of an Asset',
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='Remarks',
        help_text='Remarks',
    )
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        """."""
        return str(self.asset_id)

    def __str__(self):
        """."""
        return str(self.asset_id)

    def get_absolute_url(self):
        """."""
        return reverse('asset-detail', kwargs={'slug': self.slug})

    class Meta:
        """."""

        db_table = "Asset"
        ordering = ["updated"]
        permissions = [('full_details_asset', 'Can View Full Details Asset')]


def pre_save_asset_receiver(sender, instance, *args, **kwargs):
    """Generating Asset ID before saving the Asset."""
    if not instance.asset_id:
        instance.asset_id = gen_asset_id(instance.warehouse_name)
        instance.slug = slugify(instance.asset_id)


pre_save.connect(pre_save_asset_receiver, sender=Asset)
