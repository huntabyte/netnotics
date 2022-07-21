<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const endpoint = `http://localhost:8000/devices/${id}`;
		let res = await fetch(endpoint, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await res.json();

		if (res.ok) {
			return {
				props: { device }
			};
		}
		return {
			status: res.status,
			error: new Error('Could not fetch the device')
		};
	}
</script>

<script>
	export let device;
	import title from '$lib/stores/title';

	$title = device.name.toUpperCase();
</script>

<h1>{device.name}</h1>
<a sveltekit:prefetch href="/devices/{device.id}/interfaces">Interfaces</a>
