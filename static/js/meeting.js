body =
    document.getElementsByTagName(
        "BODY"
    )[0];

title =
    document.querySelector(
        ".Title"
    );
title.remove();
body.onload =
    () => {
        const roomName =
            window.location.href.split(
                "/"
            )[5];

        const domain =
            "meet.jit.si";
        const options = {
            roomName: roomName,
            width: screen.width -
                150,
            height: screen.availHeight -
                150,
            parentNode: document.querySelector(
                "#meet"
            ),
        };
        api =
            new JitsiMeetExternalAPI(
                domain,
                options
            );

        api.on(
            "participantJoined",
            function(id, dispName) {
                var partInfo = JSON.stringify(api.getParticipantsInfo());
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                console.log("Participant Joined: ", id)
                $.ajax({
                    type: 'POST',
                    url: `/CLP/meeting/${roomName}/`,
                    data: {
                        'type': 'part_join',
                        'info': partInfo,
                        'userID': id,
                        'roomName': roomName,
                        'csrfmiddlewaretoken': csrftoken
                    },
                    success: function() {
                        console.log('Success');
                    },
                    error: function() {
                        console.log('Failed');
                    }
                })
            }
        );

        api.on("participantLeft", function(id) {
            var partInfo = JSON.stringify(api.getParticipantsInfo());
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            console.log("Participant Left", id)
            $.ajax({
                type: 'POST',
                url: `/CLP/meeting/${roomName}/`,
                data: {
                    'type': 'part_left',
                    'info': partInfo,
                    'userID': id,
                    'roomName': roomName,
                    'csrfmiddlewaretoken': csrftoken
                },
                success: function() {
                    console.log('Success');
                },
                error: function() {
                    console.log('Failed');
                }
            })
        })
    };