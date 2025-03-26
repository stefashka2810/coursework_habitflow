document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            this.parentElement.remove();
        });
    });

    const addButton = document.querySelector(".add-button");
    const habitList = document.querySelector(".habit-list");

    addButton.addEventListener("click", function () {
        const newHabit = document.createElement("li");
        newHabit.innerHTML = `New Habit <button class="delete-btn">🗑️</button>`;

        newHabit.querySelector(".delete-btn").addEventListener("click", function () {
            newHabit.remove();
        });

        habitList.appendChild(newHabit);
    });
});
