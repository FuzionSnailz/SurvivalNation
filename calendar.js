let currentDate = new Date();
let currentYear = currentDate.getFullYear();
let currentMonth = currentDate.getMonth();

// Example events
const events = {
    "2025-03-12": { title: "SurvivalNation Showcase", time: "7:00 PM", location: "Discord Live Event", artist: "QDex", description: "New music reveal and live Q&A session.", type: "show" },
    "2025-03-20": { title: "Game Release Trailer", time: "5:00 PM", location: "YouTube Premiere", artist: "SurvivalNation Studios", description: "First official trailer of our upcoming strategy game.", type: "release" },
    "2025-04-18": { title: "Album Release Party", time: "8:00 PM", location: "YouTube Live", artist: "QDex", description: "Celebrating the drop of the new album!", type: "release" }
};

// Build calendar
function buildCalendar(year, month) {
    const monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    document.getElementById("monthYear").innerText = `${monthNames[month]} ${year} Event Calendar`;

    const calendar = document.getElementById("calendar");
    calendar.innerHTML = "";

    // First day of the month
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty slots for first week
    for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement("div");
        calendar.appendChild(emptyDiv);
    }

    // Days
    for (let day = 1; day <= daysInMonth; day++) {
        const fullDate = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        const div = document.createElement("div");
        div.classList.add("calendar-day");
        div.innerHTML = `<div class="day-number">${day}</div>`;

        if (events[fullDate]) {
            const dot = document.createElement("div");
            dot.classList.add("event-dot", events[fullDate].type);
            div.appendChild(dot);

            div.addEventListener("click", () => showEvent(fullDate));
        }

        calendar.appendChild(div);
    }
}

// Show event on the right panel
function showEvent(date) {
    const ev = events[date];
    const details = document.getElementById("eventDetails");
    document.getElementById("eventTitle").innerText = ev.title;
    document.getElementById("eventDate").innerText = `Date: ${date}`;
    document.getElementById("eventTime").innerText = `Time: ${ev.time}`;
    document.getElementById("eventLocation").innerText = `Location: ${ev.location}`;
    document.getElementById("eventArtist").innerText = `Artist: ${ev.artist}`;
    document.getElementById("eventDescription").innerText = `Description: ${ev.description}`;
    const media = document.getElementById("eventMedia");
    media.innerHTML = ev.media ? ev.media : "";
}

// Navigation buttons
document.getElementById("prevMonth").addEventListener("click", () => changeMonth(-1));
document.getElementById("nextMonth").addEventListener("click", () => changeMonth(1));

function changeMonth(offset) {
    currentMonth += offset;
    if (currentMonth < 0) { currentMonth = 11; currentYear--; }
    if (currentMonth > 11) { currentMonth = 0; currentYear++; }
    buildCalendar(currentYear, currentMonth);
}

// Initialize
buildCalendar(currentYear, currentMonth);
