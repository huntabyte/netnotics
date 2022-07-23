<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const endpoint = `http://localhost:8000/devices/${id}/interfaces`;
		const res = await fetch(endpoint, {
			method: 'GET',
			credentials: 'include'
		});
		const data = await res.json();
		const device = data['device'];
		const interfaces = data['data'];

		if (res.ok) {
			return {
				props: {
					device,
					interfaces
				}
			};
		}
		return {
			status: resTwo.status,
			error: new Error('Could not retrieve device interface information')
		};
	}
</script>

<script>
	export let device;
	export let interfaces;
	import title from '$lib/stores/title';
	import InterfaceTable from '$components/InterfaceTable.svelte';

	$title = `Interface Overview - ${device.name.toUpperCase()}`;
</script>

<div class="shadow-xl">
	<InterfaceTable {interfaces} {device} />
</div>
