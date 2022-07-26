import { writable } from 'svelte/store';

const DeviceStore = writable([
	{
		id: null,
		name: null,
		ip_address: null,
		host: null,
		manageable: false
	}
]);
export default DeviceStore;
