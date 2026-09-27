document.addEventListener("DOMContentLoaded", function() {
    const footer = document.getElementById("site-footer");
    const sections = document.querySelectorAll(".section");
    
    if (sections.length > 0) {
        const lastSection = sections[sections.length - 1];
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    footer.classList.add("visible");
                } else {
                    footer.classList.remove("visible");
                }
            });
        }, { threshold: 0.5 }); 
        observer.observe(lastSection);
    }

    const menuToggle = document.getElementById("menu-toggle");
    const fullScreenMenu = document.getElementById("fullscreen-menu");

    menuToggle.addEventListener("click", () => {
        fullScreenMenu.classList.toggle("open");
    });
});