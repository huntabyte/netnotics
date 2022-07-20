<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const url = `http://localhost:8000/devices/${id}`;
		let res = await fetch(url, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await res.json();

		res = await fetch(
			`http://localhost:8000/devices/${id}/restconf?xpath=Cisco-IOS-XE-native:native/version`,
			{
				method: 'GET',
				credentials: 'include'
			}
		);
		let data = await res.json();
		const version = data['Cisco-IOS-XE-native:version'];

		return {
			props: {
				device,
				version
			}
		};
	}
</script>

<script>
	export let device;
	export let version;
</script>

<h1>Device Name: {device.name}</h1>
<h1>Version: {version}</h1>
