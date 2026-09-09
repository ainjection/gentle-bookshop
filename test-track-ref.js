function run(search, referrer, store){
  const ENDPOINT='https://x/rest/v1/events';
  let ref='';
  try{
    const q=new URLSearchParams(search);
    let src=q.get('src')||q.get('utm_source');
    if(src){store.gb_src=src;} else {src=store.gb_src??null;}
    ref=src||(referrer?new URL(referrer).host:'');
  }catch(e){ref='THREW:'+e.message;}
  return ref;
}
const cases=[
 ['?src=youtube','',{}, 'youtube'],
 ['','https://t.co/abc',{}, 't.co'],
 ['','https://www.pinterest.com/x',{}, 'www.pinterest.com'],
 ['','',{gb_src:'tiktok'}, 'tiktok'],
 ['?utm_source=pinterest','',{}, 'pinterest'],
 ['','',{}, ''],
];
let bad=0;
for(const [s,r,st,want] of cases){
  const got=run(s,r,st);
  if(got!==want)bad++;
  console.log(got===want?'ok  ':'FAIL', JSON.stringify({search:s,ref:r,sess:st.gb_src||null}),'->',JSON.stringify(got));
}
console.log(bad?bad+' FAILED':'all passed');
