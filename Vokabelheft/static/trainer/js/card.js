var word = $('p.word');
var key = $('p.key');
var my_word = word.text();
var my_key = key.text();

$('div#card').hide();
$('h3#key').text(my_key);
$('h3#word').text(my_word).hide();
var myswitch = 1;
$('div.card-body').on('click', function() {
    if (myswitch == 1) {
        $('h3#key').fadeOut(1500);
        $('h3#word').delay(1490).fadeIn(1500);
        myswitch = 0;
    } else {
        $('h3#word').fadeOut(1500);
        $('h3#key').delay(1490).fadeIn(1500);
        myswitch = 1;
    }
});