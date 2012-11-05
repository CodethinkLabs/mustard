function expand_element(hash) {
  var anchor = hash.replace('#', '').replace(/\//g, '\\/');
  $('#' + anchor).parent().next('dd').show();
}

function collapse_element(hash) {
  var anchor = hash.replace('#', '').replace(/\//g, '\\/');
  $('#' + anchor).parent().next('dd').hide();
}

function show_element(hash) {
  var anchor = hash.replace('#', '').replace(/\//g, '\\/');
  $('#' + anchor).parent().show();
}

function hide_element(hash) {
  var anchor = hash.replace('#', '').replace(/\//g, '\\/');
  $('#' + anchor).parent().hide();
  $('#' + anchor).parent().next('dd').hide();
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

  $('#filter').keyup(function() {
    var search = $(this).val();
    $('dt > h2').each(function () {
      var title_match = $(this).text().search(new RegExp(search, 'i')) >= 0;
      var path_match = $(this).attr('id').search(new RegExp(search, 'i')) >= 0;
      var text_match = $(this).parent().next('dd').text().search(new RegExp(search, 'i')) >= 0;
      if (!search || search.length == 0 || text_match || title_match || path_match) {
        show_element($(this).attr('id'));
      } else {
        hide_element($(this).attr('id'));
      }
    });
  });
});

$(document).unload(function() {
  $('body').fadeOut(250);
});
