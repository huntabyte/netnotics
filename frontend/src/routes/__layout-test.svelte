<script>
	import ProfileDropdown from '$components/Layout/ProfileDropdown.svelte';
	import Icon from '$components/Icon.svelte';
	import {
		faBars,
		faHouse,
		faServer,
		faThumbtack,
		faThumbTack
	} from '@fortawesome/free-solid-svg-icons';
	import UserStore from '$lib/stores/UserStore';
	import NavLink from '$components/Layout/NewNavLink.svelte';
	import MobileNav from '../components/Layout/MobileNav.svelte';
	import TopBar from '../components/Layout/TopBar.svelte';
	export let initials = $UserStore.name.charAt(0);
	import title from '$lib/stores/title';
	let showUserMenu = false;
	let drawerOpen = true;

	function toggleUserMenu() {
		showUserMenu = !showUserMenu;
	}
	function toggleDrawer() {
		drawerOpen = !drawerOpen;
	}

	let navLinks = [
		{
			title: 'Dashboard',
			href: '/dashboard',
			icon: faHouse
		},
		{
			title: 'Devices',
			href: '/devices',
			icon: faServer
		}
	];
</script>

<div>
	<!-- Off-canvas menu for mobile, show/hide based on off-canvas menu state. -->
	<MobileNav />

	<!-- Static sidebar for desktop -->
	<div
		class="hidden md:flex {drawerOpen ? 'md:w-64' : 'md:w-20'} md:flex-col md:fixed md:inset-y-0"
	>
		<div class="flex flex-col flex-grow border-r border-gray-200 pt-5 bg-white overflow-y-auto">
			<div class="flex justify-between flex-shrink-0 px-6">
				<!-- <img
					class="h-8 w-auto"
					src=""
					alt="Netnotics"
				/> -->
				<p class="text-2xl font-medium uppercase">Netnotics</p>
				<button on:click={toggleDrawer} class="rotate-90">
					<Icon icon={faThumbtack} size="1x" />
				</button>
			</div>
			<div class="mt-5 flex-grow flex flex-col">
				<nav class="flex-1 px-4 pb-4 space-y-1">
					{#each navLinks as link}
						<NavLink title={link.title} href={link.href} icon={link.icon} />
					{/each}
				</nav>
			</div>
		</div>
	</div>

	<div class="{drawerOpen ? 'md:pl-64' : 'md:pl-20'} flex flex-col flex-1">
		<TopBar />
		<main class="flex-1">
			<div class="py-6">
				<div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
					<h1 class="text-2xl font-semibold text-gray-900">{$title}</h1>
				</div>
				<div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
					<div class="py-4">
						<slot />
					</div>
				</div>
			</div>
		</main>
	</div>
</div>
