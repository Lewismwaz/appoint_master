document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with class "available-percentage"
    var percentageElements = document.querySelectorAll('.available-percentage');
 
    // Loop through each percentage element
    percentageElements.forEach(function(element) {
       // Get the percentage value from the element
       var percentage = parseFloat(element.innerText);
 
       // Calculate the radius based on the percentage range
       var radius = 36; // Default radius
 
       if (percentage <= 10) {
           radius = 36; // Set radius for percentages between 1% and 10%
       } else if (percentage <= 20) {
           radius = 36; // Set radius for percentages between 11% and 20%
       } else if (percentage <= 30) {
           radius = 36; // Set radius for percentages between 21% and 30%
       } else if (percentage <= 40) {
           radius = 36; // Set radius for percentages between 31% and 40%
       } else if (percentage <= 50) {
           radius = 36; // Set radius for percentages between 41% and 50%
       } else if (percentage <= 60) {
           radius = 36; // Set radius for percentages between 51% and 60%
       } else if (percentage <= 70) {
           radius = 36; // Set radius for percentages between 61% and 70%
       } else if (percentage <= 80) {
           radius = 36; // Set radius for percentages between 71% and 80%
       } else if (percentage <= 90) {
           radius = 36; // Set radius for percentages between 81% and 90%
       } else if (percentage <= 100) {
           radius = 36; // Set radius for percentages between 91% and 100%
       }
 
       // Get the parent progress element
       var progressElement = element.closest('.progress');
 
       // Get the circle element within the progress element
       var circle = progressElement.querySelector('circle');
 
       // Calculate the circumference
       var circumference = 2 * Math.PI * radius;
 
       // Set the radius and dash attributes for the initial full (100%) stroke
       circle.setAttribute('r', radius);
       circle.setAttribute('stroke-dasharray', circumference);
       circle.setAttribute('stroke-dashoffset', 0);
 
       // Trigger a reflow by accessing the offsetHeight property
       progressElement.offsetHeight;
 
       // Apply the smooth animation to reduce the stroke to 0%
       circle.style.transition = 'stroke-dashoffset 2s ease-in-out';
       circle.setAttribute('stroke-dashoffset', circumference);
 
       // Apply the final stroke based on the current percentage with a delayed transition
       var finalDashoffset = circumference * (1 - (percentage / 100));
       setTimeout(function() {
          circle.style.transition = 'stroke-dashoffset 1.5s ease-in-out'; // Transition for final stroke
          circle.setAttribute('stroke-dashoffset', finalDashoffset);
       }, 2000); // Delay the final stroke update after the initial animation
    });
 });
 