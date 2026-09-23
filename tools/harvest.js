// Run in the console of any https://www.lastepochtools.com/skills/<lang>/... page (after picking the
// language in the site's own selector). It opens every class and mastery skill of the page in turn and
// collects the rendered ability card; the result lands in window.__res as {abilityId: cardHtml}.
// Save it as cards/<lang>.json next to build.py, then run `python build.py` (see README).
(async function(){
  const A=window.LEAbilities.abilityList;
  const need=[...Object.keys(window.classSkillSources), ...Object.keys(window.masterySkillSources)];
  const links=[...document.querySelectorAll('a.section-item[section]')].filter(a=>!/\/tree$/.test(a.getAttribute('href')));
  const evadeSec={evade1:'acolyte_evade',evade2:'mage_evade',evade3:'primalist_evade',evade4:'rogue_evade',evade5:'sentinel_evade'};
  // the list links carry the ability icon, which is how a link is matched to an ability id
  const pairs=need.map(id=>{ let a; if(evadeSec[id]) a=links.find(l=>l.getAttribute('section')===evadeSec[id]); else { const spr=(A[id].abilitySprite||'').replace('a-r-',''); a=links.find(l=>l.querySelector('.icons-r-'+spr)); } return [id,a]; });
  const out={}, sleep=ms=>new Promise(r=>setTimeout(r,ms));
  for(const [id,a] of pairs){
    if(!a) continue;
    a.click();
    const t0=Date.now(); let ok=false;
    while(Date.now()-t0<6000){ await sleep(50); const n=document.querySelector('.ability-card .ability-name'); if(n && n.getAttribute('ability_id')===id){ok=true;break;} }
    if(!ok){ out[id]=null; continue; }
    await sleep(150);
    const c=document.querySelector('.ability-card').cloneNode(true);
    c.querySelectorAll('.diff-prefab.old-value, script').forEach(e=>e.remove());
    out[id]=c.innerHTML;
  }
  window.__res=out;
})();
