// Add events here easily
const events = {
    "2025-03-12": {
        title: "SurvivalNation Showcase",
        time: "7:00 PM",
        location: "Discord Live Event",
        artist: "QDex",
        description: "New music reveal and live Q&A session."
    },
    "2025-03-20": {
        title: "Game Release Trailer",
        time: "5:00 PM",
        location: "YouTube Premiere",
        artist: "SurvivalNation Studios",
        description: "First official trailer of our upcoming strategy game."
    }
};

events["2025-04-18"] = {
    title: "Album Release Party",
    time: "8:00 PM",
    location: "YouTube Live",
    artist: "QDex",
    description: "Celebrating the drop of the new album!"
};

const calendar = document.getElementById("calendar");

// Build calendar for current month
const date = new Date();
const year = date.getFullYear();
const month = date.getMonth();
const daysInMonth = new Date(year, month + 1, 0).getDate();

for (let day = 1; day <= daysInMonth; day++) {
    const fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

    const div = document.createElement("div");
    div.classList.add("calendar-day");

    div.innerHTML = `<div class="day-number">${day}</div>`;

    if (events[fullDate]) {
        const dot = document.createElement("div");
        dot.classList.add("event-dot");
        div.appendChild(dot);

        div.addEventListener("click", () => openEvent(fullDate));
    }

    calendar.appendChild(div);
}

// Modal functionality
const modal = document.getElementById("eventModal");
const closeBtn = document.querySelector(".close");

function openEvent(date) {
    const ev = events[date];
    document.getElementById("eventTitle").innerText = ev.title;
    document.getElementById("eventDate").innerText = date;
    document.getElementById("eventTime").innerText = ev.time;
    document.getElementById("eventLocation").innerText = ev.location;
    document.getElementById("eventArtist").innerText = ev.artist;
    document.getElementById("eventDescription").innerText = ev.description;
    modal.style.display = "block";
}

closeBtn.onclick = () => (modal.style.display = "none");
window.onclick = (e) => { if (e.target == modal) modal.style.display = "none"; };
