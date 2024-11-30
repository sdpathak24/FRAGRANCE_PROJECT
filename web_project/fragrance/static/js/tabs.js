function openTab(event, tabName) {
    // Hide all tab content
    const tabContents = document.querySelectorAll(".tab-content");
    tabContents.forEach(content => content.style.display = "none");

    // Remove active class from all tab links
    const tabLinks = document.querySelectorAll(".tab-link");
    tabLinks.forEach(link => link.classList.remove("active"));

    // Show the selected tab content and set the active tab link
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.classList.add("active");
}
