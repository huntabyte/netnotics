<script>
	import NavLink from './NavLink.svelte';
	import Icon from '$components/Icon.svelte';
	import { faBars } from '@fortawesome/free-solid-svg-icons';
	export let navLinks;
	import { sidebarOpen } from '$lib/stores/ui';

	function toggleSidebar() {
		sidebarOpen.update((sidebar) => {
			return !$sidebarOpen;
		});
		console.log($sidebarOpen);
	}
</script>

<div
	class="hidden md:flex md:flex-col md:fixed md:inset-y-0 overflow-hidden md:w-20 md:active:w-56"
	class:active={$sidebarOpen}
>
	<div class="flex flex-col flex-grow border-r border-gray-200 pt-5 bg-white overflow-y-auto">
		<div
			class="flex items-center active:justify-between justify-center flex-shrink-0 px-4 overflow-hidden"
			class:active={$sidebarOpen}
		>
			{#if $sidebarOpen}
				<p class="text-2xl font-medium uppercase">Netnotics</p>
			{/if}
			<button on:click={toggleSidebar}>
				<Icon icon={faBars} size="1.25x" />
			</button>
		</div>
		<div class="mt-5 flex-grow flex flex-col">
			<nav class="flex-1 px-2 pb-4 space-y-1">
				{#each navLinks as link}
					<NavLink title={link.title} href={link.href} icon={link.icon} />
				{/each}
			</nav>
		</div>
	</div>
</div>
