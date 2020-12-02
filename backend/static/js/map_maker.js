var zoom_slider = document.getElementById("zoom_range");
var layers_slider = document.getElementById("layers_range");




 // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
var zoom_value = document.getElementById("zoom_value");
var layers_value = document.getElementById("layers_value");



zoom_value.innerHTML = zoom_slider.value;
layers_value.innerHTML = layers_slider.value;



zoom_slider.oninput = function() {
    zoom_value.innerHTML = this.value;
}

layers_slider.oninput = function() {
    layers_value.innerHTML = this.value;
}
