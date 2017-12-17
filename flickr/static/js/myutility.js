function photoBtnClick(btn) {
    console.log(btn.getAttribute('data-title'))
    id = btn.getAttribute('data-id')
    title = btn.getAttribute('data-title')
    url = btn.getAttribute('data-url')
    
    $('#hash-tags-existed').html('')
    
    $.ajax({
        type: 'GET',
        url: '/photo/' + id + '/tags/get',
        dataType: 'json',
        success: function(data) {
            waitingDialog.hide()
            
            console.log(data.status)
            if (typeof data.tags === 'undefined' || data.tags.length == 0) {
                $('#hash-tags-existed').html('<span class="tags-font">No tag</span>');
            }
            
            var tags = '';
            data.tags.forEach(e => {
                console.log('tag:' + e)
                tags += '<span class="badge badge-info tags-font">' +
                        e + '<button class="badge-delete" onclick="tagDeleteButtonClick(this)" tag-value="'+ e +'" photo-id="' + id + '">&times;</button></span>'
            })
            $('#hash-tags-existed').html(tags);
        },
        error: function() {
        }
    }
    ) 
    
    photoModalView.show(url, title, id)
    waitingDialog.show("Loading...")
}

function tagSaveButtonClick(btn) {
   $.ajax({
        type: 'POST',
        /*headers: {
          'Content-Type': 'application/json;charset=utf-8',  
        },*/
        url: '/photo/' + $('#hash-tags-save').val() + '/tags/add',
        data : {
            'tags' : $('#hash-tags').val(),
        },
        dataType: 'json',
        success: function(data) {
            waitingDialog.show("Saved...");
            console.log(data.status)
            //waitingDialog.hide();
            //waitingDialog.show("Saved!");
            
            if (typeof data !== 'undefined' && data.status == 'pass') {
                var tags = $('#hash-tags-existed').html();
                console.log("existed tags: " + tags)
                data.tags.forEach(e => {
                    console.log('tag:' + e)
                    tags += '<span class="badge badge-info tags-font">' +
                            e + '</span>'
                })
                $('#hash-tags-existed').html(tags)
                $('#hash-tags').val('')
            }
            
            setTimeout(() => {
                waitingDialog.hide();
            }, 1000
            )
        },
        error: function() {
            waitingDialog.show('Failed...')
            setTimeout(() => {
                waitingDialog.hide();
            }, 1000
            )
        }
    }
    )    
}

function tagDeleteButtonClick(btn) {
    tag = btn.getAttribute('tag-value');
    id = btn.getAttribute('photo-id');
    console.log("Delete: " + id + ',' + tag);
}

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

var photoModalView = photoModalView || (function($) {
    'use strict';    
    
    var $view = $(            
        '<div class="modal fade" id="photoModal" role="dialog" aria-labelledby="photoModalLabel" aria-hidden="true">' +
                '<div class="modal-dialog" role="document">' +
                    '<div class="modal-content">' +
                        '<div class="modal-header">' +
                            '<p class="modal-title photoset-title" id="photoModalLabel"></p>' +
                            '<button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
                                '<span aria-hidden="true">&times;</span>' +
                            '</button>' +
                        '</div>' +
                        '<div class="modal-body"><div class="card"></div></div>' +
                        '<div class="modal-footer">' +
                            '<div class="container">' +
                                '<span id="hash-tags-existed"></span>' +
                                '<textarea class="form-control" id="hash-tags"></textarea>' +
                                '<button type="button" class="btn btn-primary" id="hash-tags-save" onclick="tagSaveButtonClick(this)">Save</button>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>');
    
	return {
		show: function (url, title, id) {
			// Assigning defaults
			if (typeof url === 'undefined') {
				url = "";
			}
			if (typeof title === 'undefined') {
				title = 'Unknown';
			}
            if (typeof id === 'undefined') {
                id = -1;
            }

			// Configuring dialog
            $view.find('.modal-title').text(title)
            $view.find('.modal-body').find('.card').html('<img src="' + url + '" class="card-img-top img-fluid"/>')
            $view.find('#hash-tags-save').attr('value', id)
            
			// Adding callbacks
			/*if (typeof settings.onHide === 'function') {
				$view.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
					settings.onHide.call($view);
				});
			}*/
            
			// Opening dialog
			$view.modal();
		},
		/**
		 * Closes dialog
		 */
		hide: function () {
			$view.modal('hide');
		}
	};
})(jQuery);