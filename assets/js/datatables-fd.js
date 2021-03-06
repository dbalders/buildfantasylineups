$.fn.dataTable.defaults.column.asSorting = ['desc', 'asc'];

var pg1 = 0;
var pg2 = 0;
var sg1 = 0;
var sg2 = 0;
var sf1 = 0;
var sf2 = 0;
var pf1 = 0;
var pf2 = 0;
var c1 = 0;
var origPGRow = [];
var origSGRow = [];
var origSFRow = [];
var origPFRow = [];
var origCRow = [];

var playersTable = $('#players-table').dataTable({
    ajax: {
        url: '/assets/json/fdFinalData.json',
        dataSrc: ""
    },
    dom: 'Bflrtip',
    select: true,
    paging: true,
    info: false,
    destroy: true,
    scrollY: 600,
    deferRender: false,
    scroller: true,
    responsive: true,
    order: [
        [3, "desc"]
    ],
    "columnDefs": [{
        "visible": false,
        "targets": [0]
    }],
    columns: [{
        "data": "ID"
    }, {
        "data": "Position"
    }, {
        "data": "Name"
    }, {
        "data": "Salary"
    }, {
        "data": "oppTeamDvPRank"
    }, {
        "data": "teamPace"
    }, {
        "data": "oppPace"
    }, {
        "data": "grindersProj"
    }, {
        "data": "grindersPPD"
    }, {
        "data": "AvgPointsPerGame"
    }, {
        "data": "PPD"
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
    },
    buttons: [{
        text: 'All',
        action: function(e, dt, node, config) {
            playersTable.api().column(1).search('').draw();
        }
    }, {
        text: 'PG',
        action: function(e, dt, node, config) {
            playersTable.api().column(1).search('PG').draw();
        }
    }, {
        text: 'SG',
        action: function(e, dt, node, config) {
            playersTable.api().column(1).search('SG').draw();
        }
    }, {
        text: 'SF',
        action: function(e, dt, node, config) {
            playersTable.api().column(1).search('SF').draw();
        }
    }, {
        text: 'PF',
        action: function(e, dt, node, config) {
            playersTable.api().column(1).search('PF').draw();
        }
    }, {
        text: 'C',
        action: function(e, dt, node, config) {
            playersTable.api().column(1).search('C').draw();
        }
    }, {
        text: 'Add Player',
        action: function(e, dt, node, config) {
            addPlayersToTeam();
        }
    }],
    rowCallback: function(row, data, index) {
        colorTableCells(row, data, index);
    }
});

var teamTable = $('#team-table').dataTable({
    ajax: {
        url: "/assets/json/blank.json",
        dataSrc: ""
    },
    dom: 'Blrtip',
    paging: false,
    info: false,
    destroy: true,
    select: true,
    ordering: false,
    responsive: true,
    order: [
        [3, "desc"]
    ],
    "columnDefs": [{
        "visible": false,
        "targets": [0]
    }],
    columns: [{
        "data": "ID"
    }, {
        "data": "Position"
    }, {
        "data": "Name"
    }, {
        "data": "Salary"
    }, {
        "data": "oppTeamDvPRank"
    }, {
        "data": "teamPace"
    }, {
        "data": "oppPace"
    }, {
        "data": "grindersProj"
    }, {
        "data": "grindersPPD"
    }, {
        "data": "AvgPointsPerGame"
    }, {
        "data": "PPD"
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
    },
    drawCallback: calculateTeamTotals,
    buttons: [{
        text: 'Remove Player',
        action: function(e, dt, node, config) {
            removePlayersFromTeam();
        }
    }, {
        text: 'Clear',
        action: function(e, dt, node, config) {
            var table = $('#team-table').DataTable();
            table.ajax.url('/assets/json/blank.json').load();
            tableCleared();
        }
    }, {
        text: 'Best Roster Based on Season AVG',
        action: function(e, dt, node, config) {
            var table = $('#team-table').DataTable();
            table.ajax.url('/assets/json/optimalAVG.json').load();
            tableFilled();
        }
    }, {
        text: 'Best Roster Based on Last 5 Games',
        action: function(e, dt, node, config) {
            var table = $('#team-table').DataTable();
            table.ajax.url('/assets/json/optimalLastFive.json').load();
            tableFilled();
        }
    }, {
        text: 'Best Roster Based on Rotogrinders Projections',
        action: function(e, dt, node, config) {
            var table = $('#team-table').DataTable();
            table.ajax.url('/assets/json/optimalRotogrinders.json').load();
            tableFilled();
        }
    }],
    initComplete: function(settings, json) {
        origPGRow = $('#team-table').DataTable().row(0).data();
        origSGRow = $('#team-table').DataTable().row(2).data();
        origSFRow = $('#team-table').DataTable().row(4).data();
        origPFRow = $('#team-table').DataTable().row(6).data();
        origCRow = $('#team-table').DataTable().row(8).data();
    },
    rowCallback: function(row, data, index) {
        colorTableCells(row, data, index);
    }
});

function addPlayersToTeam() {
    var playerData = playersTable.DataTable().row('.selected', 1).data();
    var playerPosition = playerData.Position;
    var addTeamTable = $('#team-table').DataTable();

    switch (playerPosition) {
        case 'PG':
            if (pg1 === 0) {
                addTeamTable.row(0).data(playerData).draw();
                pg1 = 1;
            } else if (pg2 === 0) {
                addTeamTable.row(1).data(playerData).draw();
                pg2 = 1;
            } else {

            }
            break;

        case 'SG':
            if (sg1 === 0) {
                addTeamTable.row(2).data(playerData).draw();
                sg1 = 1;
            } else if (sg2 === 0) {
                addTeamTable.row(3).data(playerData).draw();
                sg2 = 1;
            } else {

            }
            break;

        case 'SF':
            if (sf1 === 0) {
                addTeamTable.row(4).data(playerData).draw();
                sf1 = 1;
            } else if (sf2 === 0) {
                addTeamTable.row(5).data(playerData).draw();
                sf2 = 1;
            } else {

            }
            break;

        case 'PF':
            if (pf1 === 0) {
                addTeamTable.row(6).data(playerData).draw();
                pf1 = 1;
            } else if (pf2 === 0) {
                addTeamTable.row(7).data(playerData).draw();
                pf2 = 1;
            } else {

            }
            break;

        case 'C':
            if (c1 === 0) {
                addTeamTable.row(8).data(playerData).draw();
                c1 = 1;
            } else {

            }
            break;
    }
    $('#players-table').DataTable().search("").draw()
    calculateTeamTotals();
}

function removePlayersFromTeam() {
    var playerData = teamTable.DataTable().row('.selected', 1).data();
    var playerPosition = playerData.Position;
    var addTeamTable = $('#team-table').DataTable();
    var rowIndex = teamTable.DataTable().row('.selected', 1).index();

    switch (playerPosition) {
        case 'PG':
            teamTable.DataTable().row('.selected', 1).data(origPGRow);
            break;

        case 'SG':
            teamTable.DataTable().row('.selected', 1).data(origSGRow);
            break;

        case 'SF':
            teamTable.DataTable().row('.selected', 1).data(origSFRow);
            break;

        case 'PF':
            teamTable.DataTable().row('.selected', 1).data(origPFRow);
            break;

        case 'C':
            teamTable.DataTable().row('.selected', 1).data(origCRow);
            break;
    }

    switch (rowIndex) {
        case 0:
            pg1 = 0;
            break;
        case 1:
            pg2 = 0;
            break;
        case 2:
            sg1 = 0;
            break;
        case 3:
            sg2 = 0;
            break;
        case 4:
            sf1 = 0;
            break;
        case 5:
            sf2 = 0;
            break;
        case 6:
            pf1 = 0;
            break;
        case 7:
            pf2 = 0;
            break;
        case 8:
            c1 = 0;
            break;
    }
    calculateTeamTotals();
}

function tableFilled() {
    pg1 = 1;
    pg2 = 1;
    sg1 = 1;
    sg2 = 1;
    sf1 = 1;
    sf2 = 1;
    pf1 = 1;
    pf2 = 1;
    c1 = 1;
}

function tableCleared() {
    pg1 = 0;
    pg2 = 0;
    sg1 = 0;
    sg2 = 0;
    sf1 = 0;
    sf2 = 0;
    pf1 = 0;
    pf2 = 0;
    c1 = 0;
}

function calculateTeamTotals() {
    var totalSalary = 60000;
    var rowsRemaining = 9;
    var ppg = 0;
    var lastPPG = 0;
    var grindersPPG = 0;

    var table = $('#team-table').DataTable();

    table.rows().every(function(rowIdx, tableLoop, rowLoop) {
        totalSalary = totalSalary - this.data().Salary;

        $('#salary-remaining').text(totalSalary);

        if (this.data().Salary > 0) {
            rowsRemaining = rowsRemaining - 1;
        }

        if (rowsRemaining === 0) {
            $('#salary-per-player').text(Math.round(totalSalary));
        } else {
            $('#salary-per-player').text(Math.round(totalSalary / rowsRemaining));
        }

        ppg = Math.round(Number(ppg) + Number(this.data().AvgPointsPerGame), 1);
        $('#total-avg').text(ppg);

        lastPPG = Math.round(Number(lastPPG) + Number(this.data().lastFivePoints), 1);
        $('#last-five-avg').text(lastPPG);

        grindersPPG = Math.round(Number(grindersPPG) + Number(this.data().grindersProj), 1);
        $('#total-rotogrinders').text(grindersPPG);
    });
}

function colorTableCells(row, data, index) {
    if (data.oppTeamDvPRank < 6 && data.oppTeamDvPRank !== "") {
        $('td:eq(3)', row).addClass('bright-green');
    }
    if (data.oppTeamDvPRank > 5 && data.oppTeamDvPRank < 11) {
        $('td:eq(3)', row).addClass('light-green');
    }
    if (data.oppTeamDvPRank > 20 && data.oppTeamDvPRank < 26) {
        $('td:eq(3)', row).addClass('light-red');
    }
    if (data.oppTeamDvPRank < 31 && data.oppTeamDvPRank > 25) {
        $('td:eq(3)', row).addClass('bright-red');
    }

    if (data.PPD > 5.1) {
        $('td:eq(9)', row).addClass('bright-green');
    }
    if (data.PPD > 4.7 && data.PPD < 5.2) {
        $('td:eq(9)', row).addClass('light-green');
    }
    if (data.PPD > 3.9 && data.PPD < 4.4) {
        $('td:eq(9)', row).addClass('light-red');
    }
    if (data.PPD < 4 && data.PPD !== "") {
        $('td:eq(9)', row).addClass('bright-red');
    }

    if (data.lastFivePPD > 5.1) {
        $('td:eq(12)', row).addClass('bright-green');
    }
    if (data.lastFivePPD > 4.7 && data.lastFivePPD < 5.2) {
        $('td:eq(12)', row).addClass('light-green');
    }
    if (data.lastFivePPD > 3.9 && data.lastFivePPD < 4.4) {
        $('td:eq(12)', row).addClass('light-red');
    }
    if (data.lastFivePPD < 4 && data.lastFivePPD !== "") {
        $('td:eq(12)', row).addClass('bright-red');
    }

    if (data.grindersPPD > 5.1) {
        $('td:eq(7)', row).addClass('bright-green');
    }
    if (data.grindersPPD > 4.7 && data.grindersPPD < 5.2) {
        $('td:eq(7)', row).addClass('light-green');
    }
    if (data.grindersPPD > 3.9 && data.grindersPPD < 4.4) {
        $('td:eq(7)', row).addClass('light-red');
    }
    if (data.grindersPPD < 4 && data.grindersPPD !== "") {
        $('td:eq(7)', row).addClass('bright-red');
    }

    if (data.oppPace > 101) {
        $('td:eq(5)', row).addClass('bright-green');
    }
    if (data.oppPace > 100 && data.oppPace < 101.01) {
        $('td:eq(5)', row).addClass('light-green');
    }
    if (data.oppPace > 96.5 && data.oppPace < 98) {
        $('td:eq(5)', row).addClass('light-red');
    }
    if (data.oppPace < 96.5 && data.oppPace !== "") {
        $('td:eq(5)', row).addClass('bright-red');
    }

    if (data.teamPace > 101) {
        $('td:eq(4)', row).addClass('bright-red');
    }
    if (data.teamPace > 100 && data.teamPace < 101.01) {
        $('td:eq(4)', row).addClass('light-red');
    }
    if (data.teamPace > 96.5 && data.teamPace < 98) {
        $('td:eq(4)', row).addClass('light-green');
    }
    if (data.teamPace < 96.5 && data.teamPace !== "") {
        $('td:eq(4)', row).addClass('bright-green');
    }
}
