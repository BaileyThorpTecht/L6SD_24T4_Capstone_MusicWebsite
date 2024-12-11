function lightingmode()
{
  if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
    document.documentElement.setAttribute('data-bs-theme','light');
  }
  else
  {
    document.documentElement.setAttribute('data-bs-theme','dark');
  }
}

// ########################################
// ##         Loading Screen             ##
// ########################################

var animation = lottie.loadAnimation({
  container: document.getElementById('lottie-container'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: "{% static 'videos/LottieLoadingScreen.json' %}" // Path to your Lottie JSON file
});

// Extend display time for the loading screen
window.addEventListener('load', function () {
  var loadingScreen = document.getElementById('loading-screen');
  setTimeout(function () {
      loadingScreen.classList.add('fade-out'); // Add fade-out class after 150 milliseconds
      setTimeout(function () {
          loadingScreen.style.display = 'none'; // Hide after fade-out
      }, 500); // Match CSS transition duration
  }, 150); // Delay for 150 milliseconds
});