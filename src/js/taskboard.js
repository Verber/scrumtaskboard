$(document).ready(function(){
    /* HANDLERS */
    $(".add-task").click(function(){
           $('#story-key').val($(this).parents('tr.story-row').attr("id"));
           $('.add-task-dialog').dialog({
               title: 'Add new task',
               close: function(event, ui) {
                    $('.add-task-dialog').dialog('destroy');
               }
           });
        })

    $('#new-task-form').ajaxForm({
        dataType:  'json',
        success: function(data) {
            if (data.success) {
                var task = '<div class="draggable task-sticker"'
                    +'id="'+data.task_key+'">'
                    +'<div class="task">'
                    +$(".add-task-dialog input[name='name']").val()
                    +'<span class="estimate">'
                    +$(".add-task-dialog input[name='estimate']").val()
                    +'</span>'
                    +'</div>'
                    +'</div>';
                $('#'+$('#story-key').val()+' td.not-started').append(task);
                $('#'+data.task_key).draggable({
                    containment: $(this).parents('tr.story-row'),
                    snap: false,
                    snapMode: 'inner',
                    snapTolerance: 100,
                    scope: 'tasks',
                    revert: 'invalid',
                    helper: 'original',
                    cursor: 'move'
                });
                $('.add-task-dialog').dialog('close');
            } else {
                alert(data.message);
            }
        }
    });

    $('.draggable').each(function(){
        $(this).draggable({
            //cancel: 'a.ui-icon',// clicking an icon won't initiate dragging
            containment: $(this).parents('tr.story-row'),
            snap: false,
            snapMode: 'inner',
            snapTolerance: 100,
            scope: 'tasks',
            revert: 'invalid',
            helper: 'original',
            cursor: 'move'
        });
    });

    $('th').droppable({scope: 'stories'});
    $('td.droppable').droppable({
        scope: 'tasks',
        tolerance: 'pointer',
        drop: function(event, ui){
            $(this).append(ui.draggable);
            ui.draggable.removeAttr('style');
            ui.draggable.draggable('destroy');
            ui.draggable.draggable({
                containment: $(this).parents('tr.story-row'),
                snap: false,
                snapMode: 'inner',
                snapTolerance: 100,
                scope: 'tasks',
                revert: 'invalid',
                helper: 'original',
                cursor: 'move'
            });
            changeStatus(ui.draggable.attr('id'), $(this));
        }
    });

    function changeStatus(task_key, dropp_status)
    {
        var new_status = '';
        if ($(dropp_status).hasClass('not-started')) {
            new_status = 'Not Started';
        } else if ($(dropp_status).hasClass('done')) {
            new_status = 'Done';
        } else {
            new_status = 'In Progress';
        }
        $.post('/taskboard/set_status', {key: task_key, status: new_status})
    }
})

