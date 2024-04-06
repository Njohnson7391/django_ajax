console.log('hello world detail')

const postBox = document.getElementById('post-box')
const alertBox = document.getElementById('alert-box')
const backBtn = document.getElementById('back-btn')
const updateBtn = document.getElementById('update-btn')
const deleteBtn = document.getElementById('delete-btn')

const url = window.location.href + "data/"
const updateUrl = window.location.href + "update/"
const deleteUrl = window.location.href + "delete/"

const updateForm = document.getElementById('update-form')
const deleteForm = document.getElementById('delete-form')

const spinnerBox = document.getElementById('spinner-box')

const titleInput = document.getElementById('id_title')
const bodyInput = document.getElementById('id_body')

const commentForm = document.getElementById('comment-form')
const commentsSection = document.getElementById('comments-section')

const csrf = document.getElementsByName('csrfmiddlewaretoken')


// backBtn.addEventListener('click', ()=>{
//     history.back()
// })

$.ajax({
    type: 'GET',
    url: url,
    success: function(response){
        console.log(response)
        const data = response.data

        if (data.logged_in !== data.author){
            console.log('different')
        }else {
            console.log('the same')
            updateBtn.classList.remove('not-visible')
            deleteBtn.classList.remove('not-visible')
        }

        const titleEl = document.createElement('h3')
        titleEl.setAttribute('class', 'mt-3')
        titleEl.setAttribute('id', 'title')

        const bodyEl = document.createElement('p')
        bodyEl.setAttribute('class', 'mt-1')
        bodyEl.setAttribute('id', 'body')

        titleEl.textContent = data.title
        bodyEl.textContent = data.body

        postBox.appendChild(titleEl)
        postBox.appendChild(bodyEl)

                // New code to create an avatar image and username element
        const userBox = document.createElement('div')
        userBox.className = 'user-box d-flex align-items-center mb-3'  // Bootstrap classes for flexbox and alignment

        const avatarEl = document.createElement('img')
        avatarEl.src = data.avatar  // The avatar URL from your AJAX response
        avatarEl.alt = 'User avatar'  // Alternative text for the avatar image
        avatarEl.className = 'rounded-circle mr-2'  // Bootstrap class for rounded images and margin
        avatarEl.style.width = '40px'  // Adjust width as needed
        avatarEl.style.height = '40px'  // Adjust height as needed
        avatarEl.style.objectFit = 'cover'  // Ensure the image covers the area

        const usernameEl = document.createElement('span')
        usernameEl.textContent = data.author  // The username from your AJAX response
        usernameEl.className = 'username'  // Class for potential additional styling

        // Append the avatar and username to the userBox
        userBox.appendChild(avatarEl)
        userBox.appendChild(usernameEl)

        // Append the userBox to the postBox
        postBox.appendChild(userBox)


        titleInput.value = data.title
        bodyInput.value = data.body

        spinnerBox.classList.add('not-visible')
    },
    error: function(error){
        console.log(error)
    }
})

updateForm.addEventListener('submit', e=>{
    e.preventDefault()

    const title = document.getElementById('title')
    const body = document.getElementById('body')

    $.ajax({
        type: 'POST',
        url: updateUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'title': titleInput.value,
            'body': bodyInput.value,
        },
        success: function(response){
            console.log(response)
            handleAlerts('success', 'post has been updated')
            title.textContent = response.title
            body.textContent = response.body
            usernameEl.textContent = `Posted by: ${data.author}`
        },
        error: function(error){
            console.log(error)
        }
    })


})


deleteForm.addEventListener('submit', e=>{
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: deleteUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
        },
        success: function(response){
           window.location.href = window.location.origin
           localStorage.setItem('title', titleInput.value)
        },
        error:function(error){
            console.log(error)
        }
    })
})

commentForm.addEventListener('submit', e => {
    e.preventDefault();

    const commentInput = document.getElementById('comment-input');
    const commentText = commentInput.value;
    const url = commentForm.getAttribute('data-url');  // Get the URL from the data attribute
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'comment': commentText,
        },
        success: function(response) {
            commentInput.value = '';  // Clear the input field on success

            // Create and append the new comment element
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.innerHTML = `
                <strong>${response.username}</strong>
                <p>${response.comment}</p>
            `;
            commentsSection.appendChild(newComment);
        },
        error: function(error) {
            console.error(error);
        }
    });
});