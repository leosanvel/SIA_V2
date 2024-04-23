$(document).ready(function() {
    $('.folder1').click(function(event) {
        if ($(event.target).prop('tagName').toLowerCase() !== 'input') {
            var checkbox = $(this).prev();
            checkbox.prop('checked', !checkbox.prop('checked'));
            $(this).siblings('ul').toggleClass('collapsed');
        }
    });
});
