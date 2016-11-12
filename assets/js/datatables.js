$.fn.dataTable.defaults.column.asSorting = ['desc', 'asc'];

var playersTable = $('#players-table').dataTable({
    ajax: {
        url: '/assets/json/data.json',
        dataSrc: ""
    },
    paging: false,
    info: false,
    destroy: true,
    order: [
        [2, "desc"]
    ],
    "columnDefs": [{
        "visible": false,
        "targets": [0]
    }],
    columns: [{
        "data": "ID"
    }, {
        "data": "Name"
    }, {
        "data": "Salary"
    }, {
        "data": "MIN"
    }, {
        "data": "AvgPointsPerGame"
    }, {
        "data": "PPD"
    }, {
        "data": "Ceiling"
    }, {
        "data": "ceilingPPD"
    }, {
        "data": "Floor"
    }, {
        "data": "floorPPD"
    }, {
        "data": "lastFiveGameMin"
    }, {
        "data": "lastFivePoints"
    }, {
        "data": "lastFivePPD"
    }],
    language: {
        emptyTable: "Loading...",
        search: "Filter:"
    }
});
