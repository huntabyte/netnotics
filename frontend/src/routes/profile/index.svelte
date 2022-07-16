<script context="module">
	export async function load({ session }) {
		if (!session.authenticated) {
			return {
				status: 302,
				redirect: '/login'
			};
		}
		return {
			props: {
				id: session.user_id
			}
		};
	}
</script>

<script>
	import { onMount } from 'svelte';

	export let id;
	let name;
	let email;

	onMount(async () => {
		const res = await fetch('http://localhost:8000/users/me', {
			method: 'GET',
			credentials: 'include'
		});
		const user = await res.json();
		name = user.name;
		email = user.email;
	});
</script>

<h1>Profile {id}</h1>
<p>Welcome {name}, you are logged in with the email {email}</p>
