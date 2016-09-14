function draftkingsNFL() {
    var draftkingsJson;

    //Grab the data.json file
    $.getJSON('assets/json/draftkingsNFLData.json', function(data) {
        draftkingsJson = data;
    }).done(function() {
        for (var i = 1; i < draftkingsJson.length; i++) {
            switch (draftkingsJson[i].Position) {
                case "QB":
                    qbTable.row.add([
                        draftkingsJson[i]['Name'],
                        "$" + draftkingsJson[i]['Salary'],
                        draftkingsJson[i]['GameInfo'],
                        draftkingsJson[i]['AvgPointsPerGame'],
                        "",
                        "",
                        ""
                    ]).draw();
                    break;

                case "RB":
                    rbTable.row.add([
                        draftkingsJson[i]['Name'],
                        "$" + draftkingsJson[i]['Salary'],
                        draftkingsJson[i]['GameInfo'],
                        draftkingsJson[i]['AvgPointsPerGame'],
                        "",
                        "",
                        ""
                    ]).draw();
                    break;

                case "WR":
                    wrTable.row.add([
                        draftkingsJson[i]['Name'],
                        "$" + draftkingsJson[i]['Salary'],
                        draftkingsJson[i]['GameInfo'],
                        draftkingsJson[i]['AvgPointsPerGame'],
                        "",
                        "",
                        ""
                    ]).draw();
                    break;

                case "TE":
                    teTable.row.add([
                        draftkingsJson[i]['Name'],
                        "$" + draftkingsJson[i]['Salary'],
                        draftkingsJson[i]['GameInfo'],
                        draftkingsJson[i]['AvgPointsPerGame'],
                        "",
                        "",
                        ""
                    ]).draw();
                    break;

                case "DST":
                    defTable.row.add([
                        draftkingsJson[i]['Name'],
                        "$" + draftkingsJson[i]['Salary'],
                        draftkingsJson[i]['GameInfo'],
                        draftkingsJson[i]['AvgPointsPerGame'],
                        "",
                        "",
                        ""
                    ]).draw();
                    break;
            }

            if (i === (draftkingsJson.length - 1)) {

                //Initialize variables
                qbArray = qbTable.columns(3).data()[0];
                var qbArrayLength = qbArray.length;
                var qbStDev = 0;
                var qbAvg = 0;

                rbArray = rbTable.columns(3).data()[0];
                var rbArrayLength = rbArray.length;
                var rbStDev = 0;
                var rbAvg = 0;

                wrArray = wrTable.columns(3).data()[0];
                var wrArrayLength = wrArray.length;
                var wrStDev = 0;
                var wrAvg = 0;

                teArray = teTable.columns(3).data()[0];
                var teArrayLength = teArray.length;
                var teStDev = 0;
                var teAvg = 0;

                defArray = defTable.columns(3).data()[0];
                var defArrayLength = defArray.length;
                var defStDev = 0;
                var defAvg = 0;

                //remove $ from beginning of dataset
                removeDollar(qbArray, qbTable);
                removeDollar(rbArray, rbTable);
                removeDollar(wrArray, wrTable);
                removeDollar(teArray, teTable);
                removeDollar(defArray, defTable);

                //Calc the stDev and avg for data sets
                qbStDev = math.std(qbArray);
                qbAvg = math.mean(qbArray);

                rbStDev = math.std(rbArray);
                rbAvg = math.mean(rbArray);

                wrStDev = math.std(wrArray);
                wrAvg = math.mean(wrArray);

                teStDev = math.std(teArray);
                teAvg = math.mean(teArray);

                defStDev = math.std(defArray);
                defAvg = math.mean(defArray);

                //Calculate the values for last few columns
                calcVals(qbTable, qbStDev, qbAvg);
                calcVals(rbTable, rbStDev, rbAvg);
                calcVals(wrTable, wrStDev, wrAvg);
                calcVals(teTable, teStDev, teAvg);
                calcVals(defTable, defStDev, defAvg);

            }
        }
    })


};

function removeDollar(dataArray, table) {
    for (var k = 1; k < dataArray.length; k++) {
        table.cell(k, 4).data(dataArray[k]);
        if (dataArray[k] === "0") {
            dataArray.splice(k, 1);
            k = k - 1;
        }
    }
}

function calcVals(table, stDev, avg) {
    table.rows().every(function(rowIdx, tableLoop, rowLoop) {
        var d = this.data();
        var salary = d[1].slice(1)

        d[4] = ((d[3] - avg) / stDev).toFixed(2); //creating the stDev value
        d[5] = ((d[4] / salary) * 10000).toFixed(2);
        //If the avg is > than 0
        if (d[3] > 0) {
            d[6] = (salary / d[3]).toFixed(2);
        } else {
            d[6] = "N/A";
        }

        this.invalidate(); // invalidate the data DataTables has cached for this row
    });

    table.draw();
}
