function callSendToGen(url,targetTab){
    if(typeof sendToGen === 'function'){
        sendToGen(url,targetTab);
    }else{
        setTimeout(function(){callSendToGen(url,targetTab)},100);
    }
}
function createHistBtn(){
var btn=document.createElement("button");
btn.textContent="\u5386\u53f2";
btn.style.cssText="background:#252a40;border:none;color:#e0e4ec;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px;margin-left:auto";
btn.onclick=function(){
    var o=document.createElement("div");
    o.style.cssText="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:9999;display:flex;align-items:center;justify-content:center";
    o.onclick=function(){o.remove()};
    var c=document.createElement("div");
    c.style.cssText="background:#131722;border:1px solid #1e2233;border-radius:12px;padding:20px;max-width:700px;width:90%;max-height:80vh;overflow-y:auto;color:#e0e4ec;font-size:13px";
    c.onclick=function(e){e.stopPropagation()};
    var header=document.createElement("div");
    header.style.cssText="display:flex;justify-content:space-between;margin-bottom:12px";
    var titleSpan=document.createElement("span");
    titleSpan.style.cssText="font-size:16px;font-weight:600";
    titleSpan.textContent="\u751f\u6210\u5386\u53f2 ("+__hist.length+")";
    header.appendChild(titleSpan);
    var closeSpan=document.createElement("span");
    closeSpan.style.cssText="color:#6b7394;font-size:12px;cursor:pointer";
    closeSpan.textContent="\u2716 \u5173\u95ed";
    closeSpan.onclick=function(){o.remove()};
    header.appendChild(closeSpan);
    c.appendChild(header);
    if(__hist.length===0){
        var empty=document.createElement("div");
        empty.style.cssText="text-align:center;padding:20px;color:#6b7394";
        empty.textContent="\u6682\u65e0\u5386\u53f2";
        c.appendChild(empty);
    }
    for(var i=0;i<__hist.length&&i<50;i++){
        var url=__hist[i].url;
        var item=document.createElement("div");
        item.style.cssText="display:inline-block;width:calc(33% - 4px);margin:2px;position:relative";
        var img=document.createElement("img");
        img.src=url;
        img.style.cssText="width:100%;border-radius:4px;display:block;cursor:pointer";
        img.onclick=function(ev){zoomImg(ev.target.src)};
        item.appendChild(img);
        var btnDownload=document.createElement("button");
        btnDownload.textContent="\u4e0b\u8f7d";
        btnDownload.style.cssText="display:none;position:absolute;top:2px;right:3px;background:#252a40;color:#fff;border:none;padding:1px 4px;border-radius:2px;cursor:pointer;font-size:8px;white-space:nowrap;z-index:5";
        (function(u){btnDownload.onclick=function(e){e.stopPropagation();di(u)}})(url);
        item.appendChild(btnDownload);
        var btnImg2img=document.createElement("button");
        btnImg2img.textContent="\u56fe\u751f\u56fe";
        btnImg2img.style.cssText="display:none;position:absolute;top:2px;right:46px;background:#00b894;color:#fff;border:none;padding:1px 4px;border-radius:2px;cursor:pointer;font-size:8px;white-space:nowrap;z-index:5";
        (function(u){btnImg2img.onclick=function(e){e.stopPropagation();callSendToGen(u,2)}})(url);
        item.appendChild(btnImg2img);
        var btnImg2vid=document.createElement("button");
        btnImg2vid.textContent="\u56fe\u751f\u89c6\u9891";
        btnImg2vid.style.cssText="display:none;position:absolute;top:2px;right:95px;background:#6c5ce7;color:#fff;border:none;padding:1px 4px;border-radius:2px;cursor:pointer;font-size:8px;white-space:nowrap;z-index:5";
        (function(u){btnImg2vid.onclick=function(e){e.stopPropagation();callSendToGen(u,4)}})(url);
        item.appendChild(btnImg2vid);
        item.onmouseenter=function(){this.querySelectorAll("button").forEach(function(b){b.style.display="block"})};
        item.onmouseleave=function(){this.querySelectorAll("button").forEach(function(b){b.style.display="none"})};
        c.appendChild(item);
    }
    var clearDiv=document.createElement("div");
    clearDiv.style.cssText="margin-top:10px;text-align:center";
    var clearBtn=document.createElement("button");
    clearBtn.textContent="\u6e05\u7a7a\u5386\u53f2";
    clearBtn.style.cssText="background:#e17055;border:none;color:#fff;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px";
    clearBtn.onclick=function(){if(confirm("\u6e05\u7a7a\u6240\u6709\u5386\u53f2?")){localStorage.removeItem("img_history");window.__hist=[];o.remove()}};
    clearDiv.appendChild(clearBtn);
    c.appendChild(clearDiv);
    o.appendChild(c);
    document.body.appendChild(o);
};
return btn;
}
function addHistBtns(){
document.querySelectorAll(".card-title").forEach(function(title){
    if(title.querySelector("button[data-hist]"))return;
    var saveBtn=title.querySelector("button.btn-sm");
    if(!saveBtn)return;
    var btn=createHistBtn();
    btn.setAttribute("data-hist","1");
    saveBtn.parentNode.insertBefore(btn,saveBtn.nextSibling);
});
}
setTimeout(addHistBtns,500);
setTimeout(addHistBtns,2000);
