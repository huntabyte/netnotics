<script>
	export let device;
</script>

<tr>
	<td class="whitespace-nowrap py-2 pl-4 pr-3 text-sm text-gray-500 sm:pl-6">{device.name}</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm font-medium text-gray-900">{device.ip_address}</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-900">CAC</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">+$4.37</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">$3,509.00</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">12.00</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">$4,397.00</td>
	<td class="relative whitespace-nowrap py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
		<a href="/devices/{device.id}" class="text-indigo-600 hover:text-indigo-900"
			>Edit<span class="sr-only">, AAPS0L</span></a
		>
	</td>
</tr>
