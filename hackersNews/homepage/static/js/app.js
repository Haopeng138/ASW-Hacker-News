function upvote(item, item_str) {
    let id = item.id.substring(3);

    let data = {id: id};
    let url = ((item_str === 'post') ? '/upvote-post' : '/upvote-comment');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': crsfToken
        },
        body: JSON.stringify(data)
    }).then(res => {

        res.json().then(res => {
            if (res.success) {
                item.children[0].style.visibility = 'hidden';

                scoreItem = document.getElementById('score_' + id);
                if (item_str === 'post') {
                    scoreItem.innerText =
                        (parseInt(scoreItem.innerText.match(/\d+/)[0]) + 1).toString() + ' points';
                }
            } else if (res.redirect) {
                window.location = '/accounts/login';
            }
        })

    }).catch(error => console.log(error));
}