<script>
	import { goto } from '$app/navigation';
	import { DeviceStore } from '$lib/stores/DeviceStore';
	import { browser } from '$app/env';

	let name, ipAddress, site, vendor, model, operatingSystem;

	import { BASE_URL } from '$lib/constants';

	async function handleCreate() {
		const res = await fetch(`${BASE_URL}/devices`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify({
				name: name,
				ip_address: ipAddress,
				site: site,
				vendor: vendor,
				model: model,
				operating_system: operatingSystem
			})
		});

		const data = await res.json();
		// save poll to store
		DeviceStore.update((currentDevices) => {
			return [data, ...currentDevices];
		});
		goto('/devices');
	}
</script>

<form class="space-y-8 divide-y divide-gray-200">
	<div class="space-y-8 divide-y divide-gray-200 sm:space-y-5">
		<div class="pt-8 space-y-6 sm:pt-10 sm:space-y-5">
			<div>
				<h3 class="text-lg leading-6 font-medium text-gray-900">Device Information</h3>
				<p class="mt-1 max-w-2xl text-sm text-gray-500">Basic device related information</p>
			</div>
			<div class="space-y-6 sm:space-y-5">
				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="name" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Name
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={name}
							type="text"
							name="name"
							id="name"
							class="max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md"
						/>
					</div>
				</div>

				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="ip-address" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						IP Address
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={ipAddress}
							type="text"
							name="ip-address"
							id="ip-address"
							class="max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md"
						/>
					</div>
				</div>

				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="site" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Site
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={site}
							id="site"
							name="site"
							type="text"
							class="block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-300 rounded-md"
						/>
					</div>
				</div>

				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="vendor" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Vendor
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<select
							bind:value={vendor}
							id="vendor"
							name="vendor"
							class="max-w-lg block focus:ring-indigo-500 focus:border-indigo-500 w-full shadow-sm sm:max-w-xs sm:text-sm border-gray-300 rounded-md"
						>
							<option>Cisco</option>
							<option>Juniper</option>
							<option>Arista</option>
						</select>
					</div>
				</div>

				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="model" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Model
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={model}
							type="text"
							name="model"
							id="model"
							class="block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-300 rounded-md"
						/>
					</div>
				</div>

				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label
						for="operating-system"
						class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2"
					>
						Operating System
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<select
							bind:value={operatingSystem}
							id="vendor"
							name="vendor"
							class="max-w-lg block focus:ring-indigo-500 focus:border-indigo-500 w-full shadow-sm sm:max-w-xs sm:text-sm border-gray-300 rounded-md"
						>
							<option>IOS-XE</option>
							<option>IOS</option>
							<option>JUNOS</option>
						</select>
					</div>
				</div>
			</div>
		</div>

		<div class="pt-5">
			<div class="flex justify-end">
				<button
					href="/devices"
					type="button"
					class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
					>Cancel</button
				>
				<button
					on:click|once|preventDefault={handleCreate}
					class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
					>Save</button
				>
			</div>
		</div>
	</div>
</form>
