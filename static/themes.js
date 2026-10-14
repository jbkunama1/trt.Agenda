(()=>{
 const themes=['ocean','graphite','paper','forest','sunset'];
 const requested=new URLSearchParams(location.search).get('theme');
 let saved='ocean';try{saved=localStorage.getItem('agenda-theme')||'ocean';}catch{}
 let current=themes.includes(requested)?requested:(themes.includes(saved)?saved:'ocean');
 document.documentElement.dataset.theme=current;
 document.addEventListener('DOMContentLoaded',()=>{
  if(new URLSearchParams(location.search).has('embed'))document.body.classList.add('embed');
  const select=document.getElementById('theme-select');
  const link=document.getElementById('view-link');
  function apply(){document.documentElement.dataset.theme=current;if(link)link.href='/static/view.html?theme='+encodeURIComponent(current);}
  apply();
  if(select){select.value=current;select.addEventListener('change',()=>{if(!themes.includes(select.value))return;current=select.value;apply();try{localStorage.setItem('agenda-theme',current);}catch{}const url=new URL(location.href);url.searchParams.set('theme',current);history.replaceState(null,'',url);});}
 });
})();
