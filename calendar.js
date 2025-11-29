let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

const events = {
    "2025-11-12": {
        title: "SurvivalNation Showcase",
        type: "show-event",
        time: "7:00 PM",
        location: "Discord Live Event",
        artist: "QDex",
        description: "New music reveal and live Q&A session.",
        media: '<a href="https://example.com" target="_blank">Event Link</a>'
    },
    "2025-11-20": {
        title: "Game Release Trailer",
        type: "song-release",
        time: "5:00 PM",
        location: "YouTube Premiere",
        artist: "SurvivalNation Studios",
        description: "First official trailer of our upcoming strategy game.",
        media: '<img src="trailer.png" alt="Trailer Image">'
    }
};

// DOM Elements
const calendar = document.getElementById("calendar");
const monthYear = document.getElementById("monthYear");
const prevBtn = document.getElementById("prevMonth");
const nextBtn = document.getElementById("nextMonth");
const eventDetails = document.getElementById("eventDetails");

function buildCalendar(month, year) {
    calendar.innerHTML = "";
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    monthYear.textContent = `${monthNames[month]} ${year} Event Calendar`;

    for(let day=1; day <= daysInMonth; day++){
        const fullDate = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        const div = document.createElement("div");
        div.classList.add("calendar-day");
        div.innerHTML = `<div class="day-number">${day}</div>`;

        if(events[fullDate]){
            const dot = document.createElement("div");
            dot.classList.add("event-dot", events[fullDate].type);
            div.appendChild(dot);

            div.addEventListener("click", () => showEvent(fullDate));
        }

        calendar.appendChild(div);
    }
}

function showEvent(date){
    const ev = events[date];
    document.getElementById("eventTitle").innerText = ev.title;
    document.getElementById("eventDate").innerText = `Date: ${date}`;
    document.getElementById("eventTime").innerText = `Time: ${ev.time}`;
    document.getElementById("eventLocation").innerText = `Location: ${ev.location}`;
    document.getElementById("eventArtist").innerText = `Artist: ${ev.artist}`;
    document.getElementById("eventDescription").innerText = ev.description;
    document.getElementById("eventMedia").innerHTML = ev.media || '';
}

// Navigation
prevBtn.addEventListener("click", ()=>{
    currentMonth--;
    if(currentMonth < 0){ currentMonth = 11; currentYear--; }
    buildCalendar(currentMonth, currentYear);
});

nextBtn.addEventListener("click", ()=>{
    currentMonth++;
    if(currentMonth > 11){ currentMonth = 0; currentYear++; }
    buildCalendar(currentMonth, currentYear);
});

// Initialize
buildCalendar(currentMonth, currentYear);
