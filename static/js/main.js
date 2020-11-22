$(document).ready(function() {
    $("#splitter").kendoSplitter();
});


$("#splitter").kendoSplitter({
    panes: [
        { collapsible: true, min: "100px", max: "300px" },
        { collapsible: true }
    ],
    orientation: "vertical"
});



function dropDown() {
  document.getElementById("fontDropdown").classList.toggle("show");
}

