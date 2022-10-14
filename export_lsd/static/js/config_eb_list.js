var csrftoken = getCookie('csrftoken');

$(function() {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id" },
            { "data": "forma_pago" },
            { "data": "ccn_sueldo" },
            { "data": "ccn_no_rem" },
            { "data": "ccn_sijp" },
            { "data": "ccn_inssjp" },
            { "data": "ccn_os" },
            { "data": "ccn_no_rem" },
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
            },
            {
                targets: [2],
                class: 'text-center',
            },
            {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function(data, type, row) {
                var buttons = '<a href="/export-lsd/config-db/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                buttons += '<a href="/export-lsd/config-db/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                return buttons;
            }
            },
        ],
        initComplete: function(settings, json) {

        }
    });
});