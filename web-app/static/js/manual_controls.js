function engageSwitch(impButton) {
    if (impButton.textContent == "Engage") {
        impButton.textContent = "Disengage";
    }
    else {
        impButton.textContent = "Engage";
    }

    fetch('/engageSwitch', {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(impButton.textContent),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
            })
        })
        .then(function (response) {
            // impButton.textContent = "Might've Engaged"
            return response.json();
        })

}