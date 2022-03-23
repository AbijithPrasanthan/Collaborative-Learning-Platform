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
        const api =
            new JitsiMeetExternalAPI(
                domain,
                options
            );
    };