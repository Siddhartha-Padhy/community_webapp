document
  .getElementById('search_user_btn')
  .addEventListener('click', (event) => {
    event.preventDefault()
    document.getElementById('results').innerHTML = ''
    query = document.getElementById('search_box').value
    const url = 'http://localhost:8000/search/' + query
    console.log(url)
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        console.log(data['results'])
        data['results'].forEach((user) => {
          document.getElementById('results').innerHTML += `
            <li class="list-group-item">
              <i class="fa fa-user" aria-hidden="true"></i>&nbsp;
              ${user.profileName}
              <a href="http://localhost:8000/explore/${user.username}" class="card-link">@${user.username}</a>
            </li>
            `
        })
      })
  })
