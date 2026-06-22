(function(){
var VOCAB={
style:['写实','超写实','电影感','赛博朋克','蒸汽朋克','极简主义','复古','怀旧','日系清新','暗黑哥特','梦幻','水彩','油画','素描','漫画','动漫','波普艺术','低多边形','等距视角','像素风','胶片感','黑白','双重曝光','HDR','纪实','时尚','商业','艺术摄影','LOMO','移轴','红外摄影','霓虹','蒸汽波','故障艺术','极简','极繁','印象派','超现实主义','未来主义','国风','水墨','浮世绘','新艺术运动','极光风格','暗调风格','高调风格'],
focal_length:['14mm超广角','16mm超广角','24mm广角','28mm广角','35mm人文','50mm标准','50mm定焦','85mm人像','100mm微距','135mm中长焦','200mm长焦','300mm超长焦','400mm超长焦','600mm超长焦','鱼眼','移轴镜头'],
aperture:['f/1.2大光圈','f/1.4大光圈','f/1.8大光圈','f/2.0大光圈','f/2.8','f/4.0','f/5.6','f/8.0','f/11','f/16小光圈','f/22小光圈'],
lighting:['自然光','逆光','侧光','顶光','底光','顺光','散射光','硬光','柔光','伦勃朗光','蝴蝶光','环形光','分割光','边缘光','轮廓光','发丝光','烛光','霓虹灯光','金色时刻','蓝色时刻','正午阳光','阴天光线','暖光','冷光','混合光','频闪','闪光灯','持续光','光绘','丁达尔效应','体积光','剪影光','窗光','反光板补光','柔光箱','蜂巢光','聚光灯','追光灯'],
composition:['三分法','黄金分割','中心构图','对称构图','对角线构图','引导线构图','框架构图','三角形构图','S形构图','L形构图','圆形构图','留白构图','极简构图','重复构图','前景构图','层次构图','透视构图','倒影构图','负空间构图','满幅构图','纵深构图','放射线构图','交叉构图','封闭式构图','开放式构图'],
perspective:['平视','俯视','仰视','鸟瞰','虫眼视角','45度角','正面','侧面','背面','3/4侧面','过肩视角','第一人称','第三人称','微距视角','全景视角','荷兰角','低角度','高角度','倾斜视角','纵深视角'],
color_tone:['暖色调','冷色调','高饱和','低饱和','莫兰迪色','黑白','单色','双色调','复古色调','胶片色调','日系色调','电影色调','赛博朋克色调','橙青色调','粉彩色调','大地色系','金属色调','渐变色','对比色','互补色','同类色','暗调','亮调','中间调','高调','低调','青橙色调','红蓝色调','紫金色调','去饱和','过饱和','交叉冲洗色调'],
quality_style:['8K','4K','高清','超高清','细节丰富','锐利','柔焦','颗粒感','胶片颗粒','噪点','光晕','镜头光晕','景深','浅景深','深景深','散景','焦外虚化','色差','暗角','宽容度','动态范围','RAW质感','超精细','高解析','丝滑','油画质感','磨砂质感','玻璃质感','金属质感'],
shot_type:['远景','全景','中景','近景','特写','大特写','极远景','中近景','半身景','全身景','头肩景','脸部特写','眼睛特写','手部特写','脚部特写','群像景','环境人像','过膝景','腰部景','胸部景'],
camera_movement:['推镜头','拉镜头','摇镜头','移镜头','跟镜头','升镜头','降镜头','环绕运镜','航拍','手持运镜','斯坦尼康','滑轨','升降机','甩镜头','旋转运镜','变焦推拉','慢速运镜','快速运镜','静止镜头','第一人称运镜','穿越运镜','弧形运镜','对角线运镜','钟摆运镜'],
transition:['硬切','淡入淡出','叠化','划变','缩放切换','模糊切换','黑场过渡','白场过渡','匹配剪辑','跳切','L切','J切','蒙太奇','闪回','闪前','平行剪辑','交叉剪辑','动作接动作','视线匹配','图形匹配','声音先入','画面先入'],
focus_technique:['浅景深','深景深','移焦','跟焦','拉焦','手动对焦','自动对焦','焦点锁定','焦外虚化','散景效果','柔焦','微距对焦','裂像对焦','峰值对焦','焦点转移','焦点呼吸','超焦距'],
character_action:['站立','坐姿','行走','奔跑','跳跃','转身','回眸','低头','抬头','侧身','背影','伸展','蹲下','靠墙','依窗','撑伞','阅读','喝咖啡','弹奏乐器','舞蹈','冥想','瑜伽','攀爬','骑行','挥手','拥抱','思考','凝视远方','整理头发','托腮','双手交叉','插兜','扶帽','吹风','淋雨','拾花','提裙','仰望天空','俯瞰大地','侧卧','跪坐','斜靠'],
character_expression:['微笑','大笑','冷漠','悲伤','惊讶','愤怒','思考','沉思','害羞','期待','自信','忧郁','眺望远方','闭眼','咬唇','歪头','撅嘴','皱眉','眯眼','凝视','回眸一笑','侧脸','正脸','仰头','低头','侧目','含泪','窃笑','苦笑','假笑','释然','坚定','迷茫','惊喜','不屑','傲慢','温柔','宠溺','警惕','安详'],
mood_atmosphere:['宁静','温暖','浪漫','神秘','紧张','欢快','忧郁','孤独','热闹','壮观','梦幻','恐怖','怀旧','清新','压抑','自由','优雅','粗犷','纯真','成熟','慵懒','活力','沉稳','空灵','史诗感','末日感','仙境','童话','暗黑','禅意','治愈','沉浸感','荒诞','讽刺','庄严','肃穆','狂欢','静谧','苍凉','繁华','荒芜','生机','凋零'],
tags:['人像','风景','街拍','建筑','美食','产品','动物','植物','夜景','日出','日落','逆光','剪影','特写','全景','黑白','彩色','胶片','数码','自然','城市','乡村','海边','雪山','森林','沙漠','雨天','雾天','雪景','秋色','春花','夏日','冬景','室内','室外','工作室','旅行','纪实','创意','抽象','微距','长曝光','星空','银河','极光','烟花','水面','倒影','光影','纹理','极简','复古','现代','古典','东方','西方','民族','节日','婚礼','亲子','宠物','运动','音乐','舞蹈','时尚','商业','新闻','航拍','水下','延时','慢动作','快节奏','静物','花卉','昆虫','鸟类','野生动物','街头','地铁','校园','医院','工厂','废墟','古迹','教堂','寺庙','桥梁','塔楼','广场','市场','酒吧','咖啡馆','图书馆','博物馆']
};
var PM_NAMES={style:'风格描述',focal_length:'焦距',aperture:'光圈',lighting:'光线',composition:'构图',perspective:'视角',color_tone:'色调',quality_style:'画质风格',shot_type:'景别',camera_movement:'运镜',transition:'镜头切换',focus_technique:'焦点技巧',character_action:'人物动作',character_expression:'人物表情',mood_atmosphere:'情绪氛围',tags:'标签'};
var _currentPicker=null;
var _vocabStore={};
var _tabMap={0:'gen_0',1:'gen_1',2:'gen_2',3:'gen_3'};
function showVocabPicker(inputEl,fieldKey,storeKey){
    if(_currentPicker)_currentPicker.remove();
    var terms=VOCAB[fieldKey]||[];
    if(!terms.length)return;
    var key=storeKey||getVocabKey(inputEl.id);
    if(!_vocabStore[key])_vocabStore[key]={};
    var selectedTerms=_vocabStore[key][fieldKey]||[];
    var picker=document.createElement('div');
    _currentPicker=picker;
    picker.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:10001;display:flex;align-items:center;justify-content:center;padding:20px';
    var box=document.createElement('div');
    box.style.cssText='background:#131722;border:1px solid #1e2233;border-radius:12px;padding:20px;max-width:750px;width:95%;max-height:85vh;display:flex;flex-direction:column;color:#e0e4ec;font-size:13px';
    box.onclick=function(e){e.stopPropagation()};
    var headerHtml='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px"><span style="font-size:16px;font-weight:600">专业词汇选择</span><button id="_vpClose" style="background:none;border:none;color:#6b7394;font-size:20px;cursor:pointer">x</button></div>';
    var searchHtml='<div style="margin-bottom:12px"><input id="_vpSearch" placeholder="搜索词汇..." style="width:100%;background:#0b0d13;border:1px solid #252a40;border-radius:6px;padding:7px 10px;color:#e0e4ec;font-size:13px;outline:none;box-sizing:border-box"></div>';
    var catFilterHtml='<div id="_vpCatFilter" style="display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap"></div>';
    var listHtml='<div id="_vpList" style="flex:1;overflow-y:auto;display:flex;flex-wrap:wrap;gap:6px;align-content:flex-start;padding:4px 0"></div>';
    var summaryHtml='<div id="_vpSummary" style="margin-top:12px;padding:10px;background:#0b0d13;border:1px solid #1e2233;border-radius:6px;font-size:12px;color:#8b95b5;max-height:120px;overflow-y:auto;white-space:pre-wrap;line-height:1.6"></div>';
    var footerHtml='<div style="margin-top:14px;display:flex;gap:8px;justify-content:flex-end"><button id="_vpClear" style="background:#2e1410;border:1px solid #3d1f18;color:#e17055;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px">清空选择</button><button id="_vpCancel" style="background:#252a40;border:none;color:#e0e4ec;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px">取消</button><button id="_vpApply" style="background:#00b894;border:none;color:#fff;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:12px">应用到输入框</button></div>';
    box.innerHTML=headerHtml+searchHtml+catFilterHtml+listHtml+summaryHtml+footerHtml;
    picker.appendChild(box);
    document.body.appendChild(picker);
    var allSelected={};
    function syncAll(){
        allSelected={};
        var summaryParts=[];
        for(var k in _vocabStore[key]){
            var arr=_vocabStore[key][k]||[];
            allSelected[k]=arr;
            if(arr.length){
                summaryParts.push(PM_NAMES[k]+': '+arr.join(', '));
            }
        }
        var summaryEl=document.getElementById('_vpSummary');
        if(summaryEl)summaryEl.innerHTML=summaryParts.join('\n')||'暂未选择任何词汇';
    }
    syncAll();
    var cats=['style','focal_length','aperture','lighting','composition','perspective','color_tone','quality_style','shot_type','camera_movement','transition','focus_technique','character_action','character_expression','mood_atmosphere','tags'];
    var catNames={style:'风格',focal_length:'焦距',aperture:'光圈',lighting:'光线',composition:'构图',perspective:'视角',color_tone:'色调',quality_style:'画质',shot_type:'景别',camera_movement:'运镜',transition:'切换',focus_technique:'焦点',character_action:'动作',character_expression:'表情',mood_atmosphere:'氛围',tags:'标签'};
    var cfEl=document.getElementById('_vpCatFilter');
    if(cfEl){
        var allBtn=document.createElement('button');
        allBtn.className='_vpCatBtn';
        allBtn.textContent='全部';
        allBtn.style.cssText='background:#6c5ce7;color:#fff;border:none;padding:4px 12px;border-radius:6px;font-size:11px;cursor:pointer';
        allBtn.dataset.cat='';
        cfEl.appendChild(allBtn);
        cats.forEach(function(c){
            var btn=document.createElement('button');
            btn.className='_vpCatBtn';
            btn.textContent=catNames[c]||c;
            btn.style.cssText='background:#252a40;color:#8b95b5;border:none;padding:4px 12px;border-radius:6px;font-size:11px;cursor:pointer';
            btn.dataset.cat=c;
            cfEl.appendChild(btn);
        });
        cfEl.querySelectorAll('._vpCatBtn').forEach(function(btn){
            btn.onclick=function(){
                cfEl.querySelectorAll('._vpCatBtn').forEach(function(b){b.style.background='#252a40';b.style.color='#8b95b5'});
                this.style.background='#6c5ce7';this.style.color='#fff';
                renderTerms(this.dataset.cat,'');
            };
        });
    }
    function renderTerms(catFilter,searchFilter){
        var list=document.getElementById('_vpList');
        if(!list)return;
        var html='';
        var fl=searchFilter?searchFilter.toLowerCase():'';
        cats.forEach(function(fieldKey){
            if(catFilter&&catFilter!==fieldKey)return;
            var terms=VOCAB[fieldKey]||[];
            if(!terms.length)return;
            html+='<div style="width:100%;margin-bottom:4px"><span style="font-size:11px;color:#6c5ce7;font-weight:600">'+(catNames[fieldKey]||fieldKey)+'</span></div>';
            terms.forEach(function(term){
                if(fl&&term.toLowerCase().indexOf(fl)===-1)return;
                var isSelected=allSelected[fieldKey]&&allSelected[fieldKey].indexOf(term)!==-1;
                html+='<div class="_vpTerm" data-field="'+fieldKey+'" data-term="'+term+'" style="display:inline-flex;align-items:center;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:11px;user-select:none;transition:all .15s;'+
                (isSelected?'background:#6c5ce7;color:#fff;box-shadow:0 0 8px rgba(108,92,231,.3)':'background:#1e2233;color:#8b95b5;border:1px solid #2d3250')+'">'+term+'</div>';
            });
        });
        if(!html)html='<div style="color:#6b7394;text-align:center;width:100%;padding:16px">无匹配词汇</div>';
        list.innerHTML=html;
        list.querySelectorAll('._vpTerm').forEach(function(el){
            el.onmouseenter=function(){if(!el.style.background.includes('#6c5ce7'))el.style.opacity='0.7'};
            el.onmouseleave=function(){el.style.opacity='1'};
            el.onclick=function(){
                var f=el.getAttribute('data-field');
                var t=el.getAttribute('data-term');
                if(!allSelected[f])allSelected[f]=[];
                var idx=allSelected[f].indexOf(t);
                if(idx!==-1){
                    allSelected[f].splice(idx,1);
                    el.style.background='#1e2233';el.style.color='#8b95b5';el.style.borderColor='#2d3250';
                }else{
                    allSelected[f].push(t);
                    el.style.background='#6c5ce7';el.style.color='#fff';el.style.boxShadow='0 0 8px rgba(108,92,231,.3)';
                }
                _vocabStore[key][f]=allSelected[f].slice();
                syncAll();
            };
        });
    }
    renderTerms('','');
    var searchEl=document.getElementById('_vpSearch');
    if(searchEl)searchEl.oninput=function(){renderTerms('',this.value.trim())};
    var closeEl=document.getElementById('_vpClose');
    if(closeEl)closeEl.onclick=function(){picker.remove();_currentPicker=null};
    picker.onclick=function(){picker.remove();_currentPicker=null};
    var cancelEl=document.getElementById('_vpCancel');
    if(cancelEl)cancelEl.onclick=function(){picker.remove();_currentPicker=null};
    var clearEl=document.getElementById('_vpClear');
    if(clearEl)clearEl.onclick=function(){
        cats.forEach(function(c){
            if(allSelected[c])allSelected[c]=[];
            if(_vocabStore[key])_vocabStore[key][c]=[];
        });
        syncAll();
        document.querySelectorAll('._vpTerm').forEach(function(el){
            el.style.background='#1e2233';
            el.style.color='#8b95b5';
            el.style.borderColor='#2d3250';
            el.style.boxShadow='none';
        });
    };
    var applyEl=document.getElementById('_vpApply');
    if(applyEl)applyEl.onclick=function(){
        var summaryParts=[];
        for(var k in allSelected){
            if(allSelected[k]&&allSelected[k].length){
                summaryParts.push(PM_NAMES[k]+': '+allSelected[k].join(', '));
            }
        }
        if(summaryParts.length){
            var formatted=summaryParts.join('\n');
            if(inputEl){
                if(inputEl.value.trim()){
                    inputEl.value=inputEl.value.trim()+'\n\n'+formatted;
                }else{
                    inputEl.value=formatted;
                }
            }
        }
        picker.remove();
        _currentPicker=null;
    };
    if(searchEl)setTimeout(function(){searchEl.focus()},100);
}
function addVocabButtonToInput(inputEl,storeKey){
    if(inputEl.dataset.vocabAdded)return;
    inputEl.dataset.vocabAdded='1';
    var parent=inputEl.parentElement;
    if(!parent)return;
    var label=parent.querySelector('label');
    if(!label)return;
    if(label.querySelector('.vocab-btn'))return;
    var btn=document.createElement('button');
    btn.type='button';
    btn.className='vocab-btn';
    btn.innerHTML='&#128218;';
    btn.title='选择专业词汇';
    btn.style.cssText='background:#6c5ce7;border:none;color:#fff;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:11px;margin-left:6px;vertical-align:middle';
    btn.onclick=function(e){
        e.preventDefault();e.stopPropagation();
        showVocabPicker(inputEl,'style',storeKey);
    };
    label.appendChild(btn);
}
function setupGenInputs(){
    var genFields=[
        {id:'p0',store:'gen_0'},
        {id:'p1',store:'gen_1'},
        {id:'p2',store:'gen_2'},
        {id:'p3',store:'gen_3'}
    ];
    genFields.forEach(function(g){
        var input=document.getElementById(g.id);
        if(input)addVocabButtonToInput(input,g.store);
    });
}
function hookEnhance(){
    var origEnh=window.enh;
    if(origEnh&&!origEnh._hooked){
        var newEnh=async function(t){
            var el=document.getElementById("p"+t);
            if(!el||!el.value.trim())return;
            var storeKey=_tabMap[t];
            var vocab=_vocabStore[storeKey]||{};
            var vocabParts=[];
            for(var k in vocab){
                if(vocab[k]&&vocab[k].length){
                    vocabParts.push(PM_NAMES[k]+': '+vocab[k].join(', '));
                }
            }
            var summary=vocabParts.join('\n');
            st("s"+t,"增强中...","pending");
            try{
                var payload={text:el.value.trim()};
                if(summary)payload.vocab=summary;
                var r=await ap("/api/prompts/enhance",payload);
                if(r.enhanced)el.value=r.enhanced;
                st("s"+t,"增强完成","success");
            }catch(e){st("s"+t,"增强失败:"+e.message,"error")}
        };
        newEnh._hooked=true;
        window.enh=newEnh;
    }
}
function addEditVocabButtons(){
    var keys=Object.keys(PM_NAMES);
    keys.forEach(function(key){
        var input=document.getElementById('e_'+key);
        if(!input||input.dataset.vocabAdded)return;
        input.dataset.vocabAdded='1';
        var parent=input.parentElement;
        if(!parent)return;
        var label=parent.querySelector('label');
        if(!label)return;
        if(label.querySelector('.vocab-btn'))return;
        var btn=document.createElement('button');
        btn.type='button';
        btn.className='vocab-btn';
        btn.innerHTML='&#128218;';
        btn.title='选择'+(PM_NAMES[key]||key)+'词汇';
        btn.style.cssText='background:#6c5ce7;border:none;color:#fff;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:11px;margin-left:6px;vertical-align:middle';
        btn.onclick=function(e){
            e.preventDefault();e.stopPropagation();
            showVocabPicker(input,key,'edit');
        };
        label.appendChild(btn);
    });
}
function addEditGenButton(){
    var saveBtn=document.getElementById('e_save');
    if(!saveBtn||saveBtn.dataset.genHooked)return;
    saveBtn.dataset.genHooked='1';
    var footer=saveBtn.parentElement;
    if(!footer||footer.querySelector('#e_gen'))return;
    var genBtn=document.createElement('button');
    genBtn.id='e_gen';
    genBtn.type='button';
    genBtn.className='btn';
    genBtn.style.cssText='background:linear-gradient(135deg,#6c5ce7,#a29bfe);color:#fff;border:none;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:12px';
    genBtn.textContent='AI优化提示词';
    genBtn.onclick=async function(e){
        e.preventDefault();e.stopPropagation();
        var textEl=document.getElementById('e_text');
        if(!textEl)return;
        var text=textEl.value.trim();
        if(!text){alert('请先输入提示词内容');return}
        var vocab=_vocabStore['edit']||{};
        var vocabParts=[];
        for(var k in vocab){
            if(vocab[k]&&vocab[k].length){
                vocabParts.push(PM_NAMES[k]+': '+vocab[k].join(', '));
            }
        }
        var summary=vocabParts.join('\n');
        genBtn.disabled=true;
        genBtn.textContent='AI优化中...';
        try{
            var payload={text:text};
            if(summary)payload.vocab=summary;
            var r=await ap("/api/prompts/enhance",payload);
            if(r.enhanced){
                textEl.value=r.enhanced;
                alert('提示词已优化');
            }
        }catch(err){alert('优化失败: '+err.message)}
        genBtn.disabled=false;
        genBtn.textContent='AI优化提示词';
    };
    footer.insertBefore(genBtn,saveBtn);
}
var _observer=new MutationObserver(function(){
    setupGenInputs();
    addEditVocabButtons();
    addEditGenButton();
    hookEnhance();
});
_observer.observe(document.body,{childList:true,subtree:true});
setTimeout(function(){setupGenInputs();hookEnhance()},500);
})();
