(()=>{
 const $=id=>document.getElementById(id),U=window.AgendaUI;
 function current(){const v=$('agenda-select').value||String(U.id||'');return ['1','2','3','4','5'].includes(v)?v:null;}
 function viewUrl(id){return new URL('/static/view.html?agenda='+id,location.href).href;}
 async function copy(text){
  if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return;}
  const area=document.createElement('textarea');area.value=text;area.setAttribute('readonly','');area.style.position='fixed';area.style.opacity='0';
  document.body.append(area);area.select();const ok=document.execCommand('copy');area.remove();
  if(!ok)throw Error('Kopieren nicht möglich. Bitte Link manuell kopieren.');
 }
 async function run(kind){
  const id=current();if(!id){$('status').textContent='Bitte gültige Agenda auswählen.';return;}
  const url=viewUrl(id);
  const text=kind==='iframe'?'<iframe src="'+url+'" title="Agenda '+id+'" style="width:100%;height:640px;border:0;"></iframe>':url;
  try{await copy(text);$('status').textContent=(kind==='iframe'?'iFrame-Code':'View-Link')+' für Agenda '+id+' kopiert ✓';}
  catch(e){$('status').textContent=e.message||'Kopieren fehlgeschlagen.';}
 }
 $('copy-link').onclick=()=>run('link');
 $('copy-iframe').onclick=()=>run('iframe');
})();
