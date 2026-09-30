const Voice=(()=>{
 let rec=null;
 function supported(){return !!(window.SpeechRecognition||window.webkitSpeechRecognition)}
 function listen(onText,onState){
  if(!supported())return onState("Voice recognition is not supported in this browser.");
  const R=window.SpeechRecognition||window.webkitSpeechRecognition;rec=new R();rec.lang="en-AU";rec.interimResults=false;
  rec.onstart=()=>onState("Listening…");rec.onend=()=>onState("Ready");rec.onerror=e=>onState("Voice error: "+e.error);
  rec.onresult=e=>onText(e.results[0][0].transcript);rec.start();
 }
 function speak(text){if("speechSynthesis" in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(text))}}
 return {listen,speak,supported};
})();
