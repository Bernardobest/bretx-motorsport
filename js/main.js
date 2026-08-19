// ==========================================================================
// BretX Motorsport — main.js
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Mobile nav toggle ---------- */
  const burger = document.getElementById('burgerBtn');
  const nav = document.getElementById('mainNav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => nav.classList.remove('open'));
    });
  }

  /* ---------- Vehicle category tabs ---------- */
  const vtabs = document.querySelectorAll('.vtab');
  if (vtabs.length) {
    vtabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.getAttribute('data-tab');
        vtabs.forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');
        document.querySelectorAll('.vehicle-block').forEach(block => {
          block.hidden = block.id !== targetId;
        });
      });
    });
  }

  /* ---------- Footer year ---------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Floating CTA visibility ---------- */
  const floatingCta = document.querySelector('.floating-cta');
  const hero = document.querySelector('.hero');
  if (floatingCta && hero) {
    const observer = new IntersectionObserver(([entry]) => {
      floatingCta.classList.toggle('visible', !entry.isIntersecting);
    }, { threshold: 0 });
    observer.observe(hero);
  }

  /* ---------- Animate power bars on scroll into view ---------- */
  const bars = document.querySelectorAll('.power-bar .bar-fill');
  if ('IntersectionObserver' in window && bars.length) {
    const barObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const fill = entry.target;
          const targetWidth = fill.style.width;
          fill.style.width = '0%';
          requestAnimationFrame(() => {
            setTimeout(() => { fill.style.width = targetWidth; }, 50);
          });
          barObserver.unobserve(fill);
        }
      });
    }, { threshold: 0.3 });
    bars.forEach(bar => {
      // stash the target width via data attribute pattern (inline style already set)
      barObserver.observe(bar);
    });
  }

  /* ---------- Cal.com inline embed ----------
     Remplace CAL_LINK par ton lien Cal.com réel
     (ex: "ton-pseudo/reprogrammation-moteur"). Créer un compte gratuit sur cal.com,
     configurer tes disponibilités, puis coller le lien ici. */
  const CAL_LINK = "bernardo-bb-7vad5u/rendez-vous-bretx-motorsport";
  const calContainer = document.getElementById('cal-inline');

  function initCalEmbed() {
    if (typeof Cal === 'undefined') return false;
    try {
      Cal("init", { origin: "https://cal.com" });
      Cal("inline", {
        elementOrSelector: "#cal-inline",
        calLink: CAL_LINK,
        config: { theme: "dark", layout: "month_view" }
      });
      Cal("ui", {
        theme: "dark",
        styles: { branding: { brandColor: "#e30613" } },
        hideEventTypeDetails: false
      });
      return true;
    } catch (e) {
      return false;
    }
  }

  // Try to init; if the Cal script hasn't loaded yet, retry briefly, then fall back.
  let attempts = 0;
  const tryInterval = setInterval(() => {
    attempts++;
    if (initCalEmbed() || attempts > 20) {
      clearInterval(tryInterval);
      if (attempts > 20 && calContainer && !calContainer.querySelector('iframe')) {
        calContainer.innerHTML = `
          <div class="booking-fallback">
            <p>Le calendrier de réservation n'a pas pu se charger.</p>
            <p>Réservez directement via <a href="https://cal.com/${CAL_LINK}" target="_blank" rel="noopener">ce lien</a>,
            ou contactez-moi via le formulaire ci-dessous.</p>
          </div>`;
      }
    }
  }, 300);

  /* ---------- Simple client-side validation feedback (Netlify handles submission) ---------- */
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', () => {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.textContent = 'Envoi en cours...';
        submitBtn.disabled = true;
      }
    });
  }

});
