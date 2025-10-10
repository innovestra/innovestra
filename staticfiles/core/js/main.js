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
