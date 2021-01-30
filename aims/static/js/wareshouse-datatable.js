$(document).ready(function() {
    let dt_table = $('.datatable').DataTable({
        dom: "<'row'<'col-sm-3'l><'col-sm-6 text-center'B><'col-sm-3'f>>" +
          "<'row'<'col-sm-12'tr>>" +
          "<'row'<'col-sm-5'i><'col-sm-7'p>>",
        buttons: [
          'copy', 'csv', 'excel',
        ],
        fixedHeader: {
            header: true,
            footer: true
        },
        language: dt_language,  // global variable defined in html
        order: ORDER_BY,
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {orderable: true,
             searchable: true,
             className: "center",
             targets: [0, 1]
            },
            {
                name: 'name',
                targets: [0]
            },
            {
                name: 'description',
                targets: [1]
            }
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: TESTMODEL_LIST_JSON_URL
    });
});
