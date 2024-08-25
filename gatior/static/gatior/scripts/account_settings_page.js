document.getElementById('upload-image').addEventListener('change', function(event) {
    // Check if a file was selected
    if (event.target.files && event.target.files[0]) {
        var reader = new FileReader();

        // When the file is read, set the background image
        reader.onload = function(e) {
            document.getElementById('account-image-container').style.backgroundImage = 'url(' + e.target.result + ')';
        }

        // Read the selected image file as a data URL
        reader.readAsDataURL(event.target.files[0]);

        // Remove "Select image" text
        document.getElementById("select-image-text").style.display = "none";

        // Set focus to enter post body field
        document.getElementById("first_name").focus();
    }
});
