// -------------------------------------------------------------
// main.js — UNIVERSAL SCRIPT FOR ALL PAGES
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    // =========================================================
    // 1. MOBILE MENU (Works on all pages)
    // =========================================================
    const hamburger = document.getElementById("hamburger-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    const mobileClose = document.getElementById("mobile-menu-close");

    if (hamburger && mobileMenu) {
        hamburger.addEventListener("click", () => {
            mobileMenu.style.display = "flex";
        });
    }

    if (mobileClose) {
        mobileClose.addEventListener("click", () => {
            mobileMenu.style.display = "none";
        });
    }


    // =========================================================
    // 2. GUESSING GAME (Only runs on About + Guess pages)
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
    // COPY MOVIE TITLE TO CLIPBOARD + TOAST
    // =========================================================
    const copyBtn = document.getElementById("copy-btn");
    const toast = document.getElementById("copy-toast");

    if (copyBtn && toast) {
        copyBtn.addEventListener("click", () => {
            const title = document.querySelector(".movie-title")?.textContent || "";

            if (!title) return;

            navigator.clipboard.writeText(title).then(() => {
                // Show toast
                toast.classList.add("show");

                // Hide toast after 1.4 sec
                setTimeout(() => {
                    toast.classList.remove("show");
                }, 1400);
            }).catch(err => {
                console.error("Clipboard error:", err);
            });
        });
    }
});
