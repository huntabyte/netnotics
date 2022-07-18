<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const url = `http://localhost:8000/devices/${id}`;
		const res = await fetch(url, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await res.json();
		return {
			props: {
				device
			}
		};
	}
</script>

<script>
	export let device;
</script>

<h1>{device.name}</h1>
