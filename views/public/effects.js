$(document).ready(function() {
  $('dd').hide();

  $('dt').css('cursor', 'pointer');
  $('dt').click(function () {
    $(this).next('dd').slideToggle(250);
  });
});
