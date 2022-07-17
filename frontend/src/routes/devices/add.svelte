<script>
	import title from '$lib/stores/title';
	import DeviceForm from '../../components/DeviceForm.svelte';

	$title = 'Add New Device';
</script>

<!-- TODO: Add edit or new prop to use same form for both editing and creating new devices -->
<DeviceForm />
