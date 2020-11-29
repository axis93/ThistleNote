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
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

