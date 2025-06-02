// JavaScript for polling and UI updates
class GitHubEventsMonitor {
    constructor() {
        this.eventsContainer = document.getElementById('events-container');
        this.pollInterval = 15000; // 15 seconds
        this.init();
    }
    
    init() {
        this.fetchEvents();
        setInterval(() => this.fetchEvents(), this.pollInterval);
    }
    
    async fetchEvents() {
        // Your implementation here
        // Fetch events from /api/events
        // Update UI with new events
    }
    
    displayEvents(events) {
        // Your implementation here
        // Format and display events according to requirements
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GitHubEventsMonitor();
});