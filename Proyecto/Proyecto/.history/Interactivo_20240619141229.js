function openTab(tabName) {
    var tabs = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
}
