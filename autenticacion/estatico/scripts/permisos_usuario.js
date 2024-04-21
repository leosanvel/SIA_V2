$(document).ready(function() {
    $('.folder').click(function(event) {
        if ($(event.target).prop('tagName').toLowerCase() !== 'input') {
            var checkbox = $(this).prev();
            checkbox.prop('checked', !checkbox.prop('checked'));
            $(this).siblings('ul').toggleClass('collapsed');
        }
    });
});
