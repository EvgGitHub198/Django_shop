  $(document).ready(function() {
    // Show dropdown menu on hover
    $('.dropdown').hover(function() {
      $(this).find('.dropdown-menu').addClass('show');
    }, function() {
      $(this).find('.dropdown-menu').removeClass('show');
    });
  });

