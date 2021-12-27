function updateResultTable() {

    var input, filter, table, tr, td_type, td_place, td_town, i, type_text_val, place_text_val, town_text_val;

    // Declare variables
    input = document.getElementById("searchbar");
    filter = input.value.toUpperCase();
    table = document.getElementById("results_table");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {

        td_type = tr[i].getElementsByTagName("td")[0];
        td_place = tr[i].getElementsByTagName("td")[1];
        td_town = tr[i].getElementsByTagName("td")[2];

        if (td_type || td_place || td_town) {
            type_text_val = td_type.textContent || td_type.innerText;
            place_text_val = td_place.textContent || td_place.innerText;
            town_text_val = td_town.textContent || td_town.innerText;
            
            if(type_text_val.toUpperCase().indexOf(filter) > -1 || place_text_val.toUpperCase().indexOf(filter) > -1 || town_text_val.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}