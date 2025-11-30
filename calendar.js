const events = {
    "2025-11-29": { title: "Next-UP 313", type: "show", time: "7:00 PM - 11:00 PM", location: "19560 Grand River Ave, Detroit, MI 48223", artist: "Jaidé", description: "Gen Z is taking over Pages Bookshop for a Tiny Desk–inspired showcase. We're Next-Up 313 and proud co-owners of Pages Bookshop 👏🏾 Come experience fresh voices, raw talent, and real vibes. Follow @hershekissis for more!!•YouTube: HersheKissis •Email: hershekissisbusiness@gmail.com (PAID inquiries only)", media: "e1.png", link: "https://www.instagram.com/p/DRFsyqfkSH-/" },
    "2025-12-07": { title: "Magazine Release", type: "show", time: "6:00 PM - 12:00 AM", location: "1995 Woodbridge St. DETROIT MI. 48207", artist: "Jaidé", description: "GET READY FOR DETROIT MICHIGAN 12/7 Dm @aiacollaborative to inquire! Tix via eventbrite", media: "e2.png", link: "https://www.instagram.com/p/DQs2W8lDgO8/" },
    "2025-12-09": { title: "Spades", type: "song", time: "9:00 AM EST", location: "All Music Straming Platforms", artist: "KWA ft.ANT$", description: "New Music Release", media: "ANT2.png"},
    "2025-12-16": { title: "Maybe If I Fall Back", type: "song", time: "9:00 AM EST", location: "All Music Straming Platforms", artist: "ANT$", description: "New Music Release", media: "ANT11.png"},
    "2025-12-23": { title: "My Mind", type: "song", time: "9:00 AM EST", location: "All Music Straming Platforms", artist: "ANT$", description: "New Music Release", media: "ANT6.png"},
};

let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

const calendar = document.getElementById("calendar");
const monthYear = document.getElementById("monthYear");

function buildCalendar(month, year) {
    calendar.innerHTML = "";

    const monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    monthYear.innerText = `${monthNames[month]} ${year} Event Calendar`;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty cells before first day
    for (let i = 0; i < firstDay; i++) {
        const empty = document.createElement("div");
        calendar.appendChild(empty);
    }

    // Days
    for (let day = 1; day <= daysInMonth; day++) {
        const fullDate = `${year}-${String(month + 1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        const dayDiv = document.createElement("div");
        dayDiv.classList.add("calendar-day");
        dayDiv.innerHTML = `<div class="day-number">${day}</div>`;

        if(events[fullDate]){
            const dot = document.createElement("div");
            dot.classList.add("event-dot");
            dot.classList.add(events[fullDate].type === "show" ? "event-show" : "event-song");
            dayDiv.appendChild(dot);

            dayDiv.addEventListener("click", () => showEvent(fullDate));
        }

        calendar.appendChild(dayDiv);
    }
}

function showEvent(date) {
    const ev = events[date];
    document.getElementById("eventTitle").innerText = ev.title;
    document.getElementById("eventDate").innerHTML = `<strong>Date:</strong> ${date}`;
    document.getElementById("eventTime").innerHTML = `<strong>Time:</strong> ${ev.time}`;
    document.getElementById("eventLocation").innerHTML = `<strong>Location:</strong> ${ev.location}`;
    document.getElementById("eventArtist").innerHTML = `<strong>Artist:</strong> ${ev.artist}`;
    document.getElementById("eventDescription").innerHTML = `<strong>Description:</strong> ${ev.description}`;
    const mediaDiv = document.getElementById("eventMedia");
    mediaDiv.innerHTML = ev.media ? `<a href="${ev.link}" target="_blank"><img src="${ev.media}"></a>` : "";
}

// Navigation
document.getElementById("prevMonth").addEventListener("click", () => {
    currentMonth--;
    if(currentMonth < 0) { currentMonth = 11; currentYear--; }
    buildCalendar(currentMonth, currentYear);
});

document.getElementById("nextMonth").addEventListener("click", () => {
    currentMonth++;
    if(currentMonth > 11) { currentMonth = 0; currentYear++; }
    buildCalendar(currentMonth, currentYear);
});

// Initial build
buildCalendar(currentMonth, currentYear);