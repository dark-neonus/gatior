
// Screen adaptation
var small_screen = window.matchMedia("(max-width: 1000px)");
var comments_section = document.getElementById("comments-section");
var post_container = document.getElementById("post-container");



if (in_page == null) {
    var in_page = document.getElementById("in_page");
}

small_screen.addEventListener("change", initCommentSection);

initCommentSection();

function initCommentSection() {
    if (small_screen.matches) {
        // Mobile view
        comments_section.style.height = "100%";
    }
    else {
        // Desktop view
        comments_section.style.height = Math.max(
            parseInt(window.getComputedStyle(post_container).height),
            parseInt(window.getComputedStyle(in_page).height)) + "px";
    }
}

// Image switching

var post_image = document.getElementById("post-image");
var post_image_container = document.getElementById("post-image-container");
var post_image_button = document.getElementById("post-image-button");
var image_expanded = true;

post_image_button.onclick = changeImageAppearance;

function changeImageAppearance() {
    image_expanded = !image_expanded;
    initImageAppearance()
}

function initImageAppearance() {
    
    if (image_expanded) {
        post_image.style.objectFit = "cover";
        post_image.style.aspectRatio = "1 / 1";
        post_image_container.style.aspectRatio = "1 / 1";
    }
    else {
        post_image.style.objectFit = "contain";
        post_image.style.aspectRatio = "auto";
        post_image_container.style.aspectRatio = "auto";
    }
    initCommentSection();
}


