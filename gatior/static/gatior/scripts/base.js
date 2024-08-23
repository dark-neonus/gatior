
// Collapse side panel
var side_panel_collapsed = localStorage.getItem('side_panel_collapsed') == "true";

var collapse_button = document.getElementById("collapse-side-panel");
var collapse_arrow = document.getElementById("collapse-side-panel-arrow");
var side_panel = document.getElementById("main-side_panel");
var side_panel_to_collapse = document.getElementById("side-panel-content");
var in_page = document.getElementById("in-page");
var main_container = document.getElementsByClassName("main_container")[0];
var page_header = document.getElementById("page-header");

var mobile_screen = window.matchMedia("(max-width: 768px)");

collapse_button.onclick = collapseSidePanelButton;
mobile_screen.addEventListener("change", function() { initSidePanel(); });

function collapseSidePanelButton(event) {
    event.stopPropagation();
    side_panel_collapsed = !side_panel_collapsed;
    initSidePanel();
}

initSidePanel()

function initSidePanel() {
    localStorage.setItem('side_panel_collapsed', side_panel_collapsed);

    var children = side_panel_to_collapse.children;
    if (side_panel_collapsed){
        // Collapse
        for (var i = 0; i < children.length; i++) {
            var tableChild = children[i];
            tableChild.style.display = "none";
        }
        side_panel_to_collapse.style.width = "0%";
        in_page.style.paddingRight = "0%";

        if (mobile_screen.matches) {
            // Mobile
            collapse_arrow.innerHTML = "keyboard_arrow_down";
            in_page.style.paddingTop = window.getComputedStyle(side_panel).height;
        }
        else {
            // Desktop
            collapse_arrow.innerHTML = "keyboard_arrow_left";
            in_page.style.paddingTop = "0%";
            in_page.style.paddingRight = window.getComputedStyle(side_panel).width;
        }
    }
    else {
        // Expand
        for (var i = 0; i < children.length; i++) {
            var tableChild = children[i];
            tableChild.style.display = "flex";
        }
        
        if (mobile_screen.matches) {
            // Mobile
            side_panel_to_collapse.style.width = "100%";
            in_page.style.paddingRight = "0%";
            in_page.style.paddingTop = window.getComputedStyle(side_panel).height
            collapse_arrow.innerHTML = "keyboard_arrow_up";
        }
        else {
            // Desktop
            side_panel_to_collapse.style.width = getComputedStyle(side_panel_to_collapse).getPropertyValue('--sidebar_width');
            in_page.style.paddingRight = window.getComputedStyle(side_panel).width;
            in_page.style.paddingTop = "0%";
            collapse_arrow.innerHTML = "keyboard_arrow_right";
        }
    }
}



// CSRFTOKEN

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');