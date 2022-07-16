import * as cookie from 'cookie';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	const cookies = cookie.parse(event.request.headers.get('cookie') || '');

	event.locals.user = cookies;

	if (!cookies.session_id) {
		event.locals.user.authenticated = false;
	}

	const userSession = await fetch(`http://localhost:8000/auth/session/${cookies.session_id}`, {
		method: 'GET'
	});
	const data = await userSession.json();

	if (!data.authenticated) {
		event.locals.user.authenticated = false;
	} else {
		event.locals.user.authenticated = true;
		event.locals.user.id = data.user_id;
	}

	const response = await resolve(event);

	return response;
}

export function getSession(event) {
	console.log(event.locals.user);
	if (!event.locals.user.authenticated) {
		return {
			authenticated: event.locals.user.authenticated
		};
	}

	return {
		authenticated: event.locals.user.authenticated,
		user_id: event.locals.user.id
	};
}
