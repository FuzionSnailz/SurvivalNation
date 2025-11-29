const events = {
    "2025-11-29": { title: "NextUP 313", type: "show", time: "7:00 PM - 11:00 PM", location: "19560 Grand River Ave, Detroit, MI 48223", artist: "Jaidé", description: "Gen Z is taking over Pages Bookshop for a Tiny Desk–inspired showcase. We're Next-Up 313 and proud co-owners of Pages Bookshop 👏🏾 Come experience fresh voices, raw talent, and real vibes. Follow @hershekissis for more!!•YouTube: HersheKissis •Email: hershekissisbusiness@gmail.com (PAID inquiries only)", media: "e1.png", link: "https://www.instagram.com/p/DRFsyqfkSH-/" },
    "2025-12-07": { title: "Magazine Release", type: "show", time: "6:00 PM - 12:00 AM", location: "1995 Woodbridge St. DETROIT MI. 48207", artist: "Jaidé", description: "GET READY FOR DETROIT MICHIGAN 12/7 Dm @aiacollaborative to inquire! Tix via eventbrite", media: "e2.png", link: "https://www.instagram.com/p/DQs2W8lDgO8/" },
    "2025-11-10": { title: "Random", type: "show", time: "6:00 PM", location: "Club", artist: "Artist 3", description: "Test event 3", media: "test.png", link: "https://www.instagram.com/p/DRDYNongcKM/" },
    "2025-11-15": { title: "Her", type: "song", time: "8:00 PM", location: "Live Stream", artist: "Artist 4", description: "Test event 4", media: "test.png", link: "https://www.instagram.com/p/DRDYNongcKM/" },
    "2025-11-20": { title: "Event 5", type: "show", time: "7:30 PM", location: "Stage", artist: "Artist 5", description: "Test event 5", media: "test.png", link: "https://www.instagram.com/p/DRDYNongcKM/" }
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

    for (let i = 0; i < firstDay; i++) {
        const empty = document.createElement("div");
        calendar.appendChild(empty);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const fullDate = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
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
    document.getElementById("eventDate").innerText = `Date: ${date}`;
    document.getElementById("eventTime").innerText = `Time: ${ev.time}`;
    document.getElementById("eventLocation").innerText = `Location: ${ev.location}`;
    document.getElementById("eventArtist").innerText = `Artist: ${ev.artist}`;
    document.getElementById("eventDescription").innerHTML = `Description: ${ev.description} <br> <a href="${ev.link}" target="_blank">Link</a>`;
    const mediaDiv = document.getElementById("eventMedia");
    mediaDiv.innerHTML = ev.media ? `<img src="${ev.media}">` : "";
}

// Navigation buttons
document.getElementById("prevMonth").addEventListener("click", () => {
    currentMonth--;
    if(currentMonth < 0){ currentMonth = 11; currentYear--; }
    buildCalendar(currentMonth, currentYear);
});

document.getElementById("nextMonth").addEventListener("click", () => {
    currentMonth++;
    if(currentMonth > 11){ currentMonth = 0; currentYear++; }
    buildCalendar(currentMonth, currentYear);
});

// Initial build
buildCalendar(currentMonth, currentYear);
