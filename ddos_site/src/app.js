document.addEventListener('DOMContentLoaded', () => {
  // ===== Bubbles canvas animation (soda-style background) =====
  const canvas = document.getElementById('bubbles-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    const bubbles = [];

    function resize() {
      width = canvas.width = canvas.offsetWidth;
      height = canvas.height = canvas.offsetHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    function createBubble() {
      const radius = Math.random() * 8 + 4;
      return {
        x: Math.random() * width,
        y: height + radius + Math.random() * height * 0.2,
        radius,
        speed: Math.random() * 0.5 + 0.3,
        drift: (Math.random() - 0.5) * 0.3,
        alpha: Math.random() * 0.4 + 0.2,
      };
    }

    for (let i = 0; i < 80; i++) {
      bubbles.push(createBubble());
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);
      for (let b of bubbles) {
        b.y -= b.speed;
        b.x += b.drift;
        if (b.y + b.radius < -10 || b.x < -50 || b.x > width + 50) {
          Object.assign(b, createBubble());
        }
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${b.alpha})`;
        ctx.fill();
      }
      requestAnimationFrame(draw);
    }
    draw();
  }

  // ===== Smooth scroll for internal links =====
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      const targetId = link.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
