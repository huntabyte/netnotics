import { writable } from 'svelte/store';

const UserStore = writable({
	id: 'x',
	name: 'x',
	email: 'x'
});

export default UserStore;
