import { browser } from '$app/env';

const BASE_URL = 'http://localhost:8000/api/v1';

export function browserGet(key) {
	if (browser) {
		const item = localStorage.getItem(key);

		if (item) {
			return JSON.parse(item);
		}
	}
	return null;
}

export function browserSet(key, value) {
	if (browser) {
		localStorage.setItem(key, value);
	}
}

export async function post(fetch, path, body) {
	let customError = false;

	try {
		let headers = {};
		if (!(body instanceof FormData)) {
			headers['Content-Type'] = 'application/json';
			body = JSON.stringify(body);
		}
		const token = browserGet('access_token');
		if (token) {
			headers['Authorization'] = 'Bearer ' + token;
		}

		const res = await fetch(`${BASE_URL}${path}`, {
			method: 'POST',
			body,
			headers
		});
		if (!res.ok) {
			try {
				const data = await res.json();
				const error = data.message[0].messages[0];
				customError = true;
				throw {
					id: error.id,
					message: error.message
				};
			} catch (err) {
				console.log(err);
				console.log('An unexpected API error occured');
				throw err;
			}
		}
		try {
			const json = await res.json();
			return json;
		} catch (err) {
			console.log(err);
			throw err;
		}
	} catch (err) {
		console.log(err);
		throw customError ? err : { id: '', message: 'An unknown error has occurred' };
	}
}
