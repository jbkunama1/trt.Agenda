(()=>{
 const parameter=new URLSearchParams(location.search).get('fit');
 const embedded=window.self!==window.top;
 if(parameter==='0'||(!embedded&&parameter!=='1'))return;
 const root=document.documentElement,main=document.querySelector('main');
 root.classList.add('agenda-fit');let queued=false;
 function fit(){queued=false;const w=root.clientWidth,h=root.clientHeight;if(w<1||h<1)return;const padding=Math.min(12,w*0.025,h*0.025);const width=Math.max(1,w-padding*2),height=Math.max(1,h-padding*2);main.style.width=width+'px';main.style.transform='none';const naturalW=Math.max(width,main.scrollWidth),naturalH=Math.max(1,main.offsetHeight,main.scrollHeight);const scale=Math.min(1,width/naturalW,height/naturalH);main.style.transform='scale('+scale+')';main.style.left=(padding+(width-naturalW*scale)/2)+'px';main.style.top=padding+'px';}
 function schedule(){if(!queued){queued=true;requestAnimationFrame(fit);}}
 window.addEventListener('resize',schedule);
 new MutationObserver(schedule).observe(main,{childList:true,subtree:true,characterData:true});
 if(window.ResizeObserver)new ResizeObserver(schedule).observe(document.body);
 if(document.fonts)document.fonts.ready.then(schedule);
 document.addEventListener('visibilitychange',schedule);
 schedule();
})();
