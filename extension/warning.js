// extension/warning.js
const params = new URLSearchParams(location.search);
const url = params.get('url') || '';
document.getElementById('msg').innerText = `Blocked: ${url}`;
document.getElementById('go').addEventListener('click', function() {
  if (url) { window.location = url; }
});
document.getElementById('back').addEventListener('click', function() {
  window.history.back();
});
