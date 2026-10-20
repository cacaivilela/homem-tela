const CACHE='homem-tela-v20';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
// IA (MediaPipe + modelos, ~49 MB): cache próprio que não muda junto com o site, pra não baixar tudo de novo a cada versão.
// Só troca o nome se trocar a versão da biblioteca em lib/.
const LIB='homem-tela-lib-0.10.14';
const LIBFILES=['./lib/tasks-audio/audio_bundle.mjs','./lib/tasks-audio/wasm/audio_wasm_internal.js','./lib/tasks-audio/wasm/audio_wasm_internal.wasm','./lib/tasks-audio/wasm/audio_wasm_nosimd_internal.js','./lib/tasks-audio/wasm/audio_wasm_nosimd_internal.wasm',
 './lib/tasks-vision/vision_bundle.mjs','./lib/tasks-vision/wasm/vision_wasm_internal.js','./lib/tasks-vision/wasm/vision_wasm_internal.wasm','./lib/tasks-vision/wasm/vision_wasm_nosimd_internal.js','./lib/tasks-vision/wasm/vision_wasm_nosimd_internal.wasm',
 './lib/modelos/yamnet.tflite','./lib/modelos/hand_landmarker.task'];
// Baixa só o que ainda não está guardado; um arquivo que falhar não impede o resto (tenta de novo na próxima instalação ou ao usar).
const guardaLib=()=>caches.open(LIB).then(c=>Promise.all(LIBFILES.map(u=>c.match(u).then(r=>r||c.add(u)).catch(()=>{}))));
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(guardaLib).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!==LIB).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 if(new URL(e.request.url).pathname.includes('/lib/')){   // arquivos fixos: cache primeiro
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(r=>{if(r.ok){const cp=r.clone();caches.open(LIB).then(c=>c.put(e.request,cp));}return r;})));
  return;
 }
 e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(CACHE).then(c=>c.put(e.request,cp));return r;}).catch(()=>caches.match(e.request).then(r=>r||caches.match('./index.html'))));
});
