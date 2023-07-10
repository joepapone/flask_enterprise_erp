// Sort table text.
function SortTableTxt(sort_table, col) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(sort_table);
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    /* Make a loop that will continue until no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare, one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[col];
            y = rows[i + 1].getElementsByTagName("TD")[col];
            /* Check if the two rows should switch place, based on the direction, asc or desc: */
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount ++;
        } else {
            /* If no switching has been done AND the direction is "asc", set the direction to "desc" and run the while loop again. */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}  

// Get the modal
var modal = document.getElementById('id01');

// When user clicks anywhere outside the modal, it closes
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Submit delete
function DeleteFunction(input, item) {
    form_action = document.getElementById(input).value;
    document.getElementById("form").action = form_action;
    document.getElementById('id01').style.display='block';
    document.getElementById('msg-h1').innerHTML='Delete ' + item + '!';
    document.getElementById('msg-p').innerHTML='Are you sure you want to delete this ' + item + '?';
}

// Select dropdown
function DropdownFunction(source, destination, route) {
    let select_source = document.getElementById(source);
    let select_destination = document.getElementById(destination);

    // Get form source input select value
    select_id = select_source.value;
    
    // Get route response
    fetch(route + select_id).then(function(response) {
        // Convert response into json data
        response.json().then(function(data)  {
            // Diagnostic console
            console.table(data);

            // Create destination input select options
            let optionHTML = '';
            for (let item of data.list) {
                optionHTML += '<option value=' + item.id + '>' + item.label + '</option>';
            }
            // Update form destination input select
            select_destination.innerHTML = optionHTML;
        });
    });
}




// Activate timer according to url pathname
function refresh() {
    console.log('Window location pathname: ' + window.location.pathname);
    if (window.location.pathname == '/weight') {
        // Refresh weight every 1 sec. (1000ms)
        var myVar = setInterval(timer, 1000);
        console.log('Weight refresh active!');
    }
}


// Refresh timer
function timer() {
    var dt = new Date();
    var d = dt.toDateString();
    var t = dt.toLocaleTimeString();

    // Update date time
    document.getElementById('datetime').innerHTML=d+' - '+t;

    // Get weight value
    get_weight()
}


// Progress bar
var i = 0;
function progressBar() {
    if (i == 0) {
        i = 1;
        var elem = document.getElementById("progress_bar");
        var width = 0;
        var interval = 10;
        var id = setInterval(frame, 1000);
        function frame() {
            if (width >= interval) {
                get_mean();
                clearInterval(id);
                i = 0;
            } else {
                width++;
                elem.style.width = width*(100/interval) + "%";
                document.getElementById("progress_label").innerHTML='Time: '+width+' sec.';
                get_raw();
            }
        }
    }
}


// Get raw value
function get_raw() {
    fetch('/get/raw')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log('Raw-valve = '+text);
        // Update raw value
        document.getElementById('progress_block').style.display = '';
        document.getElementById('raw_value').innerHTML = text;
        document.getElementById('read').style.display = 'none';
        document.getElementById('store').style.display = 'none';
    });
}


// Get mean value
function get_mean() {
    fetch('/get/mean')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log('Mean-valve = '+text);
        // Update raw value
        document.getElementById('progress_label').innerHTML = 'Raw value average:';
        document.getElementById('progress_block').style.display = 'none';
        document.getElementById('raw_value').innerHTML = text;
        document.getElementById('read').style.display = '';
        document.getElementById('store').style.display = '';
    });
}


// Get weight value
function get_weight() {
    fetch('/get/weight')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log('Weight = '+text+' kg');
        // Update weight
        document.getElementById('weight-value').innerHTML = text;
    });
}

