(function(){
function showCatManager(){
    fetch('/api/categories').then(function(r){return r.json()}).then(function(cats){
        var ov=document.createElement('div');
        ov.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:1000;display:flex;align-items:center;justify-content:center';
        var box=document.createElement('div');
        box.style.cssText='background:#131722;border:1px solid #1e2233;border-radius:12px;padding:24px;max-width:500px;width:90%;max-height:80vh;overflow-y:auto;color:#e0e4ec;font-size:13px';
        var h='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><span style="font-size:16px;font-weight:600">分类管理</span><button id="_cmClose" style="background:none;border:none;color:#6b7394;font-size:20px;cursor:pointer">x</button></div>';
        h+='<div style="display:flex;gap:8px;margin-bottom:16px"><input id="_cmNewName" placeholder="新分类名称..." style="flex:1;background:#0b0d13;border:1px solid #252a40;border-radius:6px;padding:6px 10px;color:#e0e4ec;font-size:13px;outline:none"><button id="_cmAdd" style="background:#00b894;border:none;color:#fff;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px">新增</button></div>';
        h+='<div id="_cmList" style="display:flex;flex-direction:column;gap:6px">';
        var keys=Object.keys(cats);
        if(keys.length===0){
            h+='<div style="text-align:center;color:#6b7394;padding:20px">暂无分类</div>';
        }else{
            keys.forEach(function(k){
                h+='<div style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#0b0d13;border:1px solid #1e2233;border-radius:6px"><span style="flex:1;color:#e0e4ec">'+k+'</span><span style="color:#6b7394;font-size:12px">'+cats[k]+'条</span><button class="_cmRen" data-name="'+k+'" style="background:#252a40;border:none;color:#a29bfe;padding:3px 8px;border-radius:4px;cursor:pointer;font-size:11px">重命名</button><button class="_cmDel" data-name="'+k+'" style="background:#2e1410;border:none;color:#e17055;padding:3px 8px;border-radius:4px;cursor:pointer;font-size:11px">删除</button></div>';
            });
        }
        h+='</div>';
        box.innerHTML=h;ov.appendChild(box);document.body.appendChild(ov);
        document.getElementById('_cmClose').onclick=function(){ov.remove()};
        ov.onclick=function(e){if(e.target===ov)ov.remove()};
        document.getElementById('_cmAdd').onclick=function(){
            var n=document.getElementById('_cmNewName').value.trim();
            if(!n)return;
            fetch('/api/categories/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n})}).then(function(){ov.remove();showCatManager();if(window.pl)window.pl();if(window.loadCats)window.loadCats()});
        };
        box.querySelectorAll('._cmRen').forEach(function(btn){
            btn.onclick=function(){
                var old=btn.getAttribute('data-name');
                var n2=prompt('重命名 "'+old+'" 为:',old);
                if(n2&&n2.trim()&&n2.trim()!==old){
                    fetch('/api/categories/rename',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({old:old,new:n2.trim()})}).then(function(){ov.remove();showCatManager();if(window.pl)window.pl();if(window.loadCats)window.loadCats()});
                }
            };
        });
        box.querySelectorAll('._cmDel').forEach(function(btn){
            btn.onclick=function(){
                var name=btn.getAttribute('data-name');
                if(confirm('删除分类 "'+name+'"？该分类下的提示词将移至"其他"')){
                    fetch('/api/categories/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name})}).then(function(){ov.remove();showCatManager();if(window.pl)window.pl();if(window.loadCats)window.loadCats()});
                }
            };
        });
    });
}
setTimeout(function(){
    var s=document.querySelector('.srch');
    if(!s||document.getElementById('_cmb'))return;
    var b=document.createElement('button');
    b.id='_cmb';
    b.textContent='分类管理';
    b.style.cssText='background:#252a40;border:none;color:#e0e4ec;padding:4px 8px;border-radius:6px;cursor:pointer;font-size:11px;margin-left:4px;white-space:nowrap';
    b.onclick=showCatManager;
    s.appendChild(b);
},500);
window._loadCats=function(){
    var sel=document.getElementById('pc');
    if(!sel)return;
    fetch('/api/categories').then(function(r){return r.json()}).then(function(cats){
        sel.innerHTML='<option value="">全部分类</option>';
        for(var k in cats){sel.innerHTML+='<option value="'+k+'">'+k+'('+cats[k]+')</option>'}
    });
};
var _lc=window.loadCats;
window.loadCats=async function(){if(_lc)await _lc();if(window._loadCats)window._loadCats()};
})();
