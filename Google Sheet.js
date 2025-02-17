const scriptURL = 'https://script.google.com/macros/s/AKfycbwl6_3Qz4YZwf5QPCKLWwrH9AVd4dz4XDfUzlc_Yqs7ZGfkBH8iMf93iT40B-h5G2vstQ/exec'

const form = document.forms['contact-form']

form.addEventListener('submit', e => {
  
  e.preventDefault()
  
  fetch(scriptURL, { method: 'POST', body: new FormData(form)})
  .then(response => alert("Thank you! Form is submitted" ))
  .then(() => { window.location.reload(); })
  .catch(error => console.error('Error!', error.message))
})