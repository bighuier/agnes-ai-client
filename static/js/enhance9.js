(function(){
async function urlToDataURL(url){
    var r=await fetch(url);
    var b=await r.blob();
    return new Promise(function(res,rej){
        var fr=new FileReader();
        fr.onload=function(){res(fr.result)};
        fr.onerror=function(){rej(fr.error)};
        fr.readAsDataURL(b);
    });
}
function renderUploadPreview(t,dataURL){
    var uploadZone=document.getElementById("u"+t);
    if(!uploadZone)return;
    var hint=uploadZone.querySelector(".hint");
    uploadZone.style.position="relative";
    uploadZone.querySelectorAll(".pv,.rm,.num").forEach(function(e){e.remove()});
    if(hint)hint.textContent="已选1张,点此重选";
    var wrap=document.createElement("div");
    wrap.className="pv";
    wrap.style.cssText="display:inline-block;position:relative;width:calc(50%-4px);margin:2px;vertical-align:top";
    var im=document.createElement("img");
    im.src=dataURL;
    im.style.cssText="width:100%;border-radius:4px;display:block";
    var num=document.createElement("span");
    num.className="num";
    num.textContent="1";
    num.style.cssText="position:absolute;top:2px;left:2px;background:#6c5ce7;color:#fff;padding:1px 5px;border-radius:3px;font-size:10px;z-index:5";
    var del=document.createElement("button");
    del.className="rm";
    del.textContent="×";
    del.style.cssText="position:absolute;top:2px;right:2px;background:#e17055;color:#fff;border:none;border-radius:50%;width:18px;height:18px;cursor:pointer;font-size:11px;z-index:5;line-height:18px;text-align:center";
    del.onclick=function(e){
        e.stopPropagation();
        up[t]=[];
        wrap.remove();
        if(hint){hint.textContent="点击上传";hint.style.display="block"}
    };
    wrap.appendChild(num);
    wrap.appendChild(del);
    wrap.appendChild(im);
    uploadZone.insertBefore(wrap,hint);
    var tmpImg=new Image();
    tmpImg.onload=function(){
        var wi=document.getElementById("w"+t);
        var hi=document.getElementById("h"+t);
        if(wi)wi.value=tmpImg.naturalWidth;
        if(hi)hi.value=tmpImg.naturalHeight;
    };
    tmpImg.src=dataURL;
}
window.sendToGen=async function(url,targetTab){
    var t=targetTab===2?1:3;
    try{
        var dataURL=await urlToDataURL(url);
        up[t]=[dataURL];
        renderUploadPreview(t,dataURL);
        sw(targetTab===2?2:4);
        window.st("s"+t,"已载入图片，输入提示词后点击生成","info");
    }catch(e){
        alert("载入图片失败: "+e.message);
    }
};
})();
