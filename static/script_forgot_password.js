function resetPassword() {
    const email = document.getElementById("reset-email").value;
    const newPassword = document.getElementById("new-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    if (newPassword !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
        return;
    }

    // Здесь можно добавить проверку пользователя и отправку данных на сервер.
    alert(`Password reset for email: ${email}`);
    window.location.href = "index.html"; // Вернуться на страницу входа.
}
