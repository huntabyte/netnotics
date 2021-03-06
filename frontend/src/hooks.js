import * as cookie from 'cookie';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	const cookies = cookie.parse(event.request.headers.get('cookie') || '');

	event.locals.user = cookies;

	if (!cookies.session_id) {
		event.locals.user.authenticated = false;
		const response = await resolve(event);
		return response;
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
		event.locals.user.name = data.user.name;
		event.locals.user.email = data.user.email;
	}

	const response = await resolve(event);

	return response;
}

export function getSession(event) {
	if (!event.locals.user.authenticated) {
		return {
			authenticated: event.locals.user.authenticated
		};
	}

	return {
		authenticated: event.locals.user.authenticated,
		user_id: event.locals.user.id,
		name: event.locals.user.name,
		email: event.locals.user.email
	};
}
