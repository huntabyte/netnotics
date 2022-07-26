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
	import DeviceEditForm from '$components/DeviceEditForm.svelte';
	export let device;
</script>

<div class="flex flex-col">
	<h1 class="text-2xl font-semibold pb-4">Edit Device - {device.name}</h1>
	<!-- TODO: Add edit or new prop to use same form for both editing and creating new devices -->
	<DeviceEditForm {device} />
</div>
