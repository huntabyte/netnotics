import { BASE_URL } from '$lib/constants';

export async function get(fetch, path) {
	const url = BASE_URL + path;
	const response = await fetch(url, {
		method: 'GET',
		credentials: 'include'
	});
	const data = await response.json();

	return data;
}

export async function post(fetch, path, body = null) {
	if (body) {
		const response = await fetch(`${BASE_URL}${path}`, {
			method: 'POST',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});
		const data = await response.json();

		return data;
	} else {
		const response = await fetch(`${BASE_URL}${path}`, {
			method: 'POST',
			credentials: 'include'
		});
		const data = await response.json();

		return data;
	}
}

export async function remove(fetch, path) {
	const response = await fetch(`${BASE_URL}${path}`, {
		method: 'DELETE',
		credentials: 'include'
	});

	const data = await response.json();
	return data;
}
