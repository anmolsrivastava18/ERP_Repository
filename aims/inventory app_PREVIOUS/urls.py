"""Inventory App Related URLS."""
from django.urls import path

from ..inventory.views import (
    WarehouseListView,
    WarehouseListJson,
    WarehouseCreateView,
    WarehouseUpdateView,
    WarehouseDetailView,
    AvailabilityListView,
    AvailabilityCreateView,
    TypeListView,
    TypeCreateView,
    CommodityListView,
    CommodityCreateView,
    PartsListView,
    PartsListJson,
    PartsDetailView,
    PartsCreateView,
    PartsUpdateView,
    DomesticinvoiceListView,
    DomesticinvoiceCreateView,
    DomesticinvoiceListJson,
    DomesticinvoiceUpdateView,
    DomesticinvoiceDetailView,
    InwardListView,
    InwardListJson,
    InwardCreateView,
    InwardDetailView,
    VendorListView,
    VendorListJson,
    VendorCreateView,
    VendorUpdateView,
    VendorDetailView,
    OverseasinvoiceListView,
    OverseasinvoiceListJson,
    OverseasinvoiceDetailView,
    OverseasinvoiceCreateView,
    OverseasinvoiceUpdateView,
    OutwardListView,
    OutwardListJson,
    OutwardDetailView,
    OutwardCreateView,
    OutwardUpdateView,
    OutwardReceiptView,
    get_part_name,
    get_stock,
    get_stock_batchnumber,
    get_avg_price,
    get_saftey_stock,
    get_part_number_name,
    get_part_name_number,
    UnitOfMeasureListView,
    UnitOfMeasureCreateView,
    BillOfMaterialListView,
    BillOfMaterialListJson,
    BillOfMaterialCreateView,
    BillOfMaterialUpdateView,
    BillOfMaterialCopyUpdateView,
    BillOfMaterialDetailView,
    ProductListView,
    ProductCreateView,
    AssetCreateView,
    AssetListView,
    AssetListJson,
    AssetDetailView,
    AssetUpdateView,
    assets_ready,
    boms_compare,
    get_bom_by_name,
    get_bom_detail,
    get_defected_parts,
    parts_demand,
    assets_by_bom,
    commodity_wise_inward,
    AssetMultipleCreateView,
    cron_health,
)


urlpatterns = [
    # WareHouse URLS
    path('warehouses/', WarehouseListView.as_view(), name='warehouse-list'),
    path(
        'warehouselistjson/',
        WarehouseListJson.as_view(),
        name='warehouse-list-data'
    ),
    path(
        'warehouses/add/',
        WarehouseCreateView.as_view(),
        name='warehouse-add'
    ),
    path(
        'warehouses/update/<pk>/',
        WarehouseUpdateView.as_view(),
        name='warehouse-update'
    ),
    path(
        'warehouses/detail/<slug:slug>/',
        WarehouseDetailView.as_view(),
        name='warehouse-detail'
    ),

    # Parts URLS
    path('parts/list/', PartsListView.as_view(), name='parts-list'),
    path(
        'partslistjson/',
        PartsListJson.as_view(),
        name='parts-list-data'
    ),
    path(
        'parts/detail/<slug:slug>/',
        PartsDetailView.as_view(),
        name='parts-detail'
    ),
    path(
        'parts/update/<pk>/',
        PartsUpdateView.as_view(),
        name='parts-update'
    ),
    path(
        'parts/add/',
        PartsCreateView.as_view(),
        name='parts-add'
    ),
    path('get_part_name', get_part_name, name='get_part_name'),
    path('get_part_number_name', get_part_number_name,
         name='get_part_number_name'),

    path('get_part_name_number', get_part_name_number,
         name='get_part_name_number'),

    path('get_bom_by_name', get_bom_by_name,
         name='get_bom_by_name'),
    path('get_bom_detail', get_bom_detail,
         name='get_bom_detail'),


    # Availability URLS
    path(
        'availabilitylist/',
        AvailabilityListView.as_view(),
        name='availability-list'
    ),
    path(
        'availabilitylist/add/',
        AvailabilityCreateView.as_view(),
        name='availability-add'
    ),

    # Type URLS
    path('typelist/', TypeListView.as_view(), name='type-list'),
    path('typelist/add/', TypeCreateView.as_view(), name='type-add'),

    # Commodity URLS
    path('commoditylist/', CommodityListView.as_view(), name='commodity-list'),
    path(
        'commoditylist/add/',
        CommodityCreateView.as_view(),
        name='commodity-add'
    ),
    # Domestic Invoice URLs
    path('domesticinvoices/', DomesticinvoiceListView.as_view(), name='domesticinvoice-list'),
    path(
        'domesticinvoices/add/',
        DomesticinvoiceCreateView.as_view(),
        name='domesticinvoice-add'
    ),
    path(
        'domesticinvoice-list-json/',
        DomesticinvoiceListJson.as_view(),
        name='domesticinvoice-list-data'
    ),
    path(
        'domesticinvoices/<pk>/edit/',
        DomesticinvoiceUpdateView.as_view(),
        name='domesticinvoice-update'
    ),
    path(
        'domesticinvoices/detail/<slug:slug>/',
        DomesticinvoiceDetailView.as_view(),
        name='domesticinvoice-detail'
    ),
    # Inward Invoice URLs
    path('inwards/', InwardListView.as_view(), name='inward-list'),
    path(
        'inwards/add/',
        InwardCreateView.as_view(),
        name='inward-add'
    ),
    path(
        'inward-list-json/',
        InwardListJson.as_view(),
        name='inward-list-data'
    ),
    path(
        'inwards/detail/<slug:slug>/',
        InwardDetailView.as_view(),
        name='inward-detail'
    ),


    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path(
        'vendorlistjson/',
        VendorListJson.as_view(),
        name='vendor-list-data'
    ),

    path(
        'vendors/add/',
        VendorCreateView.as_view(),
        name='vendor-add'
    ),

    path(
        'vendors/update/<pk>/',
        VendorUpdateView.as_view(),
        name='vendor-update'
    ),
    path(
        'vendors/detail/<slug:slug>/',
        VendorDetailView.as_view(),
        name='vendor-detail'
    ),

    # Overseasinvoice URLS
    path(
        'overseasinvoice/list/',
        OverseasinvoiceListView.as_view(),
        name='overseasinvoice-list'
    ),
    path(
        'overseasinvoicejson/',
        OverseasinvoiceListJson.as_view(),
        name='overseasinvoice-list-data'
    ),
    path(
        'overseasinvoice/detail/<slug:slug>/',
        OverseasinvoiceDetailView.as_view(),
        name='overseasinvoice-detail'
    ),
    path(
        'overseasinvoice/add/',
        OverseasinvoiceCreateView.as_view(),
        name='overseasinvoice-add'
    ),
    path(
        'overseasinvoice/update/<pk>/',
        OverseasinvoiceUpdateView.as_view(),
        name='overseasinvoice-update'
    ),

    # Outward URLS
    path(
        'outward/list/',
        OutwardListView.as_view(),
        name='outward-list'
    ),
    path(
        'outwardListJson/',
        OutwardListJson.as_view(),
        name='outward-list-data'
    ),
    path(
        'outward/detail/<slug:slug>/',
        OutwardDetailView.as_view(),
        name='outward-detail'
    ),
    path(
        'outward/add/',
        OutwardCreateView.as_view(),
        name='outward-add'
    ),
    path(
        'outward/update/<pk>/',
        OutwardUpdateView.as_view(),
        name='outward-update'
    ),
    path(
        'outward/receipt/<slug:slug>/',
        OutwardReceiptView.as_view(),
        name='outward-receipt'
    ),

    # UnitOfMeasure URLs
    path('uom/list/', UnitOfMeasureListView.as_view(), name='uom-list'),
    path('uom/add/', UnitOfMeasureCreateView.as_view(), name='uom-add'),

    # Stock
    path('get_stock', get_stock, name='get_stock'),
    path('get_saftey_stock', get_saftey_stock, name='get_saftey_stock'),
    path('get_stock_batchnumber',
         get_stock_batchnumber,
         name='get_stock_batchnumber'),
    path('get_avg_price', get_avg_price, name='get_avg_price'),
    path('parts_demand', parts_demand,
         name='parts_demand'),


    path('boms/', BillOfMaterialListView.as_view(), name='bom-list'),
    path(
        'bomlistjson/',
        BillOfMaterialListJson.as_view(),
        name='bom-list-data'
    ),

    path(
        'boms/add/',
        BillOfMaterialCreateView.as_view(),
        name='bom-add'
    ),

    path(
        'boms/update/<pk>/',
        BillOfMaterialUpdateView.as_view(),
        name='bom-update'
    ),
    path(
        'boms/copy-create/<pk>/',
        BillOfMaterialCopyUpdateView.as_view(),
        name='bom-copy'
    ),
    path(
        'boms/detail/<slug:slug>/',
        BillOfMaterialDetailView.as_view(),
        name='bom-detail'
    ),
    path(
        'boms/compare/',
        boms_compare,
        name='boms-compare'
    ),

    # Products URLS
    path('productlist/', ProductListView.as_view(), name='product-list'),
    path('productlist/add/', ProductCreateView.as_view(), name='product-add'),

    # Assets URLS

    path('assets/', AssetListView.as_view(), name='asset-list'),
    path(
        'assetslistjson/',
        AssetListJson.as_view(),
        name='asset-list-data'
    ),

    path(
        'assets/add/',
        AssetCreateView.as_view(),
        name='asset-add'
    ),
    path(
        'assets/detail/<slug:slug>/',
        AssetDetailView.as_view(),
        name='asset-detail'
    ),
    path(
        'assets/update/<slug:slug>/',
        AssetUpdateView.as_view(),
        name='asset-update'
    ),
    path(
        'assets/available/',
        assets_ready,
        name='asset-available'
    ),
    path(
        'assets/asset-by-bom/',
        assets_by_bom,
        name='asset-by-bom'
    ),
    path(
        'parts/defected/',
        get_defected_parts,
        name='defected-parts'
    ),
    path(
        'parts/commodity-wise-inward/',
        commodity_wise_inward,
        name='commodity-wise-inward'
    ),
    path(
        'assets/multiadd/',
        AssetMultipleCreateView.as_view(),
        name='asset-multi-add'
    ),
    path(
        'cron_health',
        cron_health,
        name='cron_health'
    ),
]
