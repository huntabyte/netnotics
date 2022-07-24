<script>
	import { goto } from '$app/navigation';
	import DeviceStore from '$lib/stores/DeviceStore';

	let name, ipAddress, site, vendor, model, operatingSystem, fqdn, username, password;

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
				operating_system: operatingSystem,
				fqdn: fqdn,
				username: username,
				password: password
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

<form class="divide-y divide-gray-200">
	<div class="divide-y divide-gray-200 sm:space-y-5">
		<div class="sm:space-y-5">
			<div class="sm:space-y-5">
				<div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start">
					<label for="name" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Name
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={name}
							type="text"
							name="name"
							id="name"
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
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
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
						/>
					</div>
				</div>
				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="model" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						FQDN/Hostname
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={fqdn}
							type="text"
							name="model"
							id="model"
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
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
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
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
							class="select select-bordered w-full max-w-xs"
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
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
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
							class="select select-bordered w-full max-w-xs"
						>
							<option>IOS-XE</option>
							<option>IOS</option>
							<option>JUNOS</option>
						</select>
					</div>
				</div>
				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="username" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Device Username
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={username}
							type="text"
							name="username"
							id="username"
							autocomplete="off"
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
						/>
					</div>
				</div>
				<div
					class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:border-t sm:border-gray-200 sm:pt-5"
				>
					<label for="password" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">
						Device Password
					</label>
					<div class="mt-1 sm:mt-0 sm:col-span-2">
						<input
							bind:value={password}
							type="password"
							name="password"
							id="password"
							class="input input-bordered input-md max-w-lg block w-full sm:max-w-xs rounded-md"
						/>
					</div>
				</div>
			</div>
		</div>

		<div class="pt-5">
			<div class="flex justify-end">
				<a sveltekit:prefetch href="/devices" class="btn btn-outline btn-error px-6">Cancel</a>
				<button on:click|once|preventDefault={handleCreate} class="btn btn-success ml-4 px-6"
					>Save</button
				>
			</div>
		</div>
	</div>
</form>
