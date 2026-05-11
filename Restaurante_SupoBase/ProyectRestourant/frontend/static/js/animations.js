function initBackgroundParticles() {
    const canvas = document.createElement('canvas');
    canvas.id = 'bg-canvas';
    document.body.prepend(canvas);

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const colors = ['#ff6b6b', '#4ecdc4', '#ffd166'];
    const numParticles = 30;

    for (let i = 0; i < numParticles; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            size: Math.random() * 20 + 5,
            color: colors[Math.floor(Math.random() * colors.length)],
            vx: (Math.random() - 0.5) * 1.5,
            vy: (Math.random() - 0.5) * 1.5,
            rotation: Math.random() * 360,
            shape: Math.random() > 0.5 ? 'circle' : 'square',
            alpha: Math.random() * 0.5 + 0.1
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.rotation += 1;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rotation * Math.PI / 180);
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;

            if (p.shape === 'circle') {
                ctx.beginPath();
                ctx.arc(0, 0, p.size, 0, Math.PI * 2);
                ctx.fill();
            } else {
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
            }

            ctx.restore();
        });

        requestAnimationFrame(animate);
    }
    animate();
}

// --- Side Navigation Toggle ---
function toggleNav() {
    const nav = document.getElementById("sideNavigation");
    if (nav) {
        nav.classList.toggle("active");
    }
}

// Make toggleNav global for onclick
window.toggleNav = toggleNav;

function initPageAnimations() {

    const reveals = document.querySelectorAll('.animate-reveal');
    if (reveals.length > 0) {
        anime({
            targets: '.animate-reveal',
            translateY: [50, 0],
            opacity: [0, 1],
            delay: anime.stagger(200),
            duration: 1000,
            easing: 'easeOutExpo'
        });
    }


    const cards = document.querySelectorAll('.retro-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
            card.style.boxShadow = `0 0 20px var(--primary-color)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            card.style.boxShadow = `6px 6px 0px var(--text-color)`;
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initBackgroundParticles();
    initRadialNav();
    setTimeout(initPageAnimations, 100);
});
