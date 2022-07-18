<script>
	import * as api from '$lib/api';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	async function handleLogout() {
		const response = await api.post(fetch, '/auth/logout');
		if (response.message === 'Success') {
			window.location.replace('/');
		}
	}
</script>

<ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
	<li><a href="/profile">Profile</a></li>
	<li><button on:click|once={handleLogout}>Sign Out</button></li>
</ul>
