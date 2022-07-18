import { writable } from 'svelte/store';

const DeviceStore = writable([
	{
		id: null,
		name: null,
		ip_address: null,
		site: null,
		model: null,
		vendor: null,
		operating_system: null,
		os_version: null
	}
]);
export default DeviceStore;
