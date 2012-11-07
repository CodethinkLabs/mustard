/**
 * Show/hide functionality.
 */


function show(element, fade) {
  if (fade) {
    element.slideDown('fast', function() {
      if (element.hasClass('expanded')) {
        expand(element, fade);
      }
    });
  } else {
    element.show(0, function() {
      if (element.hasClass('expanded')) {
        expand(element, fade);
      }
    });
  }
}


function hide(element, fade) {
  if (fade) {
    element.parent().next('dd').slideUp('fast', function() {
      element.slideUp('fast');
    });
  } else {
    element.hide(0, function() {
      element.parent().next('dd').hide();
    });
  }
}


/**
 * Expand/collapse functionality.
 */


function expand(element, smooth) {
  element.addClass('expanded');
  if (smooth) {
    element.parent().next('dd').slideDown(250);
  } else {
    element.parent().next('dd').show();
  }
}


function collapse(element, smooth) {
  element.removeClass('expanded');
  if (smooth) {
    element.parent().next('dd').slideUp(250);
  } else {
    element.parent().next('dd').hide();
  }
}


function toggle_expanded(element, smooth) {
  if (smooth) {
    element.parent().next('dd').slideToggle(250);
  } else {
    element.parent().next('dd').toggle();
  }
  element.toggleClass('expanded');
}


function expand_hash_elements(hash) {
  var hash_paths = hash.replace('#', '').split(',');
  for (var index in hash_paths) {
    var path = hash_paths[index];
    $('#' + path.replace(/\//g, '\\/')).each(function() {
      expand($(this));
    });
  }
}


function merge_hashes(hash1, hash2) {
  var hash1_paths = hash1.replace('#', '').split(',');
  var hash2_paths = hash2.replace('#', '').split(',');
  var hash_map = new Array();

  for (var index in hash1_paths) {
    var path = hash1_paths[index];
    if (path != hash1_paths[0]) {
      hash_map[path] = true;
    }
  }

  for (var index in hash2_paths) {
    var path = hash2_paths[index];
    if (path != hash1_paths[0]) {
      hash_map[path] = true;
    }
  }

  var merged_paths = [hash1_paths[0]];
  for (var path in hash_map) {
    merged_paths.push(path);
  }
  return merged_paths;
}


function scroll_to_first_hash_element(hash) {
  if (hash.length > 0) {
    var paths = hash.replace('#', '').split(',');
    var path = paths[0].replace(/\//g, '\\/');
    $('html, body').animate({
      scrollTop: $('#' + path).offset().top
    }, 'slow');
  }
}


/**
 * Filter functionality.
 */


function element_matches_filter(element) {
  var needle = $('#filter').val();
  
  var title_match = element.text().search(new RegExp(needle, 'i')) >= 0;
  var path_match = element.attr('id').search(new RegExp(needle, 'i')) >= 0;
  var text_match = element.parent().next('dd').text().search(new RegExp(needle, 'i')) >= 0;

  if (!needle || needle.length == 0 || text_match || title_match || path_match) {
    return true;
  } else {
    return false;
  }
}

function element_is_unhappy(element) {
  var has = element.has('> .error');
  if (has.length > 0) {
    return true;
  } else {
    return false;
  }
}

function update_filter() {
  $('dt > h2').each(function () {
    var matches_unhappy = true;
    if ($('#unhappy-filter').hasClass('pressed')) {
      if (element_is_unhappy($(this))) {
        matches_unhappy = true;
      } else {
        matches_unhappy = false;
      }
    }
    if (matches_unhappy && element_matches_filter($(this))) {
      show($(this), true);
    } else {
      hide($(this), true);
    }
  });
}


function set_document_title() {
  var path = window.location.pathname.split('/');

  if (path.length > 1) {
    var page = path[path.length-1];
    page = page.charAt(0).toUpperCase() + page.slice(1);
    page = page.replace('-', ' ');
    document.title =  page + ' - ' + document.title;
  }
}


$(document).ready(function() {
  // fade the body in nicely
  $('body').hide().fadeIn(250);

  set_document_title();

  // collapse all items by default
  $('h2').each(function() {
    collapse($(this));
  });

  // expand all items in the # part of the URL
  expand_hash_elements(window.location.hash);

  // scroll to the first hash
  scroll_to_first_hash_element(window.location.hash);

  // tweaks for links 
  $('a').click(function(event) {
    var element = event.target;
    if (event.target.hash) {
      element = $(event.target);
    } else {
      element = $(event.target).parent();
    }

    var href = element.attr('href');

    if (href) {
      var url_segments = href.split('#');
      if (url_segments.length > 0) {
        expand_hash_elements(url_segments[1]);
        var target_path = url_segments[0];
        var current_path = window.location.pathname;
        if (target_path == current_path) {
          event.target.hash = merge_hashes(event.target.hash,
                                           window.location.hash);
          scroll_to_first_hash_element(event.target.hash);
        }
      }
    }
  });

  // allow elements to be expanded/collapsed
  $('h2').css('cursor', 'pointer');
  $('h2').mouseup(function() {
    toggle_expanded($(this), true);
  });

  // center all images
  $('img').each(function() {
    $(this).parent().each(function() {
      $(this).css('text-align', 'center');
    });
  });

  // install filter element
  $('#filter').keyup(function() {
    update_filter();
  });

  $('#reset-filter').click(function() {
    $('#filter').val('');
    update_filter();
  });

  $('#unhappy-filter').toggle(
    function() {
      $(this).addClass('pressed');
      $('h2').each(function() {
        if (element_is_unhappy($(this)) && element_matches_filter($(this))) {
          show($(this), true);
        } else {
          hide($(this), true);
        };
      });
    },
    function() {
      $(this).removeClass('pressed');
      update_filter();
    }
  );

  $('#predefined-filters').change(function() {
      $('#filter').val($(this).val());
      update_filter();
      $(this).val('');
  });
});


$(document).unload(function() {
  $('body').fadeOut(250);
});
