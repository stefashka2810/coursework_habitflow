// // // Функция регистрации пользователя
// // function register() {
// //     let firstName = document.getElementById("first-name").value;
// //     let lastName = document.getElementById("last-name").value;
// //     let email = document.getElementById("email").value;
// //     let password = document.getElementById("password").value;
// //     let confirmPassword = document.getElementById("confirm-password").value;
// //
// //     if (password !== confirmPassword) {
// //         alert("Passwords do not match!");
// //         return;
// //     }
// //
// //     if (!firstName || !lastName || !email || !password) {
// //         alert("Please fill in all fields!");
// //         return;
// //     }
// //
// //     if (localStorage.getItem(email)) {
// //         alert("User already exists! Please log in.");
// //         return;
// //     }
// //
// //     // Сохраняем пользователя в localStorage
// //     localStorage.setItem(email, JSON.stringify({
// //         firstName: firstName,
// //         lastName: lastName,
// //         password: password
// //     }));
// //
// //     alert("Registration successful! Please log in.");
// //     window.location.href = "registration.html"; // Перенаправляем на страницу входа
// // }
// //
// // // Функция входа в систему
// // function login() {
// //     let email = document.getElementById("login-email").value;
// //     let password = document.getElementById("login-password").value;
// //     let userData = localStorage.getItem(email);
// //
// //     if (!userData) {
// //         document.getElementById("login-error").innerText = "User not found. Please register.";
// //         return;
// //     }
// //
// //     let user = JSON.parse(userData);
// //
// //     if (user.password === password) {
// //         alert(`Welcome, ${user.firstName} ${user.lastName}!`);
// //         localStorage.setItem("user", JSON.stringify(user)); // Сохраняем текущего пользователя
// //         window.location.href = "main_after_registration.html"; // Перенаправляем после входа
// //     } else {
// //         document.getElementById("login-error").innerText = "Incorrect password!";
// //     }
// // }
// // Функция регистрации пользователя
// function register() {
//     let firstName = document.getElementById("first-name").value.trim();
//     let lastName = document.getElementById("last-name").value.trim();
//     let email = document.getElementById("email").value.trim();
//     let password = document.getElementById("password").value.trim();
//     let confirmPassword = document.getElementById("confirm-password").value.trim();
//
//     // Проверяем, заполнены ли все поля
//     if (!firstName || !lastName || !email || !password || !confirmPassword) {
//         alert("Please fill in all fields!");
//         return;
//     }
//
//     // Проверяем, совпадают ли пароли
//     if (password !== confirmPassword) {
//         alert("Passwords do not match!");
//         return;
//     }
//
//     // Проверяем, зарегистрирован ли пользователь уже
//     if (localStorage.getItem(email)) {
//         alert("User already exists! Please log in.");
//         return;
//     }
//
//     // Сохраняем пользователя в localStorage
//     localStorage.setItem(email, JSON.stringify({
//         firstName: firstName,
//         lastName: lastName,
//         password: password
//     }));
//
//     alert("Registration successful! Please log in.");
//     window.location.href = "registration.html"; // Перенаправление на страницу входа
// }
//
// // Функция входа в систему
// function login() {
//     let email = document.getElementById("login-email").value.trim();
//     let password = document.getElementById("login-password").value.trim();
//
//     if (!email || !password) {
//         alert("Please enter your email and password!");
//         return;
//     }
//
//     let userData = localStorage.getItem(email);
//
//     if (!userData) {
//         document.getElementById("login-error").innerText = "User not found. Please register.";
//         return;
//     }
//
//     let user = JSON.parse(userData);
//
//     if (user.password === password) {
//         alert(`Welcome, ${user.firstName} ${user.lastName}!`);
//         localStorage.setItem("user", JSON.stringify(user)); // Сохраняем текущего пользователя
//         window.location.href = "main_after_registration.html"; // Перенаправляем после входа
//     } else {
//         document.getElementById("login-error").innerText = "Incorrect password!";
//     }
// }
function handleRegistration() {
    let firstName = document.getElementById("first-name").value.trim();
    let lastName = document.getElementById("last-name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let confirmPassword = document.getElementById("confirm-password").value.trim();

    // Проверяем, заполнены ли все поля
    if (!firstName || !lastName || !email || !password || !confirmPassword) {
        alert("Please fill in all fields!");
        return;
    }

    // Проверяем, совпадают ли пароли
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Проверяем, зарегистрирован ли пользователь уже
    if (localStorage.getItem(email)) {
        alert("User already exists! Please log in.");
        return;
    }

    // Сохраняем пользователя в localStorage
    localStorage.setItem(email, JSON.stringify({
        firstName: firstName,
        lastName: lastName,
        password: password
    }));

    alert("Registration successful! Please log in.");
    window.location.href = "registration.html"; // Переход на страницу входа
}

function login() {
    let email = document.getElementById("login-email").value.trim();
    let password = document.getElementById("login-password").value.trim();

    if (!email || !password) {
        alert("Please enter your email and password!");
        return;
    }

    let userData = localStorage.getItem(email);

    if (!userData) {
        document.getElementById("login-error").innerText = "User not found. Please register.";
        return;
    }

    let user = JSON.parse(userData);

    if (user.password === password) {
        alert(`Welcome, ${user.firstName} ${user.lastName}!`);
        localStorage.setItem("user", JSON.stringify(user)); // Сохраняем текущего пользователя
        window.location.href = "main_after_registration.html"; // Теперь после входа ведет на главную страницу!
    } else {
        document.getElementById("login-error").innerText = "Incorrect password!";
    }
}
