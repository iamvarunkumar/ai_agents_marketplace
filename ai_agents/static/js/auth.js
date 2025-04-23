document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form"); // Assume register form has this ID
  const loginError = document.getElementById("login-error");
  const registerError = document.getElementById("register-error"); // Assume register form has error div

  // Function to handle API errors
  function displayError(element, message) {
    if (element) {
      element.textContent = message;
      element.classList.remove("d-none");
    }
  }
  function clearError(element) {
    if (element) {
      element.textContent = "";
      element.classList.add("d-none");
    }
  }

  // --- Login Handler ---
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearError(loginError);

      const formData = new FormData(loginForm);
      const data = Object.fromEntries(formData.entries());
      // Remove csrf token if not needed for API (depends on session vs token auth)
      delete data.csrfmiddlewaretoken;

      try {
        const response = await fetch("/api/auth/login/", {
          // Use correct API endpoint
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Add CSRF header if using Django sessions + CSRF protection on API
          },
          body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
          // Store tokens (Example: localStorage - consider security)
          localStorage.setItem("accessToken", result.access);
          localStorage.setItem("refreshToken", result.refresh);
          // Redirect to dashboard
          window.location.href = "/dashboard"; // Change to your dashboard URL
        } else {
          // Handle specific errors from backend
          let errorMessage = "Login failed. Please check your credentials.";
          if (result.detail) {
            errorMessage = result.detail;
          } else if (result.non_field_errors) {
            errorMessage = result.non_field_errors.join(" ");
          }
          displayError(loginError, errorMessage);
        }
      } catch (error) {
        console.error("Login error:", error);
        displayError(
          loginError,
          "An unexpected error occurred. Please try again."
        );
      }
    });
  }

  // --- Registration Handler ---
  if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearError(registerError);

      const formData = new FormData(registerForm);
      const data = Object.fromEntries(formData.entries());
      delete data.csrfmiddlewaretoken; // If needed

      try {
        const response = await fetch("/api/auth/register/", {
          // Correct endpoint
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        const result = await response.json(); // Read response even if error

        if (response.ok || response.status === 201) {
          // Registration successful - maybe redirect to login or auto-login
          alert("Registration successful! Please login."); // Simple feedback
          window.location.href = "/login"; // Redirect to login
        } else {
          // Handle errors (e.g., email exists, password mismatch)
          let errorMessage = "Registration failed.";
          if (result.email) errorMessage += ` Email: ${result.email.join(" ")}`;
          if (result.username)
            errorMessage += ` Username: ${result.username.join(" ")}`;
          if (result.password)
            errorMessage += ` Password: ${result.password.join(" ")}`;
          if (result.detail) errorMessage = result.detail; // General DRF errors

          displayError(registerError, errorMessage);
        }
      } catch (error) {
        console.error("Registration error:", error);
        displayError(
          registerError,
          "An unexpected error occurred during registration."
        );
      }
    });
  }

  // --- Logout Logic --- (Add a logout button/link handler)
  const logoutButton = document.getElementById("logout-button"); // Assume button exists
if (logoutButton) {
logoutButton.addEventListener("click", () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    window.location.href = "/login"; // Redirect to login
    });
}
}); // End DOMContentLoaded
