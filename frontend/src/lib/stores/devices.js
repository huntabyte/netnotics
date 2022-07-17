import { writable } from 'svelte/store';

export const devices = writable([
	{
		id: null,
		name: null,
		ip_address: null
	}
]);
