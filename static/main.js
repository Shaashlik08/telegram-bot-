document.addEventListener("DOMContentLoaded", function () {
    const authForms = document.querySelectorAll(".auth-form");

    authForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const username = form.querySelector("#username");
            const password = form.querySelector("#password");

            if (username && username.value.length < 3) {
                alert("Username must be at least 3 characters.");
                event.preventDefault();
            }

            if (password && password.value.length < 6) {
                alert("Password must be at least 6 characters.");
                event.preventDefault();
            }
        });
    });

    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm("Are you sure you want to delete this user?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    const searchInput = document.getElementById("userSearch");
    const usersTable = document.getElementById("usersTable");

    if (searchInput && usersTable) {
        searchInput.addEventListener("keyup", function () {
            const filter = searchInput.value.toLowerCase();
            const rows = usersTable.getElementsByTagName("tr");

            for (let i = 1; i < rows.length; i++) {
                const rowText = rows[i].innerText.toLowerCase();

                if (rowText.includes(filter)) {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }
            }
        });
    }
});