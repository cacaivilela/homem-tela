const CACHE='homem-tela-v21';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
// IA (MediaPipe + modelos, ~49 MB): cache próprio que não muda junto com o site, pra não baixar tudo de novo a cada versão.
// Só troca o nome se trocar a versão da biblioteca em lib/.
const LIB='homem-tela-lib-0.10.14';
const LIBFILES=['./lib/tasks-audio/audio_bundle.mjs','./lib/tasks-audio/wasm/audio_wasm_internal.js','./lib/tasks-audio/wasm/audio_wasm_internal.wasm','./lib/tasks-audio/wasm/audio_wasm_nosimd_internal.js','./lib/tasks-audio/wasm/audio_wasm_nosimd_internal.wasm',
 './lib/tasks-vision/vision_bundle.mjs','./lib/tasks-vision/wasm/vision_wasm_internal.js','./lib/tasks-vision/wasm/vision_wasm_internal.wasm','./lib/tasks-vision/wasm/vision_wasm_nosimd_internal.js','./lib/tasks-vision/wasm/vision_wasm_nosimd_internal.wasm',
 './lib/modelos/yamnet.tflite','./lib/modelos/hand_landmarker.task'];
// Baixa só o que ainda não está guardado; um arquivo que falhar não impede o resto (a página pede de novo toda vez que abre).
const guardaLib=()=>caches.open(LIB).then(c=>Promise.all(LIBFILES.map(u=>c.match(u).then(r=>r||c.add(u)).catch(()=>{}))));
// A instalação só espera o site (~60 KB); os 49 MB de IA vêm depois, quando a página pede, sem travar a troca de versão.
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!==LIB).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('message',e=>{if(e.data==='guardaLib')e.waitUntil(guardaLib());});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 if(new URL(e.request.url).pathname.includes('/lib/')){   // arquivos fixos: cache primeiro
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(r=>{if(r.ok){const cp=r.clone();caches.open(LIB).then(c=>c.put(e.request,cp));}return r;})));
  return;
 }
 // Site: abre na hora com o que está guardado e busca a versão nova por trás (aparece na próxima vez que abrir).
 // Internet lenta ou nenhuma não atrasa a abertura; sem nada guardado ainda, espera a rede.
 const rede=fetch(e.request).then(r=>{if(r.ok){const cp=r.clone();caches.open(CACHE).then(c=>c.put(e.request,cp));}return r;});
 e.waitUntil(rede.catch(()=>{}));
 e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||rede.catch(()=>caches.match('./index.html'))));
});
