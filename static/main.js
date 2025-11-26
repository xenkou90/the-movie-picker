// --------------------------------------------------------------
// MOVIE GUESSING GAME LOGIC
// --------------------------------------------------------------
//
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
        // Get input, remove whitespace, make lowercase
        const guess = input.value.trim().toLowerCase();

        // If user submitted an empty guess, ignore
        if (!guess) return;

        // If correct
        if (guess === CORRECT_ANSWER) {
            result.textContent = "You are correct!";
            result.style.color = "limegreen";

        // If incorrect
        } else {
            result.textContent = "Try again!";
            result.style.color = "red";
        }
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

});
