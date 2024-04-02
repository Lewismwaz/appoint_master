function updateTime() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    var day = now.toLocaleDateString('en-US', { weekday: 'long' });
    var month = now.toLocaleDateString('en-US', { month: 'long' });
    var date = now.getDate();
    var year = now.getFullYear();
    var ampm = hours >= 12 ? 'PM' : 'AM'; // Check if it's AM or PM

    // Convert hours to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12; // If hours is 0, make it 12

    // Add leading zeros to minutes and seconds if they are less than 10
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    var timeString = day + ', ' + month + ' ' + date + ', ' + year + ' ' + hours + ':' + minutes + ':' + seconds + ' ' + ampm;
    document.getElementById('real-time-clock').textContent = timeString;
}

updateTime(); // Call initially
setInterval(updateTime, 1000); // Update every second