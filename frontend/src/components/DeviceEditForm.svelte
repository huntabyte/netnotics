<script>
	import { BASE_URL } from '$lib/constants';
	import { goto } from '$app/navigation';
	import DeviceStore from '$lib/stores/DeviceStore';

	export let device;
	let name = device.name;
	let ipAddress = device.ip_address;
	let host = device.host;
	let username = device.username;
	let password = device.password;

	async function handleUpdate() {
		const res = await fetch(`${BASE_URL}/devices/${device.id}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify({
				name: name,
				ip_address: ipAddress,
				host: host,
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

<form>
	<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
		<div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
			<div class="space-y-6">
				<div class="form-control w-full">
					<label for="name" class="label">
						<span class="label-text font-semibold">Name</span>
					</label>
					<input
						type="text"
						id="name"
						name="name"
						class="input input-bordered w-full"
						required
						bind:value={name}
					/>
				</div>
				<div class="form-control w-full">
					<label for="host" class="label">
						<span class="label-text font-semibold">Host</span>
					</label>
					<input
						type="text"
						id="host"
						name="host"
						class="input input-bordered w-full"
						required
						bind:value={host}
					/>
				</div>
				<div class="form-control w-full">
					<label for="ipAddress" class="label">
						<span class="label-text font-semibold">IP Address</span>
					</label>
					<input
						type="text"
						id="ipAddress"
						name="ipAddress"
						class="input input-bordered w-full"
						required
						bind:value={ipAddress}
					/>
				</div>
				<div class="form-control w-full">
					<label for="username" class="label">
						<span class="label-text font-semibold">Device Username</span>
					</label>
					<input
						type="text"
						id="username"
						name="username"
						class="input input-bordered w-full"
						required
						bind:value={username}
					/>
				</div>

				<div class="form-control w-full">
					<label for="password" class="label">
						<span class="label-text font-semibold">Device Password</span>
					</label>
					<input
						type="password"
						id="password"
						name="password"
						required
						class="input input-bordered w-full"
						bind:value={password}
					/>
				</div>

				<div>
					<button class="w-full btn btn-primary" on:click|preventDefault={handleUpdate}
						>Edit Device</button
					>
				</div>
			</div>
		</div>
	</div>
</form>
