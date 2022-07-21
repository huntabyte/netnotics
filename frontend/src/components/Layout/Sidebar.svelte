<script>
	import NavLink from './NavLink.svelte';

	export let navLinks;
</script>

<div class="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
	<div class="flex flex-col flex-grow border-r border-gray-200 pt-5 bg-white overflow-y-auto">
		<div class="flex items-center flex-shrink-0 px-4">
			<!-- <img
                class="h-8 w-auto"
                src=""
                alt="Netnotics"
            /> -->
			<p class="text-2xl font-medium uppercase">Netnotics</p>
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
