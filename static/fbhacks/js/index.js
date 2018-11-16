function showEvents() {
    document.getElementById("events").style.display = "block";
    document.getElementById("history").style.display = "none";
    document.getElementById("contacts").style.display = "none";

    document.getElementById("event_a").classList.add("active");
    document.getElementById("history_a").classList.remove("active");
    document.getElementById("contact_a").classList.remove("active");
}

function showHistory() {
    document.getElementById("events").style.display = "none";
    document.getElementById("history").style.display = "block";
    document.getElementById("contacts").style.display = "none";

    document.getElementById("event_a").classList.remove("active");
    document.getElementById("history_a").classList.add("active");
    document.getElementById("contact_a").classList.remove("active");
}

function showContacts() {
    document.getElementById("events").style.display = "none";
    document.getElementById("history").style.display = "none";
    document.getElementById("contacts").style.display = "block";

    document.getElementById("event_a").classList.remove("active");
    document.getElementById("history_a").classList.remove("active");
    document.getElementById("contact_a").classList.add("active");
}