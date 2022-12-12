var word = $('p.word');
var key = $('p.key');
var my_word = word.text();
var my_key = key.text();

$('div#card').hide();
$('p#key').text(my_key);
$('p#word').text(my_word).hide();
var myswitch = 1;
$('div.card-body').on('click', function() {
    if (myswitch == 1) {
        $('p#key').fadeOut(1500);
        $('p#word').delay(1490).fadeIn(1500);
        myswitch = 0;
    } else {
        $('p#word').fadeOut(1500);
        $('p#key').delay(1490).fadeIn(1500);
        myswitch = 1;
    }
});