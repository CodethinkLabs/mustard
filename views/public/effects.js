$(document).ready(function() {
  //$('dd').hide();

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
