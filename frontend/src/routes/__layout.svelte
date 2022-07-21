<script context="module">
	export async function load({ fetch, session }) {
		if (!session.authenticated) {
			return {
				status: 302,
				redirect: '/login'
			};
		}
		return {
			props: {
				id: session.user_id,
				name: session.name,
				email: session.email
			}
		};
	}
</script>

<script>
	import '../app.css';
	import title from '$lib/stores/title';
	import MobileNav from '../components/Layout/MobileNav.svelte';
	import Sidebar from '../components/Layout/Sidebar.svelte';
	import TopBar from '../components/Layout/TopBar.svelte';
	import UserStore from '$lib/stores/UserStore';
	import { onMount } from 'svelte';
	import { faHouse, faServer } from '@fortawesome/free-solid-svg-icons';

	export let name;
	export let id;
	export let email;

	onMount(() => {
		UserStore.update((current_user) => {
			return {
				id: id,
				name: name,
				email: email
			};
		});
	});

	$title = 'Dashboard';

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
	<Sidebar {navLinks} />
	<div class="md:pl-64 flex flex-col flex-1">
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
