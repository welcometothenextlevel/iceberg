(function(){
'use strict';
var $=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return[].slice.call((c||document).querySelectorAll(s))};
var root=document.documentElement,reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
/* header + sticky */
var top=$('.top'),side=$('.side');
function onS(){var y=scrollY,d=$('.dive'),lim=d?(reduce?innerHeight*.5:d.offsetHeight-innerHeight*1.02):60;top.classList.toggle('solid',y>lim);}
addEventListener('scroll',onS,{passive:true});onS();
/* menu */
var menu=$('#menu'),bg=$('.burger');
function mset(o){menu.classList.toggle('on',o);menu.inert=!o;bg.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':'';if(o)$('.menu-x').focus();else bg.focus({preventScroll:true});}
bg.onclick=function(){mset(true)};$('.menu-x').onclick=function(){mset(false)};$$('a',menu).forEach(function(a){a.addEventListener('click',function(){if(menu.classList.contains('on'))mset(false)})});
/* live status, Swiss time */
(function(){try{var p={};new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Zurich',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()).forEach(function(x){p[x.type]=x.value});
 var m=+p.hour%24*60+ +p.minute,d=p.weekday,end=d==='Fri'?990:1080,t='Dépannage 24h/24';
 if(!/Sat|Sun/.test(d)){if(m>=450&&m<720)t='Ouvert jusqu’à 12h00';else if(m>=810&&m<end)t='Ouvert jusqu’à '+(end===990?'16h30':'18h00');else if(m>=720&&m<810)t='Réouverture à 13h30';}
 $$('[data-status]').forEach(function(e){e.textContent=t});}catch(e){}
 $$('[data-year]').forEach(function(e){e.textContent=new Date().getFullYear()});})();
/* whatsapp */
var wa=$('#wa'),box=$('.wa-box'),fab=$('.wa-fab');
function wset(o){wa.classList.toggle('open',o);box.inert=!o;fab.setAttribute('aria-expanded',o);if(!o)fab.focus({preventScroll:true})}
fab.onclick=function(){wset(!wa.classList.contains('open'))};$('.wa-h button').onclick=function(){wset(false)};
addEventListener('keydown',function(e){if(e.key!=='Escape')return;if(wa.classList.contains('open'))wset(false);if(menu.classList.contains('on'))mset(false)});
document.addEventListener('click',function(e){if(wa.classList.contains('open')&&!wa.contains(e.target))wset(false)});
/* hide sticky bar while typing */
document.addEventListener('focusin',function(e){if(/INPUT|TEXTAREA/.test(e.target.tagName)&&!/radio|range/.test(e.target.type))root.classList.add('kb')});document.addEventListener('focusout',function(){root.classList.remove('kb')});
/* lazy videos */
if('IntersectionObserver'in window){var vo=new IntersectionObserver(function(es){es.forEach(function(x){var v=x.target;if(x.isIntersecting){if(!v.src)v.src=v.dataset.src;if(!reduce)v.play().catch(function(){})}else if(v.src)v.pause()})},{rootMargin:'150px'});$$('video[data-src]').forEach(function(v){v.muted=true;vo.observe(v)})}
/* thermostat */
var th=$('.th');
if(th){var S=[['+23','Confort',23],['+20','Locaux informatiques',20],['+12','Cave à vin',12],['+3','Chambre froide',3],['−20','Congélation',-20]];
 var r=$('#thr'),num=$('#thn'),cur=0,tr=$('.th-tr'),raf;
 function paint(v){var k=v/25,a=Math.min(3,Math.floor(k)),f=k-a,t=S[a][2]+(S[a+1][2]-S[a][2])*f,n=Math.round(t);
  num.textContent=(n>0?'+':n<0?'−':'')+Math.abs(n);tr.style.setProperty('--v',v/100);
  th.style.setProperty('--warm',Math.max(0,.55-v/100*1.1).toFixed(3));th.style.setProperty('--fr',Math.max(0,Math.min(1,(v-55)/45)).toFixed(3));
  var i=Math.round(k);if(i!==cur){cur=i;['.th-bg','.th-card','.th-marks button'].forEach(function(s){$$(s,th).forEach(function(e,j){e.classList.toggle('on',j===i);if(s==='.th-card')e.inert=j!==i})})}
  r.setAttribute('aria-valuetext',S[i][0]+' °C, '+S[i][1]);}
 function go(v,ms){cancelAnimationFrame(raf);var s=+r.value,t0;if(reduce){r.value=v;paint(v);return}raf=requestAnimationFrame(function st(t){t0=t0||t;var p=Math.min(1,(t-t0)/(ms||800)),e=1-Math.pow(1-p,3);r.value=s+(v-s)*e;paint(s+(v-s)*e);if(p<1)raf=requestAnimationFrame(st)});}
 function touch(){th.classList.add('touched')}
 r.addEventListener('input',function(){touch();cancelAnimationFrame(raf);paint(+r.value)});r.addEventListener('change',function(){go(Math.round(+r.value/25)*25,350)});
 r.addEventListener('keydown',function(e){var d={ArrowRight:1,ArrowDown:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(d){e.preventDefault();touch();go(Math.max(0,Math.min(4,cur+d))*25,500)}});
 $$('.th-marks button').forEach(function(b){b.onclick=function(){touch();go(b.dataset.i*25)}});
 paint(0);
 /* gentle hint: cools down once when it first comes into view */
 if('IntersectionObserver'in window&&!reduce){var ho=new IntersectionObserver(function(e){if(e[0].isIntersecting){ho.disconnect();setTimeout(function(){if(!th.classList.contains('touched'))go(50,2200)},900)}},{threshold:.6});ho.observe(th)}
 window.__th=go;}
/* lightbox */
var lb=$('.lb');
if(lb){var P=JSON.parse($('#posts').textContent),pi=0,ii=0,M=$('.lb-m'),opener;
 function show(){var p=P[pi],n=p.imgs?p.imgs.length:1;M.innerHTML='';
  if(p.kind==='reel'){var v=document.createElement('video');v.src='assets/video/'+p.src+'.mp4';v.poster='assets/img/'+p.poster+'.webp';v.controls=v.playsInline=v.loop=v.muted=true;M.appendChild(v);v.play().catch(function(){})}
  else{var g=new Image();g.src='assets/img/'+p.imgs[ii]+'.webp';g.alt=p.cap+' ('+(ii+1)+'/'+n+')';M.appendChild(g)}
  $('.lb-prev').hidden=$('.lb-next').hidden=n<2;$('.lb-dots').innerHTML=n>1?p.imgs.map(function(_,j){return'<i'+(j===ii?' class="on"':'')+'></i>'}).join(''):'';
  $('.lb-cap').textContent=p.cap;$('.lb-d').textContent='Publié le '+p.date;$('.lb-l').href='https://www.instagram.com/p/'+p.id+'/';}
 function step(d){var n=(P[pi].imgs||[1]).length;if(n<2)return;ii=(ii+d+n)%n;show()}
 $$('[data-post]').forEach(function(b){b.addEventListener('click',function(){opener=b;pi=+b.dataset.post;ii=0;show();lb.showModal();document.body.style.overflow='hidden'})});
 lb.addEventListener('close',function(){M.innerHTML='';document.body.style.overflow='';if(opener)opener.focus({preventScroll:true})});
 $('.lb-x').onclick=function(){lb.close()};$('.lb-prev').onclick=function(){step(-1)};$('.lb-next').onclick=function(){step(1)};$('[data-lbclose]').addEventListener('click',function(){opener=null;lb.close()});
 lb.addEventListener('click',function(e){if(e.target===lb)lb.close()});lb.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')step(-1);if(e.key==='ArrowRight')step(1);if(e.key==='Escape')lb.close()});
 var sx;M.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});M.addEventListener('touchend',function(e){var d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>45)step(d<0?1:-1)});}
/* wizard */
var wz=$('#wiz');
if(wz){var st=$$('.st',wz),c=0,er=$('.err',wz),nx=$('.next',wz),bk=$('.back',wz);
 function wsh(f){st.forEach(function(s,i){s.classList.toggle('on',i===c)});$('.wiz-p i').style.width=(c+1)*25+'%';bk.hidden=c===0;nx.hidden=c===3;nx.style.display=c===3?'none':'';er.hidden=true;if(f){var y=wz.getBoundingClientRect().top;if(y<80||y>innerHeight*.5)scrollTo({top:scrollY+y-100,behavior:'smooth'});}}
 function ok(){var s=st[c],m='';var names={};$$('input[type=radio]',s).forEach(function(x){names[x.name]=names[x.name]||x.checked});for(var n in names)if(!names[n])m='Choisissez une réponse pour continuer.';
  $$('input[required]:not([type=radio])',s).forEach(function(x){if(!x.value.trim())m='Complétez le champ « '+x.name+' ».';else if(x.type==='tel'&&x.value.replace(/\D/g,'').length<9)m='Vérifiez le numéro de téléphone.'});
  er.textContent=m;er.hidden=!m;return!m}
 nx.onclick=function(){if(ok()){c++;wsh(true)}};bk.onclick=function(){c--;wsh(true)};
 wz.addEventListener('submit',function(e){e.preventDefault();if(c<3)nx.click()});
 var ptr=false;wz.addEventListener('pointerdown',function(){ptr=true});wz.addEventListener('keydown',function(){ptr=false});
 wz.addEventListener('change',function(e){if(e.target.type==='radio'&&c<2&&ptr)setTimeout(function(){if(ok()){c++;wsh(true)}},280)});
 $$('[data-send]',wz).forEach(function(b){b.onclick=function(){if(!ok())return;var d=new FormData(wz),l=['Bonjour Iceberg, je souhaite un devis.',''];d.forEach(function(v,k){if(String(v).trim())l.push(k+' : '+v)});var t=l.join('\n');
  if(b.dataset.send==='wa')window.open('https://wa.me/41797261111?text='+encodeURIComponent(t),'_blank','noopener');else location.href='mailto:info@iceberg-sarl.ch?subject='+encodeURIComponent('Demande de devis, '+(d.get('Besoin')||''))+'&body='+encodeURIComponent(t);}});
 $$('[data-besoin]').forEach(function(a){a.addEventListener('click',function(){var x=$$('input[name=Besoin]',wz).filter(function(i){return i.value===a.dataset.besoin})[0];if(x){x.checked=true;c=1;wsh()}})});
 $$('[data-devis]').forEach(function(a){a.addEventListener('click',function(e){var t=$('#devis');if(t&&/#devis$/.test(a.getAttribute('href'))){e.preventDefault();t.scrollIntoView({behavior:reduce?'auto':'smooth'})}})});
 wsh();
 if('IntersectionObserver'in window)new IntersectionObserver(function(e){side.classList.toggle('hid',e[0].isIntersecting)},{threshold:.15}).observe($('#devis'));}
/* motion */
if(reduce||!window.gsap){root.classList.add('still');return}
gsap.registerPlugin(ScrollTrigger);ScrollTrigger.config({ignoreMobileResize:true});
var dive=$('.dive');
if(dive){
 var im=$('.dive-img'),stg=$('.dive-st');
 var tl=gsap.timeline({scrollTrigger:{trigger:dive,start:'top top',end:'bottom bottom',scrub:.6,invalidateOnRefresh:true}});
 tl.to(im,{y:function(){return-(im.offsetTop+im.offsetHeight*.726-innerHeight*(innerWidth<=800?.36:.47))},scale:1.14,ease:'power1.inOut',duration:1},0)
 .to('.dive-a',{y:-90,autoAlpha:0,duration:.24,ease:'none'},.06)
 .to('.dive-sh',{opacity:0,duration:.3,ease:'none'},.12)
 .fromTo('.dive-b',{autoAlpha:0,y:80},{autoAlpha:1,y:0,duration:.26,ease:'power2.out'},.5)
 .fromTo('.dive-b li',{opacity:0,y:40},{opacity:1,y:0,stagger:.05,duration:.18},.56)
 .to('.dive-d em',{top:100,duration:1,ease:'none'},0);
 /* particles: plankton under water, snow above */
 var cv=$('.dive-c'),x=cv.getContext('2d'),pt=[],W,H,vis=true,dp=Math.min(devicePixelRatio,1.5);
 function rs(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dp;cv.height=H*dp;x.setTransform(dp,0,0,dp,0,0);pt=[];var n=innerWidth<800?34:80;while(n--)pt.push([Math.random()*W,Math.random()*H,Math.random()*1.8+.5,Math.random()*6.3,Math.random()*.4+.15])}
 rs();addEventListener('resize',rs);ScrollTrigger.create({trigger:dive,start:'top bottom',end:'bottom top',onToggle:function(s){vis=s.isActive}});
 var last=scrollY;(function dr(t){requestAnimationFrame(dr);if(!vis)return;var dy=scrollY-last;last=scrollY;var u=tl.scrollTrigger?tl.progress():0,dir=u<.35?.5:-.35;x.clearRect(0,0,W,H);x.fillStyle='#e6f6ff';
  pt.forEach(function(p){p[1]+=dir*p[4]*1.6-dy*.04*p[2];p[0]+=Math.sin(t/1600+p[3])*.25;if(p[1]>H+5)p[1]=-5;if(p[1]<-5)p[1]=H+5;x.globalAlpha=(.25+.35*Math.sin(t/900+p[3])*.5+.2)*(u<.35?.8:.65);x.beginPath();x.arc(p[0],p[1],p[2],0,6.3);x.fill()})})(0);
 gsap.from('.dive-a>*',{y:34,opacity:0,duration:1,stagger:.11,ease:'power3.out',delay:.1});
}
/* cave: pinned, three columns moving against each other */
var mm=gsap.matchMedia();
mm.add('(min-width:901px)',function(){if(!$('.cave'))return;
 var t=gsap.timeline({scrollTrigger:{trigger:'.cave',start:'top top',end:'+=130%',pin:true,scrub:.6,anticipatePin:1}});
 t.fromTo('.cg-1',{y:60},{y:function(){return-innerHeight*.3},ease:'none'},0).fromTo('.cg-2',{y:0},{y:function(){return-innerHeight*.34},ease:'none'},0).fromTo('.cg-3',{y:-60},{y:function(){return innerHeight*.1},ease:'none'},0);});
$$('[data-count]').forEach(function(e){var o={v:e.dataset.count==='12'?24:40};gsap.to(o,{v:+e.dataset.count,duration:2,ease:'power2.out',onUpdate:function(){e.textContent=Math.round(o.v)},scrollTrigger:{trigger:e,start:'top 92%'}})});
$$('[data-r]').forEach(function(e){gsap.from(e,{y:44,opacity:0,duration:1,ease:'power3.out',scrollTrigger:{trigger:e,start:'top 88%'}})});
if($('.ref-m'))gsap.fromTo('.ref-m img',{yPercent:-13},{yPercent:0,ease:'none',scrollTrigger:{trigger:'.ref-m',start:'top bottom',end:'bottom top',scrub:true}});
if($('.sh-m'))gsap.fromTo('.sh-m img',{yPercent:0},{yPercent:-10,ease:'none',scrollTrigger:{trigger:'.sh',start:'top top',end:'bottom top',scrub:true}});
$$('.free-g i').forEach(function(e){gsap.from(e,{scaleX:.02,duration:1.5,ease:'power3.inOut',scrollTrigger:{trigger:e,start:'top 88%'}})});
gsap.from('.tile',{y:70,opacity:0,duration:.9,stagger:.09,ease:'power3.out',scrollTrigger:{trigger:'.tiles',start:'top 85%'}});
if($('.urg-v')){gsap.from('.urg-v img:first-child',{x:220,opacity:0,duration:1.2,ease:'power3.out',scrollTrigger:{trigger:'.urg-v',start:'top 80%'}});gsap.from('.urg-v img:last-child',{x:-200,opacity:0,duration:1.2,delay:.15,ease:'power3.out',scrollTrigger:{trigger:'.urg-v',start:'top 80%'}})}
gsap.from('.brands li',{opacity:0,duration:.6,stagger:.04,scrollTrigger:{trigger:'.brands ul',start:'top 88%'}});
addEventListener('load',function(){ScrollTrigger.refresh()});
})();
