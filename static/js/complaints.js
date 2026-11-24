// ================= MY COMPLAINTS JAVASCRIPT =================


// Get search and filter elements
const searchInput = document.getElementById("complaintSearch");
const statusFilter = document.getElementById("statusFilter");
const priorityFilter = document.getElementById("priorityFilter");


// Get all complaint cards
const complaintCards = document.querySelectorAll(".complaint-card");

// Message shown when no complaint matches the search/filter
const noResults = document.getElementById("noResults");


// ================= SEARCH + FILTER =================

function filterComplaints() {

    // Get current search text
    const searchText = searchInput.value.toLowerCase().trim();

    // Get selected filters
    const selectedStatus = statusFilter.value;
    const selectedPriority = priorityFilter.value;

    // Keep track of matching complaints
    let visibleComplaints = 0;


    // Check every complaint card
    complaintCards.forEach(function(card) {

        // Get complaint information from the card
        const complaintText =
            card.getAttribute("data-search").toLowerCase();

        const complaintStatus =
            card.getAttribute("data-status");

        const complaintPriority =
            card.getAttribute("data-priority");


        // Check search condition
        const matchesSearch =
            complaintText.includes(searchText);


        // Check status condition
        const matchesStatus =
            selectedStatus === "all" ||
            complaintStatus === selectedStatus;


        // Check priority condition
        const matchesPriority =
            selectedPriority === "all" ||
            complaintPriority === selectedPriority;


        // Show card only when all conditions match
        if (matchesSearch && matchesStatus && matchesPriority) {

            card.style.display = "block";
            visibleComplaints++;

        } else {

            card.style.display = "none";

        }

    });


    // Show "No complaints found" if nothing matches
    if (visibleComplaints === 0) {

        noResults.style.display = "block";

    } else {

        noResults.style.display = "none";

    }
}


// Run filtering when user types
searchInput.addEventListener("input", filterComplaints);


// Run filtering when status changes
statusFilter.addEventListener("change", filterComplaints);


// Run filtering when priority changes
priorityFilter.addEventListener("change", filterComplaints);


// ================= VIEW DETAILS =================

function showComplaintDetails(button) {

    // Find the complaint card containing the clicked button
    const card = button.closest(".complaint-card");


    // Get complaint information
    const complaintId =
        card.querySelector(".complaint-id").textContent.trim();

    const category =
        card.querySelector("h3").textContent.trim();

    const description =
        card.querySelector(".complaint-description").textContent.trim();

    const location =
        card.querySelector(".complaint-info strong").textContent.trim();

    const priority =
        card.querySelector(".priority").textContent.trim();

    const status =
        card.querySelector(".status").textContent.trim();


    // Create modal
    const modal = document.createElement("div");

    modal.className = "complaint-modal";


    // Create modal content
    modal.innerHTML = `
        <div class="complaint-modal-content">

            <button class="modal-close" onclick="closeComplaintDetails()">
                ×
            </button>

            <p class="modal-label">
                COMPLAINT DETAILS
            </p>

            <h2>${category}</h2>

            <div class="modal-id">
                ${complaintId}
            </div>

            <div class="modal-details">

                <div>
                    <span>Status</span>
                    <strong>${status}</strong>
                </div>

                <div>
                    <span>Priority</span>
                    <strong>${priority}</strong>
                </div>

                <div>
                    <span>Location</span>
                    <strong>${location}</strong>
                </div>

            </div>

            <div class="modal-description">

                <span>Description</span>

                <p>
                    ${description}
                </p>

            </div>

        </div>
    `;


    // Add modal to the page
    document.body.appendChild(modal);


    // Close modal when clicking outside the content
    modal.addEventListener("click", function(event) {

        if (event.target === modal) {
            closeComplaintDetails();
        }

    });

}


// ================= CLOSE MODAL =================

function closeComplaintDetails() {

    const modal =
        document.querySelector(".complaint-modal");

    if (modal) {
        modal.remove();
    }

}