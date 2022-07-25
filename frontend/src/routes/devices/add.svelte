<script>
	import title from '$lib/stores/title';
	import DeviceForm from '../../components/DeviceForm.svelte';

	$title = 'Add New Device';
</script>

<div class="flex flex-col">
	<h1 class="text-2xl font-semibold pb-4">Add New Device</h1>
	<!-- TODO: Add edit or new prop to use same form for both editing and creating new devices -->
	<DeviceForm />
</div>
