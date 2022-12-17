var word = $('p.word');
var key = $('p.key');
var my_word = word.text();
var my_key = key.text();

$('div#card').hide();
$('h#key').text(my_key);
$('h#word').text(my_word).hide();
var myswitch = 1;
$('div.card-body').on('click', function() {
    if (myswitch == 1) {
        $('h#key').fadeOut(1500);
        $('h#word').delay(1490).fadeIn(1500);
        myswitch = 0;
    } else {
        $('h#word').fadeOut(1500);
        $('h#key').delay(1490).fadeIn(1500);
        myswitch = 1;
    }
});