/* base.js */


function move(id, until=200) {
	div=$(id);
	right = parseInt(div.css('right'));
	until = parseInt(until)
	if(right < until){
		btn.css('opacity', (right/until).toFixed(1));
		div.css('right', right+5+'px');
		setTimeout("move('"+id+"', until='"+until+"')",0.2);
	}
}

function moveWaitingButtun(id){
	btn =$(id);
	right = btn.css('right');
	btn.css('right',0);
	btn.css('opacity',0);
	move(id, until=right);
}


$(document).ready(function(){
	// moveWaitingButtun("#btn-waiting-for-call");
})