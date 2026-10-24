window.AgendaUI=(()=>{
 const themes=['ocean','graphite','paper','forest','sunset','70s','80s','90s','modern','cyberpunk','neon','terminal','pastell'];
 const layouts=['list','columns','timeline','tiles'];
 const raw=new URLSearchParams(location.search).get('agenda')||'1';
 const valid=['1','2','3','4','5'].includes(raw);
 const id=valid?Number(raw):null;
 function theme(value){document.documentElement.dataset.theme=themes.includes(value)?value:'ocean';}
 function layout(value){document.documentElement.dataset.layout=layouts.includes(value)?value:'list';}
 function el(tag,cls,text){const node=document.createElement(tag);if(cls)node.className=cls;if(text!==undefined)node.textContent=text;return node;}
 function badge(item,index){const node=el('span',item.emoji?'number is-emoji':'number',item.emoji||String(index+1).padStart(2,'0'));return node;}
 function clock(total){const days=Math.floor(total/1440);return String(Math.floor(total/60)%24).padStart(2,'0')+':'+String(total%60).padStart(2,'0')+(days?' (+'+days+' Tag'+(days>1?'e':'')+')':'');}
 function summary(data){const start=Number(data.start.slice(0,2))*60+Number(data.start.slice(3));const total=data.items.reduce((s,i)=>s+i.minutes,0);return data.items.length+' Punkte · '+total+' Minuten · '+data.start+'–'+clock(start+total);}
 theme('ocean');layout('list');
 document.addEventListener('DOMContentLoaded',()=>{if(new URLSearchParams(location.search).has('embed'))document.body.classList.add('embed');});
 return {themes,layouts,id,theme,layout,el,badge,clock,summary};
})();
