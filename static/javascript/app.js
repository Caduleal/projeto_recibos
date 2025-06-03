document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('toggleAllPasswords');
  if (!toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    const passwordInputs = document.querySelectorAll('.password-input');

    passwordInputs.forEach(input => {
      if (input.type === 'password') {
        input.type = 'text';
      } else {
        input.type = 'password';
      }
    });

    const icon = toggleBtn.querySelector('i');
    if (icon.classList.contains('fa-eye')) {
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    } else {
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  });
  if (form){
    form.adddEventListener('submit',() =>{
      passwordInputs.forEach(input =>{
        input.type = 'password';
      });
    });
  }
});
