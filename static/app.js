const $=id=>document.getElementById(id),U=window.AgendaUI;
let id=U.id,data,version,editing=false,loading=false,saving=false;
const embed=new URLSearchParams(location.search).has('embed');
function render(){
 U.theme(data.theme);U.layout(editing?'list':data.layout);$('heading').textContent=data.title;$('summary').textContent=U.summary(data);
 $('editor').hidden=!editing;$('actions').hidden=!editing;$('edit').hidden=editing||embed;
 $('agenda-select').disabled=editing||loading;$('view-link').href='/static/view.html?agenda='+id;
 $('list').replaceChildren();let minute=Number(data.start.slice(0,2))*60+Number(data.start.slice(3));
 data.items.forEach((item,index)=>{const row=U.el('li','card'),content=U.el('div','content');row.style.flexGrow=item.minutes;row.append(U.badge(item,index),content);
 if(editing){const fields=U.el('div','edit-fields');const emoji=U.el('input','emoji');emoji.maxLength=16;emoji.placeholder='😀';emoji.value=item.emoji||'';emoji.setAttribute('aria-label','Emoji für Punkt '+(index+1));emoji.oninput=()=>{const v=emoji.value.trim();if(v)item.emoji=v;else delete item.emoji;};
 const title=U.el('input');title.value=item.title;title.required=true;title.maxLength=160;title.setAttribute('aria-label','Punkt '+(index+1));title.oninput=()=>item.title=title.value;
 const duration=U.el('input');duration.type='number';duration.min=1;duration.max=1440;duration.step=1;duration.required=true;duration.value=item.minutes;duration.setAttribute('aria-label','Dauer in Minuten');duration.oninput=()=>item.minutes=Number(duration.value);duration.onchange=()=>{if(duration.checkValidity())render();};fields.append(emoji,title,duration);content.append(fields);
 const tools=U.el('div','tools');[['↑',-1],['↓',1],['Entfernen',0]].forEach(([text,delta])=>{const b=U.el('button','ghost',text);b.disabled=delta!==0&&(index+delta<0||index+delta>=data.items.length);b.onclick=()=>{if(saving)return;if(!delta)data.items.splice(index,1);else [data.items[index],data.items[index+delta]]=[data.items[index+delta],data.items[index]];render();};tools.append(b);});content.append(tools);
 }else{content.append(U.el('div','item-title',item.title));row.append(U.el('span','duration',item.minutes+' Min.'));}
 content.append(U.el('div','time',U.clock(minute)+' – '+U.clock(minute+item.minutes)));minute+=item.minutes;$('list').append(row);});
}
async function load(){if(loading||editing||id===null)return;loading=true;$('agenda-select').disabled=true;try{const [a,b]=await Promise.all([fetch('/api/agenda?agenda='+id),fetch('/api/agendas')]);if(!a.ok||!b.ok)throw Error('Laden fehlgeschlagen.');const payload=await a.json(),list=await b.json();data=payload.data;version=payload.version;$('agenda-select').replaceChildren(...list.agendas.map(i=>{const o=U.el('option','',i.id+' · '+i.title);o.value=i.id;return o;}));$('agenda-select').value=id;render();$('status').textContent='';}catch(e){$('status').textContent=e.message;}finally{loading=false;$('agenda-select').disabled=editing;}}
$('agenda-select').onchange=()=>{if(editing||loading)return;id=Number($('agenda-select').value);data=null;const url=new URL(location.href);url.searchParams.set('agenda',id);history.replaceState(null,'',url);load();};
$('edit').onclick=()=>{if(!data||loading)return;editing=true;$('title').value=data.title;$('start').value=data.start;$('theme-select').value=data.theme;$('layout-select').value=data.layout||'list';render();};
$('title').oninput=()=>{data.title=$('title').value;$('heading').textContent=data.title;};
$('start').onchange=()=>{if($('start').value){data.start=$('start').value;render();}};
$('theme-select').onchange=()=>{data.theme=$('theme-select').value;U.theme(data.theme);};
$('layout-select').onchange=()=>{data.layout=$('layout-select').value;$('status').textContent='Layout wird nach dem Speichern angezeigt.';};
$('add').onclick=()=>{if(saving||data.items.length>=50)return;data.items.push({title:'Neuer Punkt',minutes:5});render();};
$('cancel').onclick=()=>{if(saving)return;editing=false;$('key').value='';load();};
$('save').onclick=async()=>{if([...document.querySelectorAll('#editor input:not([type=password]),#list input')].some(i=>!i.reportValidity()))return;saving=true;const controls=[...document.querySelectorAll('#editor input,#editor select,#list button,#list input,#actions button')];controls.forEach(i=>i.disabled=true);try{const response=await fetch('/api/agenda?agenda='+id,{method:'PUT',headers:{'Content-Type':'application/json','X-Edit-Key':$('key').value},body:JSON.stringify({data,version})});const result=await response.json();if(!response.ok)throw Error(result.error||'Speichern fehlgeschlagen.');version=result.version;editing=false;$('key').value='';render();const option=[...$('agenda-select').options].find(i=>Number(i.value)===id);if(option)option.textContent=id+' · '+data.title;$('status').textContent='Agenda, Theme und Layout gespeichert ✓';}catch(e){$('status').textContent=e.message;}finally{saving=false;controls.forEach(i=>i.disabled=false);}};
if(id===null){$('status').textContent='Ungültige Agenda. Bitte agenda=1 bis agenda=5 verwenden.';$('edit').disabled=true;}else{load();setInterval(load,15000);}
