//NFL Datatables
var teTable;
var rbTable;
var wrTable;
var qbTable;
var defTable;


function nflDatatables(callback) {
    $.fn.dataTable.defaults.column.asSorting = ['desc', 'asc'];

    teTable = $('#te-table').DataTable({
        paging: false,
        info: false,
        destroy: true,
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

    rbTable = $('#rb-table').DataTable({
        paging: false,
        info: false,
        destroy: true,
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

    wrTable = $('#wr-table').DataTable({
        paging: false,
        info: false,
        destroy: true,
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

    defTable = $('#def-table').DataTable({
        paging: false,
        info: false,
        destroy: true,
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
        destroy: true,
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

function clearTables() {
    qbTable.clear().draw();
    wrTable.clear().draw();
    rbTable.clear().draw();
    teTable.clear().draw();
    defTable.clear().draw();
}
//End Datatables
