<script>
	import { devices } from '$lib/stores/devices';
	import DeviceRow from './DeviceRow.svelte';
</script>

<div class="mt-8 flex flex-col">
	<div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
		<div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
			<div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
				<table class="min-w-full divide-y divide-gray-300">
					<thead class="bg-gray-50">
						<tr>
							<th
								scope="col"
								class="whitespace-nowrap py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6"
								>Name</th
							>
							<th
								scope="col"
								class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
								>IP Address</th
							>
							<th
								scope="col"
								class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Site</th
							>
							<th
								scope="col"
								class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Model</th
							>
							<th
								scope="col"
								class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Vendor</th
							>
							<th
								scope="col"
								class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Operating System</th
							>
							<th
								scope="col"
								class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
								>OS Version</th
							>
							<th scope="col" class="relative whitespace-nowrap py-3.5 pl-3 pr-4 sm:pr-6">
								<span class="sr-only">Edit</span>
							</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 bg-white">
						{#each $devices as device}
							<DeviceRow {device} />
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
