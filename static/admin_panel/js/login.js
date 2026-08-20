document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.input-box input').forEach(input=>{
    const box=input.parentElement;
    const enable=()=>{
      if(!input.readOnly) return;
      input.readOnly=false;
      input.setAttribute('autocomplete', /user|email/i.test(input.name||'')||input.id==='username' ? 'username' : (input.type==='password' ? 'current-password' : 'on'));
      setTimeout(()=>input.focus(),0);
      ['mousedown','focus','click'].forEach(e=>input.removeEventListener(e,enable));
    };
    ['mousedown','focus','click'].forEach(e=>input.addEventListener(e,enable));
    const upd=()=> box.classList.toggle('filled', !!(input.value||'').trim());
    ['input','change','blur'].forEach(e=>input.addEventListener(e,upd));
    setTimeout(upd,200);
  });
});