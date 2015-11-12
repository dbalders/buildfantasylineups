//NFL Datatables

function nflDatatables() {
    $.fn.dataTable.defaults.column.asSorting = ['desc', 'asc'];

    var teTable = $('#te-table').DataTable({
        paging: false,
        info: false,
        order: [
            [5, "desc"]
        ],
        aaSorting: [
            [4, 'asc']
        ],
        columnDefs: [{
            type: "num",
            targets: 6
        }, {
            orderSequence: ["asc"],
            targets: 6
        }],
        language: {
            emptyTable: "Loading...",
            search: "Filter:"
        }

    });

    var rbTable = $('#rb-table').DataTable({
        paging: false,
        info: false,
        order: [
            [5, "desc"]
        ],
        aaSorting: [
            [4, 'asc']
        ],
        columnDefs: [{
            type: "num",
            targets: 6
        }, {
            orderSequence: ["asc"],
            targets: 6
        }],
        language: {
            emptyTable: "Loading...",
            search: "Filter:"
        }

    });

    var wrTable = $('#wr-table').DataTable({
        paging: false,
        info: false,
        order: [
            [5, "desc"]
        ],
        aaSorting: [
            [4, 'asc']
        ],
        columnDefs: [{
            type: "num",
            targets: 6
        }, {
            orderSequence: ["asc"],
            targets: 6
        }],
        language: {
            emptyTable: "Loading...",
            search: "Filter:"
        }

    });

    var defTable = $('#def-table').DataTable({
        paging: false,
        info: false,
        order: [
            [5, "desc"]
        ],
        aaSorting: [
            [4, 'asc']
        ],
        columnDefs: [{
            type: "num",
            targets: 6
        }, {
            orderSequence: ["asc"],
            targets: 6
        }],
        language: {
            emptyTable: "Loading...",
            search: "Filter:"
        }

    });

    qbTable = $('#qb-table').DataTable({
        paging: false,
        info: false,
        order: [
            [5, "desc"]
        ],
        aaSorting: [
            [4, 'asc']
        ],
        columnDefs: [{
            type: "num",
            targets: 6
        }, {
            orderSequence: ["asc"],
            targets: 6
        }],
        language: {
            emptyTable: "Loading...",
            search: "Filter:"
        }
    });
}
//End Datatables
