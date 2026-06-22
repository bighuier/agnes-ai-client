(function(){
    window._fav = false;

    window.toggleFav = async function(id, currentFav) {
        var newFav = currentFav ? 0 : 1;
        try {
            await fetch('/api/prompts/' + id, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ favorite: newFav })
            });
            if (window.pl) window.pl();
        } catch(e) { console.error(e); }
    };

    // 添加收藏筛选按钮
    function addFavBtn() {
        var s = document.querySelector('.srch');
        if (!s || document.getElementById('_favBtn')) return;
        var b = document.createElement('button');
        b.id = '_favBtn';
        b.innerHTML = '☆';
        b.title = '收藏筛选';
        b.style.cssText = 'background:none;border:none;color:#888;font-size:18px;cursor:pointer;padding:4px 8px;transition:color .2s';
        b.onclick = function(e) {
            window._fav = !window._fav;
            b.innerHTML = window._fav ? '★' : '☆';
            b.style.color = window._fav ? '#fdcb6e' : '#888';
            if (window.pl) window.pl();
        };
        s.appendChild(b);
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        addFavBtn();
    } else {
        window.addEventListener('load', addFavBtn);
    }
})();
