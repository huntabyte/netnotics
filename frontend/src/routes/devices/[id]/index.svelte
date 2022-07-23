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
					device: device,
					interfaces: interfaces
				}
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
	export let interfaces;
	import title from '$lib/stores/title';
	import StatCard from '$components/StatCard.svelte';
	import { faEthernet } from '@fortawesome/free-solid-svg-icons';
	$title = `Device Overview - ${device.name.toUpperCase()}`;
</script>

<div class="container">
	<div class="flex">
		<StatCard
			title="Interfaces"
			value={interfaces.length}
			desc={''}
			figure={faEthernet}
			Size="lg"
			link="/devices/{device.id}/interfaces"
		/>
	</div>
</div>
