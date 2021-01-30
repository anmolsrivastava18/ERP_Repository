"""."""
from django import forms
from django.core.exceptions import ValidationError
import reversion as revisions
from reversion import create_revision
from ..inventory.models import (
    Asset,
    BillOfMaterial,
    Commodity,
    Parts,
    Product,
    Warehouse,
    Vendor,
    Inward,
    Outward,
    Type,
)
from ..inventory.utils import (
    get_bom_parts,
    cal_total_price,
)

empty = [('', '---------')]


class PartsCreateForm(forms.ModelForm):
    """Form For Creating Parts."""

    class Meta:
        """."""

        model = Parts
        fields = [
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
            'part_usermanual',
        ]

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['part_type'].queryset = Type.objects.all().exclude(
            type_name='ASSETAUTOOUTWARD'
        )


class PartsupdateForm(forms.ModelForm):
    """Form For updating the existing parts."""

    class Meta:
        """."""

        model = Parts
        fields = [
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
            'part_usermanual',
        ]
    part_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    part_number = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def clean_part_name(self):
        """."""
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.part_name
        else:
            return self.cleaned_data['part_name']

    def clean_part_number(self):
        """."""
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.part_number
        else:
            return self.cleaned_data['part_number']

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['part_type'].queryset = Type.objects.all().exclude(
            type_name='ASSETAUTOOUTWARD'
        )


class AssetForm(forms.Form):
    """."""

    product = forms.ChoiceField(
        label="Product Name",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose a Product from the list"
    )
    warehouse = forms.ChoiceField(
        label="Warehouse Name",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select a Warehouse"
    )

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['product'].choices = empty + [
            (
                prod.product_name,
                prod.product_name
            ) for prod in Product.objects.all()
        ]
        self.fields['warehouse'].choices = empty + [
            (
                ware.warehouse_name,
                ware.warehouse_name
            ) for ware in Warehouse.objects.all()
        ]

    def clean(self):
        """."""
        check = [self.cleaned_data['product'], self.cleaned_data['warehouse']]
        if any(check) and not all(check):
            # possible add some errors
            return self.cleaned_data
        raise ValidationError(
            'Select only one of the filed(product/warehouse)'
        )


class DefectPartsForm(forms.Form):
    """."""

    vendor_name = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Vendor Name',
        help_text="Select a Vendor"
    )
    st_date = forms.DateField(
        required=False,
        label="Start Date",
        help_text="Pick Start Date"
    )
    ed_date = forms.DateField(
        required=False,
        label="End Date",
        help_text="Pick End Date"
    )

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['vendor_name'].choices = empty + [
            (
                ven.vendor_name,
                ven.vendor_name
            ) for ven in Vendor.objects.all()
        ]

    def clean(self):
        """."""
        check = [self.cleaned_data['st_date'], self.cleaned_data['ed_date']]
        if all(check) or not any(check):
            # possible add some errors
            return self.cleaned_data
        raise ValidationError(
            'Select Start Date and End Date or not both filed'
        )


class AssetReportForm(forms.Form):
    """."""

    bom = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Bill Of Material',
        help_text="Select BOM"
    )
    st_date = forms.DateField(
        required=False,
        label="Start Date",
        help_text="Pick Start Date"
    )
    ed_date = forms.DateField(
        required=False,
        label="End Date",
        help_text="Pick End Date"
    )

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['bom'].choices = empty + [
            (
                bom.bom_name,
                bom.bom_name
            ) for bom in BillOfMaterial.objects.all()
        ]

    def clean(self):
        """."""
        check = [self.cleaned_data['st_date'], self.cleaned_data['ed_date']]
        if self.cleaned_data['bom'] and all(check):
            raise ValidationError(
                'Select Either BOM Name or Start and End Dates'
            )
        elif self.cleaned_data['bom']:
            return self.cleaned_data
        elif all(check):
            # possible add some errors
            return self.cleaned_data
        elif not self.cleaned_data['bom'] and not any(check):
            raise ValidationError(
                'Select BOM Name or Start and End Dates to fetch the Report'
            )
        raise ValidationError(
            'Select Start Date and End Date both filed'
        )


class CommodityWiseForm(forms.Form):
    """."""

    com = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='Commodity',
        help_text="Select Commodity"
    )
    warehouse = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select a Warehouse"
    )
    st_date = forms.DateField(
        required=True,
        label="Start Date",
        help_text="Pick Start Date"
    )
    ed_date = forms.DateField(
        required=True,
        label="End Date",
        help_text="Pick End Date"
    )

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['com'].choices = empty + [
            (
                com.commodity_name,
                com.commodity_name
            ) for com in Commodity.objects.all()
        ]
        self.fields['warehouse'].choices = empty + [
            (
                ware.warehouse_name,
                ware.warehouse_name
            ) for ware in Warehouse.objects.all()
        ]


class InwardForm(forms.ModelForm):
    """Inward Form."""

    class Meta:
        """."""

        model = Inward
        fields = [
            'part_type',
            'part_number',
            'part_name',
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
            'unit_of_measure',
            'transport_charges',
            'remarks',
        ]

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['part_type'].queryset = Type.objects.all().exclude(
            type_name='ASSETAUTOOUTWARD'
        )


class OutwardCreateForm(forms.ModelForm):
    """OutWard Form."""

    class Meta:
        """."""

        model = Outward
        fields = [
            'part_type',
            'part_number',
            'part_name',
            'quantity',
            'batch_number',
            'from_warehouse_name',
            'outward_receipt_number',
            'to_warehouse_name',
            'vendor_name',
            'authorised_by',
            'verified_by',
            'unit_of_measure',
            'mode_of_transport',
            'transport_charges',
            'remarks',
        ]

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['part_type'].queryset = Type.objects.all().exclude(
            type_name='ASSETAUTOOUTWARD'
        )


class PartsDemandForm(forms.Form):
    """."""

    bom = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='Bill Of Material',
        help_text="Select BOM"
    )
    quantity = forms.IntegerField(
        label="Asset Demand",
        min_value=1,
        max_value=99999,
        required=True,
        widget=forms.NumberInput()
    )
    warehouse = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select a Warehouse"
    )

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.fields['bom'].choices = empty + [
            (
                bom.bom_name,
                bom.bom_name
            ) for bom in BillOfMaterial.objects.all()
        ]
        self.fields['warehouse'].choices = empty + [
            (
                ware.warehouse_name,
                ware.warehouse_name
            ) for ware in Warehouse.objects.all()
        ]


class BomCompareForm(forms.Form):
    """."""

    bom_1 = forms.ChoiceField(
        label="BOM 1",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose a BOM from the list"
    )
    bom_2 = forms.ChoiceField(
        label="BOM 2",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose a BOM from the list"
    )

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        choices = empty + [
            (
                bom.bom_name,
                bom.bom_name,
            ) for bom in BillOfMaterial.objects.all()
        ]

        self.fields['bom_1'].choices = choices
        self.fields['bom_2'].choices = choices


class AssetCreateForm(forms.ModelForm):
    """."""

    class Meta:
        """."""

        model = Asset
        fields = [
            "product_name",
            "bom_name",
            "warehouse_name",
            "mfg_date",
            # "quantity",
            "asset_state",
            "remarks",
        ]

    def save(self, *args, **kwargs):
        """."""
        with create_revision():
            form_data = super().save(commit=False)
            bom_name = self.cleaned_data['bom_name']
            warehouse_name = self.cleaned_data['warehouse_name']
            parts = get_bom_parts(bom_name)
            form_data.parts = parts
            form_data.total_price = cal_total_price(bom_name)
            # Create outwards for parts used in asset creation.
            for part in parts:
                part_obj = Parts.objects.get(part_number=part['PartNumber'])
                quantity = part['Qty']
                authorised_by = "asset_auto_creation"
                verified_by = "asset_auto_creation"
                mode_of_transport = "asset_auto_creation"
                remarks = "This outward was created due to asset creation."

                Outward.objects.create(
                    part_type=Type.objects.get(type_name="ASSETAUTOOUTWARD"),
                    part_number=part_obj,
                    part_name=part_obj.part_name,
                    quantity=quantity,
                    from_warehouse_name=warehouse_name,
                    to_warehouse_name=warehouse_name,
                    authorised_by=authorised_by,
                    verified_by=verified_by,
                    mode_of_transport=mode_of_transport,
                    unit_of_measure=part_obj.unit_of_measure,
                    remarks=remarks,
                )

            form_data.save()
            revisions.set_comment("Updated from web form.")
            return form_data
