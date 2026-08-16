(() => {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    initBackgroundToggle();
    initAudioPlayer();
    initProjectsFilter();
  });

  function initProjectsFilter() {
    const nav = document.getElementById('projects-nav');
    const list = document.getElementById('projects-list');
    if (!nav || !list) return;

    const navItems = nav.querySelectorAll('.projects-nav-item');
    const rows = list.querySelectorAll('.projects-row');

    nav.addEventListener('click', (e) => {
      const item = e.target.closest('.projects-nav-item');
      if (!item) return;
      e.preventDefault();

      navItems.forEach((el) => el.classList.remove('active'));
      item.classList.add('active');

      const org = item.dataset.org;
      rows.forEach((row) => {
        const show = org === 'all' || row.dataset.org === org;
        row.classList.toggle('is-hidden', !show);
      });
    });
  }

  function initBackgroundToggle() {
    const top = document.getElementById('top');
    const trigger = document.getElementById('show');
    if (!top || !trigger) return;

    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      top.classList.toggle('background_space');
      top.classList.toggle('background_initial');
    });
  }

  function initAudioPlayer() {
    const btn = document.getElementById('playpausebtn');
    if (!btn) return;

    let audio = null;
    btn.setAttribute('role', 'button');
    btn.setAttribute('aria-pressed', 'false');
    btn.setAttribute('aria-label', 'Play background audio');

    btn.addEventListener('click', async (e) => {
      e.preventDefault();

      if (!audio) {
        audio = new Audio('/blog/assets/sound/carl-sagan-pale-blue-dot.mp3');
        audio.loop = true;
        audio.preload = 'none';
      }

      try {
        if (audio.paused) {
          await audio.play();
          btn.setAttribute('aria-pressed', 'true');
        } else {
          audio.pause();
          btn.setAttribute('aria-pressed', 'false');
        }
      } catch (err) {
        console.warn('Audio playback blocked:', err);
      }
    });
  }
})();
