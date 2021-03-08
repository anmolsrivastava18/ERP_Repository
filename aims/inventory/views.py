"""."""
from datetime import datetime
from html import unescape
import ast
import psutil

# Imported as recommended in the low-level API docs:
# https://django-reversion.readthedocs.org/en/latest/api.html?#importing-the-low-level-api
import reversion as revisions
from reversion import create_revision

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import (
    Avg,
    Count,
    ExpressionWrapper,
    Func,
    F,
    Sum,
    Value,
    DecimalField,
)
from django.core import serializers
from django.http import HttpResponse
from django.utils.html import escape
from django.utils.timezone import localtime
from django.views.generic.edit import (
    CreateView,
    # DeleteView,
    UpdateView,
)

from ..inventory.models import (
    Warehouse,
    Availability,
    Type,
    Commodity,
    UnitOfMeasure,
    Parts,
    Domesticinvoice,
    Inward,
    Outward,
    Vendor,
    Overseasinvoice,
    AveragePrice,
    BillOfMaterial,
    Product,
    Asset,
    IndividualDomesticinvoice)

from ..inventory.forms import (
    AssetReportForm,
    AssetForm,
    AssetCreateForm,
    CommodityWiseForm,
    PartsCreateForm,
    PartsupdateForm,
    DefectPartsForm,
    InwardForm,
    OutwardCreateForm,
    PartsDemandForm,
    BomCompareForm,
)
from ..inventory.utils import (
    get_bom_parts,
    cal_total_price,
)


@login_required
def home(request):
    """."""
    return render(request, 'index.html')

@login_required
def get_stock(request):
    """
    Below is the Get Stock Format displayed in the UI.

    | Part No.     |Part Name   | Total Stock     | Defect Stock | Total Usable Stock          | Reorder point | Safety stock |
    |--------------|------------------------------|--------------|-----------------------------| ------------- | ------------ |
    | Part_number  | Part_name | = inward-outward | Defect stock | = Total Stock - DefectStock | Reorder point | Safety stock |
    """
    if request.method == "GET" and not request.is_ajax():
        warehouses = Warehouse.objects.all()
        context = {
            "warehouses": warehouses,
        }
        return render(request, 'inventory/stock.html', context=context)
    else:
        partnames = {}
        try:
            warehouse = request.GET.get("warehouse")
            if warehouse == "all_warehouses":
                partnames = calculate_stock()
            else:
                warehouse_obj = Warehouse.objects.get(warehouse_code=warehouse)
                partnames = calculate_stock(warehouse_obj)
        except Warehouse.DoesNotExist as e:
            return JsonResponse({"success": False,
                                 "error": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"success": False,
                                 "error": str(e)}, status=400)
        return JsonResponse(partnames, status=200)
    return JsonResponse({"success": False}, status=405)


def calculate_stock(warehouse=None, safety_stock=None):
    """Calculating the Available Stock."""
    if not warehouse:
        if not safety_stock:
            inwards = (
                Inward.objects.values(
                    "part_number__part_number",
                    "part_number__part_name",
                    "part_number__safety_stock",
                    "part_number__reorder_point"
                ).order_by("part_number__part_name")
                    .annotate(
                    inw_received_qt_total=Sum("received_quantity"),
                    defect_qt_total=Sum("defected_quantity"),
                )
            )
            outwards = (
                Outward.objects.values(
                    "part_number__part_name",
                    "part_number__safety_stock"
                ).order_by("part_number__part_name")
                    .annotate(outward_qt_total=Sum("quantity"))
            )
        else:
            inwards = (
                Inward.objects.values(
                    "part_number__part_number",
                    "part_number__part_name",
                    "part_number__safety_stock",
                    "part_number__reorder_point"
                ).order_by("part_number__part_name")
                    .annotate(
                    inw_received_qt_total=Sum("received_quantity"),
                    defect_qt_total=Sum("defected_quantity"),
                ).filter(
                    inw_received_qt_total__lte=F("part_number__safety_stock")
                )
            )
            outwards = (
                Outward.objects.values(
                    "part_number__part_name",
                    "part_number__safety_stock"
                ).order_by("part_number__part_name")
                    .annotate(outward_qt_total=Sum("quantity"))
            ).filter(
                outward_qt_total__lte=F("part_number__safety_stock")
            )
    else:
        if not safety_stock:
            inwards = (
                Inward.objects.filter(to_warehouse_name=warehouse)
                    .values(
                    "part_number__part_number",
                    "part_number__part_name",
                    "part_number__safety_stock",
                    "part_number__reorder_point"
                ).order_by("part_number__part_name")
                    .annotate(
                    inw_received_qt_total=Sum("received_quantity"),
                    defect_qt_total=Sum("defected_quantity"),
                )
            )
            outwards = (
                Outward.objects.filter(from_warehouse_name=warehouse).values(
                    "part_number__part_name",
                    "part_number__safety_stock"
                ).order_by("part_number__part_name").annotate(outward_qt_total=Sum("quantity"))
            )
        else:
            inwards = (
                Inward.objects.filter(to_warehouse_name=warehouse)
                    .values(
                    "part_number__part_number",
                    "part_number__part_name",
                    "part_number__safety_stock",
                    "part_number__reorder_point"
                ).order_by("part_number__part_name")
                    .annotate(
                    inw_received_qt_total=Sum("received_quantity"),
                    defect_qt_total=Sum("defected_quantity"),
                ).filter(
                    inw_received_qt_total__lte=F("part_number__safety_stock")
                )
            )
            outwards = (
                Outward.objects.filter(from_warehouse_name=warehouse)
                    .values(
                    "part_number__part_name",
                    "part_number__safety_stock"
                ).order_by("part_number__part_name")
                    .annotate(
                    outward_qt_total=Sum("quantity")
                ).filter(
                    outward_qt_total__lte=F("part_number__safety_stock")
                )
            )
    partnames = {}

    for inward in inwards:
        partnames[inward['part_number__part_name']] = \
            {
                'Part Number': inward['part_number__part_number'],
                'Re-order Point': inward['part_number__reorder_point'],
                'inward': inward['inw_received_qt_total'],
                'defect': inward['defect_qt_total'],
                'outward': 0,
                'safety_stock': inward["part_number__safety_stock"],
                'total_usable_stock': inward['inw_received_qt_total'] - inward['defect_qt_total'],
                'total_stock': inward['inw_received_qt_total'],
            }
    for outward in outwards:
        outward_partname = outward['part_number__part_name']
        if outward_partname in partnames:
            partnames[outward_partname]['outward'] = \
                outward['outward_qt_total']

            partnames[outward_partname]['total_stock'] -= \
                partnames[outward_partname]['outward']

            partnames[outward_partname]['total_usable_stock'] -= \
                partnames[outward_partname]['outward']
    return (partnames)


def calculate_stock_batch(warehouse=None, safety_stock=None):
    """Calculating the Available Stock."""
    if not warehouse:
        inwards = (
            Inward.objects.values(
                "part_number__part_name",
                "batch_number"
            ).order_by("part_number__part_name")
                .annotate(
                inw_received_qt_total=Sum("received_quantity"),
                defect_qt_total=Sum("defected_quantity"),
            )
        )

        outwards = (
            Outward.objects.values(
                "part_number__part_name",
                "batch_number"
            ).order_by("part_number__part_name")
                .annotate(outward_qt_total=Sum("quantity"))
        )

    else:
        inwards = (
            Inward.objects.filter(to_warehouse_name=warehouse)
                .values(
                "part_number__part_name",
                "batch_number"
            ).order_by("part_number__part_name")
                .annotate(
                inw_received_qt_total=Sum("received_quantity"),
                defect_qt_total=Sum("defected_quantity"),
            )
        )
        outwards = (
            Outward.objects.filter(from_warehouse_name=warehouse)
                .values(
                "part_number__part_name",
                "batch_number"
            ).order_by("part_number__part_name")
                .annotate(outward_qt_total=Sum("quantity"))
        )

    partnames = []

    for inward in inwards:
        partnames.append({
            'part_name': inward['part_number__part_name'],
            'inward': inward['inw_received_qt_total'],
            'defect': inward['defect_qt_total'],
            'outward': 0,
            'batch_number': inward['batch_number'],
            'total_usable_stock': inward['inw_received_qt_total'] - inward['defect_qt_total'],
            'total_stock': inward['inw_received_qt_total'],
        })
    for outward in outwards:
        outward_partname = outward['part_number__part_name']
        outward_batch_number = outward['batch_number']
        for partname in partnames:
            if outward_partname in partname and outward_batch_number in partname:
                partname[outward_partname]['outward'] = \
                    outward['outward_qt_total']
                partname[outward_partname]['total_stock'] -= \
                    partname[outward_partname]['outward']

                partname[outward_partname]['total_usable_stock'] -= \
                    partname[outward_partname]['outward']

    return (partnames)


@login_required
def get_stock_batchnumber(request):
    """
    """
    if request.method == "GET" and not request.is_ajax():
        warehouses = Warehouse.objects.all()
        context = {
            "warehouses": warehouses,
        }
        return render(
            request,
            'inventory/get_stock_batch.html',
            context=context
        )
    else:
        partnames = {}
        try:
            warehouse = request.GET.get("warehouse")
            if warehouse == "all_warehouses":
                partnames = calculate_stock_batch(
                    warehouse=None
                )
            else:
                warehouse_obj = Warehouse.objects.get(warehouse_code=warehouse)
                partnames = calculate_stock_batch(
                    warehouse=warehouse_obj
                )
        except Warehouse.DoesNotExist as e:
            return JsonResponse({"success": False,
                                 "error": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"success": False,
                                 "error": str(e)}, status=400)
        return JsonResponse(partnames, safe=False, status=200)
    return JsonResponse({"success": False}, status=405)


@login_required
@permission_required('is_staff')
def get_avg_price(request):
    """
    Calculate the Average Price of all Parts.

    Calculate the Sum of the total_invoice_amount and invoice_quantity of
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
    Domestic = list((
        Domesticinvoice.objects.values("part_number")
            .order_by("part_number")
            .annotate(
            sum_of_total_invoice_amts=Sum("total_invoice_amount"),
            sum_of_invoice_qty=Sum("invoice_quantity")
        )
    ))
    Overseas = (
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
        for rd in Domestic:
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

        for ro in Overseas:
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

    return HttpResponse(status=200)


class WarehouseListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """All Warehouse List View."""

    model = Warehouse
    template_name = "inventory/warehouse_list.html"
    permission_required = 'inventory.view_warehouse'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class WarehouseListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the Warehouse list."""

    model = Warehouse
    columns = [
        'warehouse_name',
        'warehouse_code',
        'city',
        'incharge_name',
        'incharge_email',
        'incharge_phone_number',
        'updated'
    ]

    order_columns = [
        'warehouse_name',
        'warehouse_code',
        'city',
        'incharge_name',
        'incharge_email',
        'incharge_phone_number',
        'updated'
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        # Converting the date-time to human readable format.
        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        # Hyperlink for the Details View.
        if value and hasattr(obj, 'get_absolute_url') and column == 'warehouse_name':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


class WarehouseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """WareHouse Create View."""

    model = Warehouse
    fields = [
        'warehouse_name',
        'address',
        'city',
        'phone_number',
        'warehouse_email',
        'incharge_name',
        'incharge_email',
        'incharge_phone_number',
        'remarks',
    ]

    success_message = "Warehouse: %(warehouse_name)s Created Successfully"
    template_name = "inventory/warehouse_create.html"
    permission_required = 'inventory.add_warehouse'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """Get Warehouse-list on Success."""
        return reverse('warehouse-list')


class WarehouseUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """Updating a Warehouse."""

    model = Warehouse
    fields = [
        'warehouse_name',
        'address',
        'city',
        'phone_number',
        'warehouse_email',
        'incharge_name',
        'incharge_email',
        'incharge_phone_number',
        'remarks',
    ]

    success_message = "Warehouse: %(warehouse_name)s Updated Successfully"
    template_name = "inventory/warehouse_update.html"
    permission_required = 'inventory.change_warehouse'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('warehouse-list')


class WarehouseDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """Warehouse Details View."""

    model = Warehouse
    template_name = "inventory/warehouse_detail.html"
    permission_required = 'inventory.full_details_warehouse'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class AvailabilityListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """."""

    model = Availability
    template_name = "inventory/availability_list.html"
    permission_required = 'inventory.view_availability'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class AvailabilityCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    """."""

    model = Availability
    fields = ['availability', 'description']
    template_name = "inventory/availability_create.html"
    permission_required = 'inventory.add_availability'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, "You don't have permission to View this")
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('availability-list')


class TypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Type
    template_name = "inventory/type_list.html"
    permission_required = 'inventory.view_type'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class TypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """."""

    model = Type
    fields = ['type_name', 'description']
    template_name = "inventory/type_create.html"
    permission_required = 'inventory.add_type'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('type-list')


class CommodityListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Commodity
    template_name = "inventory/commodity_list.html"
    permission_required = 'inventory.view_commodity'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class CommodityCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    """Create Commodity."""

    model = Commodity
    fields = ['commodity_name', 'description']
    template_name = "inventory/commodity_create.html"
    # success_url = "inventory/commodity-list/"
    permission_required = 'inventory.add_commodity'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('commodity-list')


class PartsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Parts
    permission_required = 'inventory.view_parts'
    permission_denied_message = "User not allowed to this view."
    template_name = "inventory/parts_list.html"

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class PartsListJson(LoginRequiredMixin, BaseDatatableView):
    """For snapshot of the Parts list."""

    model = Parts
    columns = [
        'part_number',
        'part_name',
        'unit_of_measure.uom',
        'lead_time',
        'reorder_point',
        'safety_stock',
        'updated',
    ]

    order_columns = [
        'part_number',
        'part_name',
        'unit_of_measure.uom',
        'lead_time',
        'reorder_point',
        'safety_stock',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'part_number':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


def get_part_name(request):
    """Get PartName for a given partnumber. Used for auto-fill PartName."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    if request.method == "GET" and request.is_ajax():
        part_number = request.GET.get("part_number")
        try:
            part = Parts.objects.get(id=part_number)
        except Exception:
            return JsonResponse({"success": False}, status=400)
        return JsonResponse(
            {"part_name": part.part_name, "uom": part.unit_of_measure.id}, status=200)
    return JsonResponse({"success": False}, status=405)


def get_partID_partName_uomID(request):
    """Get PartID, Part name and the Unit of Measure ID. Used for creating individual invoices automatically."""

    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    if request.method == "GET" and request.is_ajax():
        part_number = request.GET.get("part_number")
        try:
            part = Parts.objects.get(part_number=part_number)
        except Exception:
            return JsonResponse({"success": False}, status=400)
        return JsonResponse(
            {"id": part.id, "part_name": part.part_name, "uom": part.unit_of_measure.id}, status=200)
    return JsonResponse({"success": False}, status=405)


def get_part_number_name(request):
    """Get PartName for a given partnumber. Used for auto-fill PartName."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    if request.method == "GET" and request.is_ajax():
        part_number = request.GET.get("searchTerm")
        try:
            parts = Parts.objects.filter(part_number__icontains=part_number)
            data = [
                {"id": part.part_number,
                 "text": part.part_number,
                 "part_name": part.part_name,
                 "unit": part.unit_of_measure.uom}
                for part in parts
            ]
        except Exception:
            return JsonResponse({"success": False}, status=400)
        return JsonResponse(data, safe=False, status=200)
    return JsonResponse({"success": False}, status=405)


def get_part_name_number(request):
    """Get partnumber for a given PartName. Used for auto-fill PartName."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    if request.method == "GET" and request.is_ajax():
        part_name = request.GET.get("searchTerm")
        try:
            parts = Parts.objects.filter(part_name__icontains=part_name)
            data = [
                {"id": part.part_name,
                 "text": part.part_name,
                 "part_number": part.part_number,
                 "unit": part.unit_of_measure.uom}
                for part in parts
            ]
        except Exception:
            return JsonResponse({"success": False}, status=400)
        return JsonResponse(data, safe=False, status=200)
    return JsonResponse({"success": False}, status=405)


class PartsCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Create Parts."""

    model = Parts
    permission_required = 'inventory.add_parts'
    permission_denied_message = "User not allowed to this view."
    form_class = PartsCreateForm
    template_name = "inventory/parts_create.html"
    success_message = "Part: %(part_name)s created successfully"

    def get_success_url(self):
        """After Creating part redirect to parts list."""
        return reverse('parts-list')

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class PartsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """."""

    model = Parts
    template_name = "inventory/parts_details.html"
    permission_required = 'inventory.full_details_parts'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class PartsUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """Update Parts."""

    model = Parts
    form_class = PartsupdateForm
    template_name = "inventory/parts_create.html"
    success_message = "Part: %(part_name)s updated successfully"
    permission_required = 'inventory.change_parts'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """After Creating part redirect to parts list."""
        return reverse('parts-list')


class DomesticinvoiceListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """Domestic Invoice List View."""

    model = Domesticinvoice
    template_name = "inventory/domesticinvoice_list.html"
    permission_required = 'inventory.view_domesticinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class DomesticinvoiceListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the Parts list."""

    model = Domesticinvoice
    columns = [
        'invoice_number',
        'invoice_date',
        'vendor_name.vendor_name',
        'total_invoice_amount',
        'transport_charges',
        'remarks',
        'updated',
    ]

    order_columns = [
        'invoice_number',
        'invoice_date',
        'vendor_name.vendor_name',
        'total_invoice_amount',
        'transport_charges',
        'remarks',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'invoice_number':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


class DomesticinvoiceCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """."""

    model = Domesticinvoice
    fields = [
        'invoice_number',
        'invoice_date',
        'vendor_name',
        'total_invoice_amount',
        'transport_charges',
        'Invoice_parts',
        'remarks',
        'domestic_invoice',
    ]
    success_message = "Invoice: %(invoice_number)s Created Successfully"
    template_name = "inventory/domesticinvoice_create.html"
    permission_required = 'inventory.add_domesticinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('domesticinvoice-list')


class DomesticinvoiceDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    model = Domesticinvoice
    template_name = "inventory/domesticinvoice_detail.html"
    permission_required = 'inventory.full_details_domesticinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class IndividualDomesticinvoiceListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """Individual Domestic Invoice List View."""

    model = IndividualDomesticinvoice
    template_name = "inventory/individual_domestic_invoice_list.html"
    permission_required = 'inventory.view_individual_domestic_invoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class IndividualDomesticinvoiceListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the Parts list."""

    model = IndividualDomesticinvoice
    columns = [
        'invoice_number',
        'invoice_date',
        'part_number.part_number',
        'part_name',
        'invoice_quantity',
        'unit_of_measure.uom',
        'vendor_name.vendor_name',
        'invoice_amount',
        'gst_percent',
        'total_amount',
        'updated',
    ]

    order_columns = [
        'invoice_number',
        'invoice_date',
        'part_number.part_number',
        'part_name',
        'invoice_quantity',
        'unit_of_measure.uom',
        'vendor_name.vendor_name',
        'invoice_amount',
        'gst_percent',
        'total_amount',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'invoice_number':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


class IndividualDomesticinvoiceCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """."""

    model = IndividualDomesticinvoice
    fields = [
        'invoice_number',
        'invoice_date',
        'vendor_name',
        'part_number',
        'part_name',
        'invoice_quantity',
        'unit_of_measure',
        'invoice_amount',
        'gst_percent',
        'gst_amount',
        'total_amount',
        'remarks'
    ]
    success_message = "Invoice: %(invoice_number)s Created Successfully"
    template_name = "inventory/individual_domestic_invoice_create.html"
    permission_required = 'inventory.add_individual_domestic_invoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('individual_domestic_invoice-list')


class IndividualDomesticinvoiceUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """."""

    model = IndividualDomesticinvoice
    fields = [
        'invoice_number',
        'invoice_date',
        'vendor_name',
        'part_number',
        'part_name',
        'invoice_quantity',
        'unit_of_measure',
        'invoice_amount',
        'gst_percent',
        'gst_amount',
        'total_amount',
        'remarks'
    ]
    success_message = "Invoice: %(invoice_number)s Updated Successfully"
    template_name = "inventory/individual_domestic_invoice_update.html"
    permission_required = 'inventory.change_individual_domestic_invoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('individual_domestic_invoice-list')


class IndividualDomesticinvoiceDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    model = IndividualDomesticinvoice
    template_name = "inventory/individual_domestic_invoice_detail.html"
    permission_required = 'inventory.full_details_individual_domestic_invoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class InwardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Inward
    template_name = "inventory/inward_list.html"
    permission_required = 'inventory.view_inward'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class InwardListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the Parts list."""

    model = Inward
    columns = [
        'invoice_number',
        'part_type.type_name',
        'part_number.part_number',
        'part_name',
        'unit_of_measure.uom',
        'received_date',
        'vendor_name.vendor_name',
        'from_warehouse_name.warehouse_name',
        'invoice_date',
        'invoice_quantity',
        'received_quantity',
        'defected_quantity',
        'to_warehouse_name.warehouse_name',
        'updated',
    ]

    order_columns = [
        'invoice_number',
        'part_type.type_name',
        'part_number.part_number',
        'part_name',
        'unit_of_measure.uom',
        'received_date',
        'vendor_name.vendor_name',
        'from_warehouse_name.warehouse_name',
        'invoice_date',
        'invoice_quantity',
        'received_quantity',
        'defected_quantity',
        'to_warehouse_name.warehouse_name',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'invoice_number':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


class InwardCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """."""

    model = Inward
    form_class = InwardForm
    success_message = "Inward For Part: %(part_name)s Created Successfully"
    template_name = "inventory/inward_create.html"
    permission_required = 'inventory.add_inward'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('inward-list')


class InwardDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    model = Inward
    template_name = "inventory/inward_detail.html"
    permission_required = 'inventory.full_details_domesticinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class VendorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Vendor
    template_name = "inventory/vendor_list.html"
    permission_required = 'inventory.view_vendor'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class VendorListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the Vendor list."""

    model = Vendor
    columns = [
        'vendor_name',
        'vendor_code',
        'vendor_poc',
        'email1',
        'phone_number1',
        'adm_poc',
        'updated',
    ]

    order_columns = [
        'vendor_name',
        'vendor_code',
        'vendor_poc',
        'email1',
        'phone_number1',
        'adm_poc',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'vendor_name':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


class VendorCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Vendor Create View."""

    model = Vendor
    fields = [
        "vendor_name",
        "vendor_address",
        "vendor_poc",
        "email1",
        "email2",
        "phone_number1",
        "phone_number2",
        "products_available",
        "procured_by_adm",
        "vendor_since",
        "adm_poc",
        "remarks",
    ]
    success_message = "Vendor: %(vendor_name)s was created successfully"
    template_name = "inventory/vendor_create.html"
    permission_required = 'inventory.add_vendor'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('vendor-list')


class VendorUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    """Updating an Existing Vendor."""

    model = Vendor
    fields = [
        "vendor_name",
        "vendor_address",
        "vendor_poc",
        "email1",
        "email2",
        "phone_number1",
        "phone_number2",
        "products_available",
        "procured_by_adm",
        "vendor_since",
        "adm_poc",
        "remarks",
    ]

    template_name = "inventory/vendor_update.html"
    permission_required = 'inventory.change_vendor'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('vendor-list')


class VendorDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    model = Vendor
    template_name = "inventory/vendor_detail.html"
    permission_required = 'inventory.full_details_vendor'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class OverseasinvoiceListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """Overseas Invoice List View."""

    model = Overseasinvoice
    template_name = "inventory/overseasinvoice_list.html"
    permission_required = 'inventory.view_overseasinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class OverseasinvoiceListJson(LoginRequiredMixin, BaseDatatableView):
    """."""

    model = Overseasinvoice
    columns = [
        "invoice_number",
        "part_number.part_number",
        "part_name",
        "unit_of_measure.uom",
        "vendor_name.vendor_name",
        "invoice_date",
        "invoice_quantity",
        "total_invoice_amount",
        "total_duty_amount",
        "total_fright_amount",
        "total_clearance_amount",
        "total_amount",
        "price_per_part",
        'updated',
    ]

    order_columns = [
        "invoice_number",
        "part_number.part_number",
        "part_name",
        "unit_of_measure.uom",
        "vendor_name.vendor_name",
        "invoice_date",
        "invoice_quantity",
        "total_invoice_amount",
        "total_duty_amount",
        "total_fright_amount",
        "total_clearance_amount",
        "total_amount",
        "price_per_part",
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.
        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'invoice_number':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value


class OverseasinvoiceDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    template_name = "inventory/overseasinvoice_details.html"
    model = Overseasinvoice
    permission_required = 'inventory.full_details_overseasinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class OverseasinvoiceCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Create Overseasinvoice."""

    model = Overseasinvoice
    fields = [
        "part_number",
        "part_name",
        "unit_of_measure",
        "vendor_name",
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
        "stage",
        "remarks",
        "overseas_invoice",
        "customs_invoice",
        "fright_invoice",
        "clearance_invoice",
    ]
    template_name = "inventory/overseasinvoice_create.html"
    success_message = "Invoice For Part: %(part_name)s was created successfully"
    permission_required = 'inventory.add_overseasinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """After Creating Invoice redirect to Invoice list."""
        return reverse('overseasinvoice-list')


class OverseasinvoiceUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """Update Parts."""

    model = Overseasinvoice
    fields = [
        "part_number",
        "part_name",
        "unit_of_measure",
        "vendor_name",
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
        "stage",
        "remarks",
        "overseas_invoice",
        "customs_invoice",
        "fright_invoice",
        "clearance_invoice",
    ]
    template_name = "inventory/overseasinvoice_update.html"
    success_message = "Invoice For Part: %(part_name)s was Update successfully"
    permission_required = 'inventory.change_overseasinvoice'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """After Creating Invoice redirect to Invoice list."""
        return reverse('overseasinvoice-list')


class OutwardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Outward
    template_name = "inventory/outward_list.html"
    permission_required = 'inventory.view_outward'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class OutwardListJson(LoginRequiredMixin, BaseDatatableView):
    """."""

    model = Outward

    columns = [
        'outward_receipt_number',
        'part_number.part_number',
        'part_name',
        'unit_of_measure.uom',
        'quantity',
        'from_warehouse_name.warehouse_name',
        'to_warehouse_name.warehouse_name',
        'authorised_by',
        'updated',
    ]

    order_columns = [
        'outward_receipt_number',
        'part_number.part_number',
        'part_name',
        'unit_of_measure.uom',
        'quantity',
        'from_warehouse_name.warehouse_name',
        'to_warehouse_name.warehouse_name',
        'authorised_by',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.
        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'outward_receipt_number':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)
        return value

    # DO NOT USE the following commented code block; it hinders the search feature on Outwards page
    # def filter_queryset(self, qs):
    #     """Excluding outward record with part_type ASSETAUTOOUTWARD."""
    #     qs = qs.exclude(part_type__type_name='ASSETAUTOOUTWARD')
    #     return qs


class OutwardDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    template_name = "inventory/outward_detail.html"
    model = Outward
    permission_required = 'inventory.full_details_outward'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class OutwardReceiptView(LoginRequiredMixin, DetailView):
    """."""

    template_name = 'inventory/outward_receipt.html'
    model = Outward


class OutwardCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Create Outward."""

    model = Outward
    form_class = OutwardCreateForm
    template_name = "inventory/outward_create.html"
    success_message = "Outward: %(outward_receipt_number)s was created successfully"
    permission_required = 'inventory.add_outward'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """After Creating Invoice redirect to Invoice list."""
        return reverse('outward-list')


class OutwardUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    """Update Parts."""

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
    template_name = "inventory/outward_update.html"
    permission_required = 'inventory.change_outward'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """After Creating Invoice redirect to Invoice list."""
        return reverse('outward-list')


class UnitOfMeasureListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """."""

    model = UnitOfMeasure
    template_name = "inventory/uom_list.html"
    permission_required = 'inventory.view_unitofmeasure'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class UnitOfMeasureCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    """Create Commodity."""

    model = UnitOfMeasure
    fields = ['uom', 'description']
    template_name = "inventory/uom_create.html"
    permission_required = 'inventory.add_unitofmeasure'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('uom-list')


class BillOfMaterialListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    """."""

    model = BillOfMaterial
    template_name = "inventory/bom_list.html"
    permission_required = 'inventory.view_billofmaterial'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class BillOfMaterialListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the BillOfMaterial list."""

    model = BillOfMaterial
    columns = [
        'bom_name',
        'bom_description',
        'remarks',
        'updated',
    ]

    order_columns = [
        'bom_name',
        'bom_description',
        'remarks',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'bom_name':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)

        if value and column == 'parts':
            y = ast.literal_eval(unescape(value))
            z = "<hr>".join(["<br>".join(['{}: {}'.format(k, v) for k, v in i.items()]) for i in y])
            return z

        return value


class BillOfMaterialCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """."""

    model = BillOfMaterial
    fields = [
        'bom_name',
        'bom_description',
        'parts',
        'bom_file',
        'remarks',
    ]
    success_message = "BillOfMaterial: %(bom_name)s was created successfully"
    template_name = "inventory/bom_create.html"
    permission_required = 'inventory.add_billofmaterial'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('bom-list')

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Created from web form.")
            return_value = super().form_valid(form)
        return return_value


class BillOfMaterialCopyUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = BillOfMaterial
    fields = [
        'bom_name',
        'bom_description',
        'parts',
        'bom_file',
        'remarks',
    ]
    template_name = "inventory/bom_copy.html"
    permission_required = 'inventory.change_billofmaterial'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('bom-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['bom_file'] = None
        initial['bom_name'] = f"Copy of {self.object.bom_name}"
        return initial

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super().form_valid(form)
        return return_value


class BillOfMaterialUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    """."""

    model = BillOfMaterial
    fields = [
        'bom_name',
        'bom_description',
        'parts',
        'bom_file',
        'remarks',
    ]
    template_name = "inventory/bom_update.html"
    permission_required = 'inventory.change_billofmaterial'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('bom-list')

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super().form_valid(form)
        return return_value


class BillOfMaterialDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    """."""

    model = BillOfMaterial
    template_name = "inventory/bom_detail.html"
    permission_required = 'inventory.full_details_billofmaterial'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """."""

    model = Product
    template_name = "inventory/product_list.html"
    permission_required = 'inventory.view_product'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class ProductCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """."""

    model = Product
    fields = ['product_name', 'description']
    template_name = "inventory/product_create.html"
    success_message = "Product: %(product_name)s was created successfully"
    permission_required = 'inventory.add_product'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('product-list')

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super(ProductCreateView, self).form_valid(form)
        return return_value


class AssetCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    """Assets Create View."""

    model = Asset
    form_class = AssetCreateForm
    template_name = "inventory/asset_create.html"
    # success_message = "Asset created successfully"
    permission_required = 'inventory.add_asset'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def get_success_url(self):
        """."""
        return reverse('asset-update', kwargs={'slug': self.object.slug})


class AssetListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Assets List View."""

    model = Asset
    template_name = "inventory/asset_list.html"
    permission_required = 'inventory.view_asset'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class AssetListJson(LoginRequiredMixin, BaseDatatableView):
    """For Paginated View of the BillOfMaterial list."""

    model = Asset
    columns = [
        'asset_id',
        'product_name.product_name',
        'bom_name.bom_name',
        'warehouse_name.warehouse_name',
        'asset_state',
        'total_price',
        'updated',
    ]

    order_columns = [
        'asset_id',
        'product_name.product_name',
        'bom_name.bom_name',
        'warehouse_name.warehouse_name',
        'asset_state',
        'total_price',
        'updated',
    ]
    max_display_length = settings.MAX_DATATABLE_DISPLAY_LENGTH

    def render_column(self, row, column):
        """Render a column on a row. column can be given in a module notation.

        eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if value is None:
            value = self.none_string

        if isinstance(value, datetime):
            value = localtime(value).strftime('%d-%b-%Y %H:%M')

        if self.escape_values:
            value = escape(value)

        if value and hasattr(obj, 'get_absolute_url') and column == 'asset_id':
            return '<a href="%s">%s</a>' % (obj.get_absolute_url(), value)

        return value


class AssetDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """."""

    model = Asset
    template_name = "inventory/asset_detail.html"
    permission_required = 'inventory.full_details_asset'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()


class AssetUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    """Assets Update View."""

    model = Asset
    fields = [
        "product_name",
        "bom_name",
        "parts",
        "warehouse_name",
        "mfg_date",
        # "quantity",
        "asset_state",
        "remarks",
    ]
    template_name = "inventory/asset_update.html"
    # success_message = "Asset created successfully"
    permission_required = 'inventory.change_asset'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def form_valid(self, form):
        """Added the user details to the submitted data."""
        with create_revision():
            form_data = form.save(commit=False)
            bom_name = form.cleaned_data['bom_name']
            warehouse_name = form.cleaned_data['warehouse_name']
            initial_parts = form.initial.get('parts')
            updated_parts = form.cleaned_data.get('parts')
            # Using sets to find newly added parts by using set diff

            # Forming sets only with PartNumbers instead of PartsDict
            # to make comparisons easy
            initial_partNumbers = {
                part['PartNumber'] for part in initial_parts
            }
            updated_partNumbers = {
                part['PartNumber'] for part in updated_parts
            }
            newly_added_partNumbers = updated_partNumbers - initial_partNumbers
            removed_partNumbers = initial_partNumbers - updated_partNumbers

            # Reforming part dicts to access part attributes easily.
            newly_added_parts = [
                part for part in updated_parts
                if part['PartNumber'] in newly_added_partNumbers
            ]
            form_data.total_price = cal_total_price(bom_name)
            # Create outwards for parts used in asset creation.
            for part in newly_added_parts:
                part_obj = Parts.objects.get(part_number=part['PartNumber'])
                authorised_by = "asset_auto_creation"
                verified_by = "asset_auto_creation"
                mode_of_transport = "asset_auto_creation"
                remarks = "This outward was created due to asset creation."

                Outward.objects.create(
                    part_type=part_obj.part_type,
                    part_number=part_obj,
                    part_name=part_obj.part_name,
                    quantity=part['Qty'],
                    from_warehouse_name=warehouse_name,
                    to_warehouse_name=warehouse_name,
                    authorised_by=authorised_by,
                    verified_by=verified_by,
                    mode_of_transport=mode_of_transport,
                    unit_of_measure=part_obj.unit_of_measure,
                    remarks=remarks,
                )

            form_data.save()
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super().form_valid(form_data)

        return return_value

    def get_success_url(self):
        """."""
        return reverse('asset-list')


@login_required
def assets_ready(request):
    """Count of Assets which are ready for Installation."""
    # If this is a POST request then process the Form data
    asset_for_product = None
    asset_in_warehouse = None
    warehouse = None
    product = None
    if request.method == 'POST':
        # Create a form instance and populate it
        # with data from the request(binding):
        form = AssetForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            warehouse = form.cleaned_data['warehouse']
            product = form.cleaned_data['product']
            # print(warehouse)
            if product:
                prod_obj = Product.objects.get(product_name=product)
                asset_for_product = list(
                    Asset.objects.filter(product_name=prod_obj)
                        .exclude(asset_state='On Lease')
                        .values(
                        'product_name',
                        'warehouse_name__warehouse_name',
                        'asset_state'
                    ).order_by('product_name')
                        .annotate(count=Count('product_name'))
                )
            if warehouse:
                ware_obj = Warehouse.objects.get(warehouse_name=warehouse)
                asset_in_warehouse = list(
                    Asset.objects.filter(warehouse_name=ware_obj)
                        .exclude(asset_state='On Lease')
                        .values(
                        'product_name__product_name',
                        'warehouse_name',
                        'asset_state'
                    ).order_by('product_name')
                        .annotate(count=Count('product_name'))
                )
                # print(asset_in_warehouse)
    else:
        form = AssetForm()
    context = {
        'form': form,
        'warehouse': warehouse,
        'product': product,
        'asset_for_product': asset_for_product,
        'asset_in_warehouse': asset_in_warehouse
    }
    # print(context)

    return render(request, 'inventory/assets_ready.html', context)


def get_bom_by_name(request):
    """Get Boms for a matching bom name."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    if request.method == "GET" and request.is_ajax():
        bom_name = request.GET.get("searchTerm")
        try:
            boms = BillOfMaterial.objects.filter(
                bom_name__icontains=bom_name
            )
            data = [
                {"id": bom.bom_name,
                 "text": bom.bom_name, }
                for bom in boms
            ]
        except Exception:
            return JsonResponse({"success": False}, status=400)
        return JsonResponse(data, safe=False, status=200)
    return JsonResponse({"success": False}, status=405)


def get_bom_detail(request):
    """Get Bom detail for a given bom."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    if request.method == "GET" and request.is_ajax():
        bom1 = request.GET.get("bom1")
        bom2 = request.GET.get("bom2")
        try:
            bom1 = BillOfMaterial.objects.get(
                bom_name=bom1
            )
            bom2 = BillOfMaterial.objects.get(
                bom_name=bom2
            )
            data = [
                ("Name", bom1.bom_name, bom2.bom_name,),
                ("Description", bom1.bom_description, bom2.bom_description,),
                ("Parts", bom1.parts, bom2.parts,),
                # ("File", bom1.bom_file.url, bom2.bom_file.url,),
                ("Remarks", bom1.remarks, bom2.remarks,),
            ]
        except Exception as e:
            raise e
            return JsonResponse({"success": False}, status=400)
        return JsonResponse(data, safe=False, status=200)
    return JsonResponse({"success": False}, status=405)


@login_required
def get_defected_parts(request):
    """Get the Defected Parts vendor wise. With range filter."""
    vendor_name = None
    defect_parts = None
    if request.method == 'POST':
        form = DefectPartsForm(request.POST)
        if form.is_valid():
            vendor_name = form.cleaned_data['vendor_name']
            st_date = form.cleaned_data['st_date']
            ed_date = form.cleaned_data['ed_date']
            ven_obj = Vendor.objects.get(vendor_name=vendor_name)
            if not st_date:
                defect_parts = list(
                    Inward.objects.filter(vendor_name=ven_obj)
                        .values(
                        "part_number__part_number",
                        "part_number__part_name",
                        "defected_quantity"
                    )
                )
            else:
                defect_parts = list(
                    Inward.objects.filter(vendor_name=ven_obj)
                        .filter(
                        timestamp__gte=st_date,
                        timestamp__lte=ed_date,
                    ).values(
                        "part_number__part_number",
                        "part_number__part_name",
                        "defected_quantity"
                    )
                )
    else:
        form = DefectPartsForm()
    context = {
        'form': form,
        'vendor_name': vendor_name,
        'defect_parts': defect_parts,
    }
    return render(request, 'inventory/defected_parts.html', context)


@login_required
def assets_by_bom(request):
    """Count of Assets which are ready for Installation."""
    # If this is a POST request then process the Form data
    asset_by_bom = None
    asset_by_range = None
    warehouse = None
    bom = None
    if request.method == 'POST':
        # Create a form instance and populate it
        # with data from the request(binding):
        form = AssetReportForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            bom = form.cleaned_data['bom']
            st_date = form.cleaned_data['st_date']
            ed_date = form.cleaned_data['ed_date']
            if bom:
                bom_obj = BillOfMaterial.objects.get(bom_name=bom)
                asset_by_bom = list(
                    Asset.objects.values(
                        "bom_name",
                        "product_name__product_name",
                    )
                        .filter(bom_name=bom_obj)
                        .order_by('bom_name')
                        .annotate(count=Count("bom_name"))
                )
            else:
                asset_by_range = list(
                    Asset.objects.filter(
                        timestamp__gte=st_date,
                        timestamp__lte=ed_date,
                    ).values(
                        "bom_name__bom_name",
                        "product_name__product_name",
                    )
                        .order_by('bom_name')
                        .annotate(count=Count("bom_name"))
                )
    else:
        form = AssetReportForm()
    context = {
        'form': form,
        'bom': bom,
        'asset_by_bom': asset_by_bom,
        'asset_by_range': asset_by_range
    }
    # print(context)

    return render(request, 'inventory/assets_by_bom.html', context)


@login_required
def commodity_wise_inward(request):
    """."""
    # If this is a POST request then process the Form data
    warehouse = None
    com = None
    commodity_wise_in = []
    avg_price = {}
    if request.method == 'POST':
        # Create a form instance and populate it
        # with data from the request(binding):
        form = CommodityWiseForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            com = form.cleaned_data['com']
            warehouse = form.cleaned_data['warehouse']
            st_date = form.cleaned_data['st_date']
            ed_date = form.cleaned_data['ed_date']
            commodity_wise_in = (
                Inward.objects.filter(
                    part_number__commodity_name__commodity_name=com,
                    to_warehouse_name__warehouse_name=warehouse
                ).filter(
                    timestamp__gte=st_date,
                    timestamp__lte=ed_date,
                ).values("part_number", "part_name", "received_quantity")
            )
            for i in commodity_wise_in:
                avg = (
                    AveragePrice.objects.filter(
                        part_number=i['part_number']
                    ).latest('average_price').average_price
                )
                i['avg_price'] = avg
    else:
        form = CommodityWiseForm()
    context = {
        'form': form,
        'com': com,
        'warehouse': warehouse,
        'commodity_wise_in': list(commodity_wise_in),
        'avg_price': avg_price
    }
    print(context)

    return render(request, 'inventory/commodity_wise_inward.html', context)


class AssetMultipleCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    """Assets Create View."""

    model = Asset
    fields = [
        "product_name",
        "bom_name",
        "warehouse_name",
        "mfg_date",
        "quantity",
        "asset_state",
        "remarks",
    ]
    template_name = "inventory/asset_create.html"
    # success_message = "Asset created successfully"
    permission_required = 'inventory.add_asset'
    permission_denied_message = "User not allowed to this view."

    def handle_no_permission(self):
        """."""
        messages.error(self.request, 'You don\'t have permission to View this')
        return super().handle_no_permission()

    def form_valid(self, form):
        """Added the user details to the submitted data."""
        with create_revision():
            # form_data = form.save(commit=False)
            bom_name = form.cleaned_data['bom_name']
            parts = get_bom_parts(bom_name)
            total_price = cal_total_price(bom_name)
            qty = form.cleaned_data['quantity']
            product_name = form.cleaned_data['product_name']
            warehouse_name = form.cleaned_data['warehouse_name']
            asset_state = form.cleaned_data['asset_state']
            mfg_date = form.cleaned_data['mfg_date']
            remarks = form.cleaned_data['remarks']
            # multipule_assets = []
            # Outwards for asset creation

            # Outward all parts in an asset
            # multiply it with assets `qty` to limit number
            # queries for creation of Outwards
            for part in parts:
                part_obj = Parts.objects.get(part_number=part['PartNumber'])
                authorised_by = "asset_auto_creation"
                verified_by = "asset_auto_creation"
                mode_of_transport = "asset_auto_creation"
                remarks = "This outward was created due to asset creation."
                parts_assets_qty = float(part['Qty']) * qty
                Outward.objects.create(
                    part_type=Type.objects.get(type_name="ASSETAUTOOUTWARD"),
                    part_number=part_obj,
                    part_name=part_obj.part_name,
                    quantity=parts_assets_qty,
                    from_warehouse_name=warehouse_name,
                    to_warehouse_name=warehouse_name,
                    authorised_by=authorised_by,
                    verified_by=verified_by,
                    mode_of_transport=mode_of_transport,
                    unit_of_measure=part_obj.unit_of_measure,
                    remarks=remarks,
                )

            for i in range(qty):
                single_asset = Asset(
                    product_name=product_name,
                    bom_name=bom_name,
                    parts=parts,
                    total_price=total_price,
                    warehouse_name=warehouse_name,
                    asset_state=asset_state,
                    remarks=remarks,
                    mfg_date=mfg_date,
                )
                single_asset.save()
                revisions.set_user(self.request.user)
                revisions.set_comment("Created from web form.")
                return_value = super().form_valid(single_asset)
        return return_value

    def get_success_url(self):
        """."""
        return reverse('asset-list')


@login_required
def parts_demand(request):
    """Critical Parts as per Demand."""
    critical_part = []
    quantity = None
    bom_name = None
    if request.method == 'POST':
        form = PartsDemandForm(request.POST)
        if form.is_valid():
            bom_name = form.cleaned_data['bom']
            quantity = int(form.cleaned_data['quantity'])
            warehouse = form.cleaned_data['warehouse']
            warehouse_obj = Warehouse.objects.get(warehouse_name=warehouse)
            stock = calculate_stock(warehouse_obj)
            parts = get_bom_parts(bom_name)
            print(stock)
            for part in parts:
                part_qty = float(part['Qty'])
                part_name = part['PartName']
                part_number = part['PartNumber']
                if stock.get(part_name):
                    av_stock = stock.get(part_name)['total_usable_stock']
                    # print(av_stock, quantity, part_qty, quantity * part_qty)
                else:
                    av_stock = 0
                critical = int(av_stock) - int(quantity * part_qty)
                if critical <= 0:
                    test = {
                        "critical_qty": critical,
                        "part_number": part_number,
                        "part_name": part_name
                    }
                    critical_part.append(test)
    else:
        form = PartsDemandForm()
    context = {
        'form': form,
        'critical_part': critical_part,
        'quantity': quantity,
        'bom': bom_name,
    }

    return render(request, 'inventory/parts_demand.html', context)


@login_required
def boms_compare(request):
    """Count of Assets which are ready for Installation."""
    # If this is a POST request then process the Form data

    bom_1 = None
    bom_2 = None
    if request.method == 'POST':
        # Create a form instance and populate it
        # with data from the request(binding):
        form = BomCompareForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            bom_1 = BillOfMaterial.objects.get(
                bom_name=form.cleaned_data['bom_1']
            )
            bom_2 = BillOfMaterial.objects.get(
                bom_name=form.cleaned_data['bom_2']
            )

    else:
        form = BomCompareForm()

    context = {
        "form": form,
        "bom_1": bom_1,
        "bom_2": bom_2,
    }

    return render(request, 'inventory/bom_compare.html', context)


def checkIfProcessRunning(processName):
    """
    Check if there is any running process that contains the given name.

    processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def cron_health(request):
    """Checking the Cron Health."""
    if checkIfProcessRunning('crond'):
        print('Yes a crond process was running')
        return HttpResponse(status=200)
    else:
        print('crond process is Not running')

    return HttpResponse(status=500)
