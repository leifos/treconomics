var timeoutFlag = false;

$(document).ready(function()
{
     $('#username').focus()

     $('.survey table tr').filter(':odd').addClass('odd');


	 $('.matrix ul').each(function() {
		$('li:first-child label input').css('float', 'right');
	  });

	  $('.addButton').toggle(function() {
      	  $('.hidden').css({display: 'inline'});
	  $(this).attr('value','-');
   	  return false;
	  }, function() {
      	  $('.hidden').css({display: 'none'});
	  $(this).attr('value','+');
   	  return false;
	   });



    $('#end-task-link').click(function() {
		target = null;
		marked = null;
		
		$.ajax({
			url: '/treconomics/diversityendstats/' + TASKID + '/',
			async: false,
			success: function(data) {
				target = data['target'];
				marked = data['marked'];
			}
		});
		
		if (target) {
			if (marked == 1)
				return confirm("You have saved only 1 document. The target for you to reach is " + target + ". Press CANCEL to continue searching, or OK to end the task.");
			else
				return confirm("You have saved " + marked + " documents. The target for you to reach is " + target + ". Press CANCEL to continue searching, or OK to end the task.");
		}
		
		return confirm("Clicking OK will take you to the next stage of the experiment. If you clicked the 'End Task' link by accident, you can push the CANCEL button below.");
    })

}); 


