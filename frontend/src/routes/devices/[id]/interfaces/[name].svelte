<script context="module">
	export async function load({ fetch, params }) {
		let name = params.name;
		let id = params.id;
		const resOne = await fetch(`http://localhost:8000/devices/${id}`, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await resOne.json();

		const resTwo = await fetch(
			`http://localhost:8000/devices/${id}/restconf?xpath=Cisco-IOS-XE-interfaces-oper:interfaces/interface=${name}`,
			{
				method: 'GET',
				credentials: 'include'
			}
		);
		let interfaceDetails = await resTwo.json();
		interfaceDetails = interfaceDetails['Cisco-IOS-XE-interfaces-oper:interface'];
		let basicDetails = {};
		let extraDetails = {};
		for (let [key, value] of Object.entries(interfaceDetails)) {
			if (typeof value === 'object' && value !== null) {
				extraDetails[`${key}`] = value;
			} else {
				basicDetails[`${key}`] = value;
			}
		}

		if (resOne.ok && resTwo.ok) {
			return {
				props: {
					device,
					basicDetails,
					extraDetails,
					interfaceDetails
				}
			};
		}
		return {
			status: resTwo.status,
			error: new Error('Could not retrieve interface details')
		};
	}
</script>

<script>
	export let device;
	export let basicDetails;
	export let extraDetails;
	import title from '$lib/stores/title';
	import moment from 'moment';

	$title = `${device.name} - ${basicDetails.name}`;
	function capitalize(string) {
		return string.charAt(0).toUpperCase() + string.slice(1);
	}
	function lastChange(string) {
		return moment(string).fromNow();
	}
</script>

<div class="grid grid-cols-2 gap-4">
	<div class="card card-normal bg-base-100 shadow-xl w-96">
		<div class="card-body">
			<h2 class="card-title">Interface Details</h2>
			{#each Object.entries(basicDetails) as [key, value]}
				<div class="flex">
					<div>
						<p class="font-bold">{key}:</p>
					</div>
					<div class="ml-2">
						{#if key === 'last-change'}
							<p>{lastChange(value)}</p>
						{:else}
							<p>{value !== '' ? value : '---'}</p>
						{/if}
					</div>
				</div>
				<div class="divider my-0 py-0" />
			{/each}
		</div>
	</div>
	{#each Object.entries(extraDetails) as [key, value]}
		<div class="card card-normal bg-base-100 shadow-xl w-96 grow">
			<div class="card-body">
				<h2 class="card-title">{capitalize(key)}</h2>
				{#each Object.entries(value) as [innerKey, innerValue]}
					<div class="flex">
						<div>
							<p class="font-bold">{innerKey}:</p>
						</div>
						<div class="ml-2">
							<p>{innerValue !== '' ? innerValue : '---'}</p>
						</div>
					</div>
					<div class="divider my-0 py-0" />
				{/each}
			</div>
		</div>
	{/each}
</div>

<style>
</style>
