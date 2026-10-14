const $=id=>document.getElementById(id);
let data,version,editing=false,loading=false;
const embed=new URLSearchParams(location.search).has('embed');
if(embed){document.body.classList.add('embed');$('edit').hidden=true;}
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
function clock(total){const day=Math.floor(total/1440);return String(Math.floor(total/60)%24).padStart(2,'0')+':'+String(total%60).padStart(2,'0')+(day?' (+'+day+' Tag'+(day>1?'e':'')+')':'');}
function render(){
 $('heading').textContent=data.title;
 const total=data.items.reduce((s,i)=>s+i.minutes,0);let minute=Number(data.start.slice(0,2))*60+Number(data.start.slice(3));
 $('summary').textContent=data.items.length+' Punkte · '+total+' Minuten · '+data.start+'–'+clock(minute+total);
 $('editor').hidden=!editing;$('actions').hidden=!editing;$('edit').hidden=editing||embed;
 $('list').replaceChildren();
 data.items.forEach((item,index)=>{
 const li=el('li','card'),num=el('span','number',String(index+1).padStart(2,'0')),content=el('div','content');li.append(num,content);
 if(editing){
 const fields=el('div','edit-fields');const title=el('input');title.value=item.title;title.maxLength=160;title.required=true;title.setAttribute('aria-label','Titel Punkt '+(index+1));title.oninput=()=>item.title=title.value;
 const duration=el('input');duration.type='number';duration.min=1;duration.max=1440;duration.step=1;duration.required=true;duration.value=item.minutes;duration.setAttribute('aria-label','Dauer in Minuten');duration.oninput=()=>{item.minutes=Number(duration.value);};duration.onchange=()=>{if(duration.checkValidity())render();};fields.append(title,duration);content.append(fields);
 const tools=el('div','tools');[['↑',-1],['↓',1],['Entfernen',0]].forEach(([label,delta])=>{const b=el('button','ghost',label);b.type='button';b.disabled=delta!==0&&(index+delta<0||index+delta>=data.items.length);b.onclick=()=>{if(!delta)data.items.splice(index,1);else [data.items[index],data.items[index+delta]]=[data.items[index+delta],data.items[index]];render();};tools.append(b);});content.append(tools);
 }else{content.append(el('div','item-title',item.title));li.append(el('span','duration',item.minutes+' Min.'));}
 content.append(el('div','time',clock(minute)+' – '+clock(minute+item.minutes)));minute+=item.minutes;$('list').append(li);
 });
}
async function load(){if(loading||editing)return;loading=true;try{const r=await fetch('/api/agenda');if(!r.ok)throw Error('Laden fehlgeschlagen.');const p=await r.json();if(editing)return;data=p.data;version=p.version;render();$('status').textContent='';}catch(e){$('status').textContent=e.message;}finally{loading=false;}}
$('edit').onclick=()=>{if(!data||loading)return;editing=true;$('title').value=data.title;$('start').value=data.start;render();};
$('title').oninput=()=>{data.title=$('title').value;$('heading').textContent=data.title;};
$('start').onchange=()=>{if($('start').value){data.start=$('start').value;render();}};
$('add').onclick=()=>{if(data.items.length>=50)return;data.items.push({title:'Neuer Punkt',minutes:5});render();};
$('cancel').onclick=()=>{editing=false;$('key').value='';load();};
$('save').onclick=async()=>{const bad=[...document.querySelectorAll('input:not([type=password])')].find(i=>!i.reportValidity());if(bad)return;$('save').disabled=true;try{const r=await fetch('/api/agenda',{method:'PUT',headers:{'Content-Type':'application/json','X-Edit-Key':$('key').value},body:JSON.stringify({data,version})});const p=await r.json();if(!r.ok)throw Error(p.error||'Speichern fehlgeschlagen.');version=p.version;editing=false;$('key').value='';render();$('status').textContent='Gespeichert ✓';}catch(e){$('status').textContent=e.message;}finally{$('save').disabled=false;}};
load();setInterval(load,15000);
