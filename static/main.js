document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("guess-input");
    const button = document.getElementById("guess-btn");
    const result = document.getElementById("guess-result");

    const CORRECT_ANSWER = "bloodsport";

    function checkGuess() {
        const guess = input.value.trim().toLowerCase();

        if (!guess) return;

        if (guess === CORRECT_ANSWER) {
            result.textContent = "You are correct!";
            result.style.color = "limegreen";
        } else {
            result.textContent = "Try again!";
            result.style.color = "red";
        }
    }

    if (button) {
        button.addEventListener("click", checkGuess);
    }

    if (input) {
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                checkGuess();
            }
        });
    }
});