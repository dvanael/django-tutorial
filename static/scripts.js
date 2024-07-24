$(document).ready(function() {
  function convertMarkdownToHtml(file) {
    $.ajax({
      url: file,
      success: function(markdownContent) {
        const converter = new showdown.Converter();
        const htmlContent = converter.makeHtml(markdownContent);
        $('#markdownContent').html(htmlContent);

        $('#summary').html('');

        $('#markdownContent').find('h1, h2, h3, h4').each(function(index) {
          if (!$(this).attr('id')) {
            $(this).attr('id', 'heading_' + index);
          }

          $('#summary').append('<a href="#' + $(this).attr('id') + '"><li class="side-link list-group-item summary-link">' + $(this).text() + '</li></a>');
        });

        Prism.highlightAll();
      },
      error: function(error) {
        console.error('Error loading Markdown file:', error);
      }
    });
  }

  $('.md-button').click(function() {
    const file = $(this).data('file');
    convertMarkdownToHtml(file);
    $('#offcanvasResponsive').offcanvas('hide');
    $('.markdown-content').animate({
        scrollTop: $('#top').offset().top
    }, 'slow');
  });

  convertMarkdownToHtml($('.md-button').first().data('file'));
});