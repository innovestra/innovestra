document.addEventListener('DOMContentLoaded', function () {
  // Password toggle for new password
  const togglePassword1 = document.getElementById('togglePassword1');
  const passwordInput1 = document.getElementById('id_new_password1');
  const eyeIcon1 = document.getElementById('eyeIcon1');

  togglePassword1.addEventListener('click', function () {
    const isPassword = passwordInput1.getAttribute('type') === 'password';
    passwordInput1.setAttribute('type', isPassword ? 'text' : 'password');
    eyeIcon1.classList.toggle('fa-eye');
    eyeIcon1.classList.toggle('fa-eye-slash');
    eyeIcon1.classList.toggle('text-muted');
    eyeIcon1.classList.toggle('text-success');
  });

  // Password toggle for confirm password
  const togglePassword2 = document.getElementById('togglePassword2');
  const passwordInput2 = document.getElementById('id_new_password2');
  const eyeIcon2 = document.getElementById('eyeIcon2');

  togglePassword2.addEventListener('click', function () {
    const isPassword = passwordInput2.getAttribute('type') === 'password';
    passwordInput2.setAttribute('type', isPassword ? 'text' : 'password');
    eyeIcon2.classList.toggle('fa-eye');
    eyeIcon2.classList.toggle('fa-eye-slash');
    eyeIcon2.classList.toggle('text-muted');
    eyeIcon2.classList.toggle('text-success');
  });
});
document.addEventListener('DOMContentLoaded', function () {
  // Password toggle for new password
  const togglePassword1 = document.getElementById('togglePassword1');
  const passwordInput1 = document.getElementById('id_password1');
  const eyeIcon1 = document.getElementById('eyeIcon1');

  togglePassword1.addEventListener('click', function () {
    const isPassword = passwordInput1.getAttribute('type') === 'password';
    passwordInput1.setAttribute('type', isPassword ? 'text' : 'password');
    eyeIcon1.classList.toggle('fa-eye');
    eyeIcon1.classList.toggle('fa-eye-slash');
    eyeIcon1.classList.toggle('text-muted');
    eyeIcon1.classList.toggle('text-success');
  });
  // Password toggle for confirm password
  const togglePassword2 = document.getElementById('togglePassword2');
  const passwordInput2 = document.getElementById('id_password2');
  const eyeIcon2 = document.getElementById('eyeIcon2');

  togglePassword2.addEventListener('click', function () {
    const isPassword = passwordInput2.getAttribute('type') === 'password';
    passwordInput2.setAttribute('type', isPassword ? 'text' : 'password');
    eyeIcon2.classList.toggle('fa-eye');
    eyeIcon2.classList.toggle('fa-eye-slash');
    eyeIcon2.classList.toggle('text-muted');
    eyeIcon2.classList.toggle('text-success');
  });
});
document.addEventListener('DOMContentLoaded', function () {
  const togglePassword = document.getElementById('togglePassword');
  const passwordField = document.getElementById('id_password1');
  const eyeIcon = document.getElementById('eyeIcon');

  togglePassword.addEventListener('click', function () {
    const isPassword = passwordField.getAttribute('type') === 'password';
    passwordField.setAttribute('type', isPassword ? 'text' : 'password');
    eyeIcon.classList.toggle('fa-eye');
    eyeIcon.classList.toggle('fa-eye-slash');
    eyeIcon.classList.toggle('text-muted');
    eyeIcon.classList.toggle('text-success');
  });
});

document.addEventListener('DOMContentLoaded', function () {
  // Counter Animation
  const counters = document.querySelectorAll('.counter');
  const speed = 200; // Animation speed

  const animateCounter = (counter) => {
    const target = +counter.getAttribute('data-target');
    const increment = target / speed;
    let count = 0;

    const updateCount = () => {
      count += increment;
      if (count < target) {
        counter.innerText = Math.ceil(count);
        setTimeout(updateCount, 1);
      } else {
        counter.innerText = target;
      }
    };

    updateCount();
  };

  // Intersection Observer for triggering animation when element is visible
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const counter = entry.target;
          if (!counter.classList.contains('animated')) {
            counter.classList.add('animated');
            animateCounter(counter);
          }
        }
      });
    },
    {
      threshold: 0.5,
    }
  );

  // Observe all counters
  counters.forEach((counter) => {
    observer.observe(counter);
  });
});

document.addEventListener("DOMContentLoaded", function() {
    // Handle all form submit buttons globally
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", function() {
            // Find the first submit button in the form
            const submitBtn = form.querySelector("button[type='submit']");
            if (!submitBtn) return;

            // Add spinner if not already added
            if (!submitBtn.querySelector(".spinner-border")) {
                const spinner = document.createElement("span");
                spinner.className = "spinner-border spinner-border-sm ms-2";
                spinner.setAttribute("role", "status");
                spinner.setAttribute("aria-hidden", "true");
                submitBtn.appendChild(spinner);
            }

            // Change text to indicate loading
            const btnText = submitBtn.querySelector(".btn-text");
            if (btnText) {
                btnText.textContent = "Processing...";
            }

            // Disable the button and show spinner
            submitBtn.disabled = true;
            const spinner = submitBtn.querySelector(".spinner-border");
            spinner.classList.remove("d-none");

            // Optional: auto re-enable after timeout (for non-redirect forms)
            setTimeout(() => {
                submitBtn.disabled = false;
                if (btnText) btnText.textContent = "Submit";
                spinner.classList.add("d-none");
            }, 6000);
        });
    });
});
