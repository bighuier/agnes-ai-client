var g=document.getElementById('g0');
var item=document.createElement('div');
item.className='gallery-item';
var img=document.createElement('img');
img.src='/generated-images/05431e40.png';
img.onclick=function(){window.open(this.src)};
item.appendChild(img);
var btns=[
 {txt:'下载',right:'3px',bg:'',fn:'di',arg:'"/generated-images/05431e40.png"'},
 {txt:'图生图',right:'46px',bg:'#00b894',fn:'sendToGen',arg:'"/generated-images/05431e40.png",2'},
 {txt:'图生视频',right:'95px',bg:'#6c5ce7',fn:'sendToGen',arg:'"/generated-images/05431e40.png",4'}
];
btns.forEach(function(b){
 var btn=document.createElement('button');
 btn.className='dl-btn';
 btn.textContent=b.txt;
 btn.style.right=b.right;
 if(b.bg)btn.style.background=b.bg;
 btn.setAttribute('onclick',b.fn+'('+b.arg+')');
 item.appendChild(btn);
});
g.innerHTML='';
g.appendChild(item);
'inserted';
