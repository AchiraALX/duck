/**
 *
 * Author: duck
 */

const host = 'http://localhost:5000/'


document.addEventListener('DOMContentLoaded', () => {
    const year = document.querySelectorAll('.year');

    year.forEach((year) => { year.textContent = new Date().getFullYear() });
    alert('New date what do you suggest?')
})


/**
 * Try to sign-up the user
 */
const joinDuck = () => {
    // Get the values
    const username = document.getElementById('sign-up-username').value;
    const email = document.getElementById('sign-up-email').value;
    const password = document.getElementById('sign-up-password').value;
    const confirmPassword = document.getElementById('sign-up-c-password').value;


    // Validate data
    if (password !== confirmPassword) {
        alert('passwords don\'t match');
        return
    }

    // Create FormData object
    const user = new FormData();

    // Parse data
    user.append("username", username);
    user.append("email", email);
    user.append("password", password);
    user.append("confirm-password", confirmPassword)

    for (const [key, value] of user) {
        alert(`${key}: ${value}`);
    }

    fetch(host + 'sign-up', {
        method: 'POST',
        body: user,
        headers: {
            "Duck-Auth": 'duck'
        }
    })
        .then((response) => response.json())
        .then((data) => {
            alert(JSON.stringify(data))
        })
        .catch((error) => ping());
}

/**
 * Renders Sign Up template
 */
const renderSignUp = () => {
    renderLoginSignUp('sign-up');
}

/**
 * Renders the login template
 */
const renderLogin = () => {
    renderLoginSignUp('login');
}

/**
 * Check for logged in status for the user
 *
 */

const logged = (token) => {
    fetch(host, {
        method: 'POST',
        headers: {
            'Duck-Auth': 'duck',
            'Duck-Authorization': token ? token : null
        }
    })
        .then((response) => response.json())
        .then((data) => {
            alert(JSON.stringify(data));
            const logStatus = document.querySelector('.login-status');
            //const dashboard = document.querySelector('.dashboard');
            if (data.status_code === 401) {
                const temp = `${loginButton()} | ${signUpButton()}`;
                logStatus.innerHTML = temp;

                //dashboard.innerHTML = temp;
            } else {
                logStatus.textContent = 'Log out';
                //dashboard.innerHTML = 'Dashboard &nbsp; &rightarrow;';
            }
        })
        .catch((error) => ping())
}


/**
 * Log out button
 */
const logoutButton = () => `
<button class="w3-button logout-button"
id="logout-button" onclick="logout()">Logout</button>
`



/**
 * Login button template
 */

const loginButton = () => `
<button class="w3-button login-button"
id="login-button" onclick="renderLogin()">Login</button>
`
const signUpButton = () => `
<button class="w3-button sign-up-button"
id="sign-up-button" onclick="renderSignUp()">Sign up</button>
`

/**
 *
 * @param {string} template -> name of template either login or sign-up
 */
const renderLoginSignUp = (template) => {
    const contentContainer = document.querySelector('.content');

    if (template === 'login') {
        contentContainer.innerHTML = loginTemplate();
    } else {
        contentContainer.innerHTML = signUpTemplate();
    }

    contentContainer.style.marginTop = '80px'
}

const ping = () => {
    return fetch(host + 'ping', {
        headers: {
            'Duck-Auth': 'duck'
        }
    })
        .then((response) => response.json())
        .catch((error) => {
            if (error instanceof TypeError) {
                const b = document.querySelector('body');
                b.innerHTML += pongTemplate('That is not you. Its us. Try refreshing the page.')
            }
            return false
        })
}

const getStatus = (status) => {
    const uri = 'http://localhost:5000/hi'

    fetch(uri, {
        headers: {
            'Duck-Auth': 'duck'
        }

    })
        .then((response) => response.json())
        .then((data) => {
            status.textContent = data.duck === 'Ok' ? 'Ok' : 'API is down'
        })
        .catch((error) => alert(error));
}

const pongTemplate = (message) => `
<div class="w3-modal" style="display: block;">
    <div class="modal-content w3-padding w3-round">
        <p class="w3-large">${message}</p>
    </div>
</div>
`


const loginTemplate = () => `
<div class="duck-form-container w3-card w3-round w3-padding-large">
    <div class="w3-display-container w3-center w3-xlarge" style="font-weight: 900;">
        Login
    </div>

    <br>
    <div class="w3-center w3-small w3-border-top w3-border-bottom w3-margin">
        <button class="w3-button w3-padding"> &plus; &nbsp; GitHub</button>
        <button class="w3-button w3-padding">&times; &nbsp; LinkedIn</button>
    </div>

    <div class="w3-padding-top-32">
        <div class="input">
            <input type="text" placeholder="Username" class="w3-small w3-input"
                name="login-username" id="login-username" autofocus>
        </div>
        <div class="input">
            <input type="password" placeholder="Password" class="w3-small w3-input w3-margin-top"
                name="login-password" id="login-password">
        </div>

        <div class="w3-center w3-margin-top w3-small">
            <button class="w3-button w3-margin-top w3-round"
                style="background-color: var(--eucalyptus);" onclick="login()">Hop
                in</button>
            <button class="w3-button w3-margin-top w3-margin-left w3-round w3-small"
                style="background-color: var(--maverick);">Forgot
                Password?</button>
        </div>
    </div>

</div>
`

const signUpTemplate = () => `
<div class="duck-form-container w3-card w3-round w3-padding-large">
    <div class="w3-display-container w3-center w3-xlarge" style="font-weight: 900;">
        Sign Up
    </div>
    <br>
    <div class="w3-center w3-small w3-border-top w3-border-bottom w3-margin">
        <button class="w3-button w3-padding"> &plus; &nbsp; GitHub</button>
        <button class="w3-button w3-padding">&timesb; &nbsp; LinkedIn</button>
    </div>

    <div class="w3-padding-top-32">
        <div class="input">
            <input type="text" placeholder="Username" class="w3-small w3-input" name="sign-up-username"
                id="sign-up-username" autofocus>
        </div>
        <div class="input">
            <input type="email" name="sign-up-email" id="sign-up-email" placeholder="Email"
                class="w3-small w3-input w3-margin-top">
        </div>
        <div class="input">
            <input type="password" placeholder="Password" class="w3-small w3-input w3-margin-top"
                name="sign-up-password" id="sign-up-password">
        </div>

        <div class="input">
            <input type="password" placeholder="Confirm Password" class="w3-small w3-input w3-margin-top"
                name="sign-up-c-password" id="sign-up-c-password">
        </div>

        <div class="w3-center w3-margin-top w3-small">
            <button class="w3-button w3-margin-top w3-round"
                style="background-color: var(--eucalyptus);" onclick="joinDuck()">Join
                Duck</button>
            <button class="w3-button w3-margin-top w3-margin-left w3-round w3-small"
                style="background-color: var(--maverick);">Forgot
                Password?</button>
        </div>
    </div>
</div>
`