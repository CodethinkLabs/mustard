function expand_element(hash) {
  var anchor = hash.replace('#', '').replace(/\//g, '\\/');
  $('#' + anchor).parent().next('dd').show();
}

$(document).ready(function() {
  $('body').hide().fadeIn(250);

  $('dd').hide();
  expand_element(window.location.hash);

  if ($('dt').size() == 1) {
    $('dt').next('dd').show();
  }

  $('a').click(function(event) {
    expand_element(event.target.hash);
  });

  $('dt').css('cursor', 'pointer');
  $('dt').click(function () {
    $(this).next('dd').slideToggle(250);
  });

  $('img').each(function() {
    $(this).parent().each(function() {
      $(this).css('text-align', 'center');
    });
  });
});

$(document).unload(function() {
  $('body').fadeOut(250);
});
