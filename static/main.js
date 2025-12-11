// -------------------------------------------------------------
// main.js — UNIVERSAL SCRIPT FOR ALL PAGES
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    // =========================================================
    // LAVENDER CYBERPUNK HAMBURGER TOGGLE
    // =========================================================
    const hamb = document.getElementById("hamburger-btn");
    const mobileMenu = document.getElementById("mobile-menu");

    if (hamb && mobileMenu) {
        hamb.addEventListener("click", () => {
            hamb.classList.toggle("active");
            mobileMenu.style.display = "flex";
        });
    }

    const mobileClose = document.getElementById("mobile-menu-close");

    if (mobileClose) {
        mobileClose.addEventListener("click", () => {
            mobileMenu.style.display = "none";
            hamb.classList.remove("active");
        });
    }


    // =========================================================
    // GUESSING GAME (Only runs on About + Guess pages)
    // =========================================================
    const guessInput = document.getElementById("guess-input");
    const guessButton = document.getElementById("guess-btn");
    const guessModal = document.getElementById("guess-modal");
    const guessModalImg = document.getElementById("guess-modal-img");
    const guessClose = document.getElementById("guess-modal-close");

    const CORRECT_ANSWER = "bloodsport";

    function checkGuess() {
        if (!guessInput) return;

        const guess = guessInput.value.trim().toLowerCase();
        if (!guess) return;

        // Correct/wrong modal images
        if (guess === CORRECT_ANSWER) {
            guessModalImg.src = "/static/correct.jpg";
        } else {
            guessModalImg.src = "/static/wrong.jpg";
        }

        guessModal.style.display = "flex";
    }

    if (guessButton) {
        guessButton.addEventListener("click", checkGuess);
    }

    if (guessInput) {
        guessInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                checkGuess();
            }
        });
    }

    if (guessClose) {
        guessClose.addEventListener("click", () => {
            guessModal.style.display = "none";
        });
    }


    // =========================================================
    // COPY MOVIE TITLE TO CLIPBOARD + TOOLTIP
    // =========================================================
    const copyBtn = document.getElementById("copy-btn");
    const titleTextEl = document.querySelector(".movie-title");
    const titleText = titleTextEl ? titleTextEl.innerText.trim() : "";

    if (copyBtn) {
        copyBtn.addEventListener("click", () => {

            navigator.clipboard.writeText(titleText).then(() => {
                copyBtn.classList.add("show-tooltip");

                setTimeout(() => {
                    copyBtn.classList.remove("show-tooltip");
                }, 900);
            });
        });
    }
