$('#photoModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var url = button.data('url') // Extract info from data-* attributes
    var title = button.data('title') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text(title)
    modal.find('.modal-body').find('.card').html('<img src="' + url + '" class="card-img-top img-fluid"/>')
})

$('#hash-tags-save').click(function(){
    //$('#hash-tags').text($('#hash-tags-save').val())
    waitingDialog.show("Saving...");
    $.ajax({
        type: 'POST',
        headers: {
          'X_CSRF_TOKEN': 'test',  
        },
        url: '/photo/' + $('#hash-tags-save').val() + '/savetags',
        data : {
            tags: "'" + $('#hash-tags').val() + "'",
        },
        dataType: 'json',
        success: function(data) {
            console.log(data.status)
            //waitingDialog.hide();
            //waitingDialog.show("Saved!");
            setTimeout(() => {
                waitingDialog.hide();
            }, 1000
            )
        },
        error: function() {
            
        }
    }
    )
})

var waitingDialog = waitingDialog || (function ($) {
    'use strict';

	// Creating modal dialog's DOM
	var $dialog = $(
		'<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="overflow-y:visible;">' +
		'<div class="modal-dialog" align="center">' +
			'<div class="modal-body">' +
        			'<div class="alert alert-info myalert myalert-font"></div>' +
				/*'<div class="progress progress-striped active" style="margin-bottom:0;"><div class="progress-bar" style="width: 100%"></div></div>' +*/
			'</div>' +
		'</div></div>');

	return {
		/**
		 * Opens our dialog
		 * @param message Custom message
		 * @param options Custom options:
		 * 				  options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
		 * 				  options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
		 */
		show: function (message, options) {
			// Assigning defaults
			if (typeof options === 'undefined') {
				options = {};
			}
			if (typeof message === 'undefined') {
				message = 'Loading';
			}
			var settings = $.extend({
				dialogSize: 'm',
				progressType: '',
				onHide: null // This callback runs after the dialog was hidden
			}, options);

			// Configuring dialog
			$dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
			$dialog.find('.progress-bar').attr('class', 'progress-bar');
			/*if (settings.progressType) {
				$dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
			}*/
			$dialog.find('.alert').text(message);
			// Adding callbacks
			if (typeof settings.onHide === 'function') {
				$dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
					settings.onHide.call($dialog);
				});
			}
			// Opening dialog
			$dialog.modal();
		},
		/**
		 * Closes dialog
		 */
		hide: function () {
			$dialog.modal('hide');
		}
	};

})(jQuery);