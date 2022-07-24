<script context="module">
	export async function load({ fetch }) {
		const res = await fetch('http://localhost:8000/devices', {
			method: 'GET',
			credentials: 'include'
		});

		const devices = await res.json();

		if (res.ok) {
			return {
				props: {
					deviceCount: devices.length
				}
			};
		}
		return {
			status: res.status,
			error: new Error('Could not fetch devices')
		};
	}
</script>

<script>
	import title from '$lib/stores/title';
	export let deviceCount;
	import StatCard from '$components/StatCard.svelte';

	$title = 'Dashboard';
</script>

<StatCard title="Devices" link="/devices" value={deviceCount} />
