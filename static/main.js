// --------------------------------------------------------------
// MOVIE GUESSING GAME LOGIC
// --------------------------------------------------------------
// This script powers the interactive guessing feature on the
// About page. It listens for button clicks or Enter key presses,
// compares the user’s guess against the correct movie, and 
// displays feedback dynamically without needing a page reload.
// --------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {

    // ----------------------------------------------------------
    // Grab references to UI elements
    // ----------------------------------------------------------
    // Input field where user types their movie guess
    const input = document.getElementById("guess-input");

    // Button that submits the guess
    const button = document.getElementById("guess-btn");

    // Text element where feedback ("correct" / "try again") appears
    const result = document.getElementById("guess-result");

    // ----------------------------------------------------------
    // The correct answer the user must guess
    // Stored in lowercase to make comparisons easier
    // ----------------------------------------------------------
    const CORRECT_ANSWER = "bloodsport";


    // ----------------------------------------------------------
    // Function: Compare the input value with the correct answer
    // ----------------------------------------------------------
    function checkGuess() {
        const guess = input.value.trim().toLowerCase();
        if (!guess) return;

        const modal = document.getElementById("guess-modal");
        const modalImg = document.getElementById("guess-modal-img");

        if (guess === CORRECT_ANSWER) {
            modalImg.src = "/static/correct.jpg";
        } else {
            modalImg.src = "/static/wrong.jpg";
        }

        modal.style.display = "flex"  // show modal
    }


    // ----------------------------------------------------------
    // EVENT LISTENERS
    // ----------------------------------------------------------

    // When clicking the "Submit" button
    if (button) {
        button.addEventListener("click", checkGuess);
    }

    // When pressing Enter inside the input field
    if (input) {
        input.addEventListener("keydown", (e) => {

            // Prevent form submission on Enter
            if (e.key === "Enter") {
                e.preventDefault();
                checkGuess();
            }
        });
    }

    // Close button handler
    const closeBtn = document.getElementById("guess-modal-close");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            document.getElementById("guess-modal").style.display = "none";
        });
    }
});


// --------------------------------------------------------------
// MOBILE HAMBURGER MENU
// --------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    const menu = document.getElementById("mobile-menu");
    const openBtn = document.getElementById("hamburger-btn");
    const closeBtn = document.getElementById("mobile-meny-close");

    if (openBtn) {
        openBtn.addEventListener("click", () => {
            menu.style.display = "flex";
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            menu.style.display = "none";
        });
    }
});