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
	import { faBars, faHouse, faServer } from '@fortawesome/free-solid-svg-icons';
	import Icon from '$components/Icon.svelte';
	import SidebarNavItem from '$components/Sidebar/SidebarNavItem.svelte';
	import * as api from '$lib/api';
	let navActive = false;
	export let id;
	export let name;
	export let email;

	const toggleNav = () => {
		navActive = !navActive;
	};

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

	async function handleLogout() {
		const response = await api.post(fetch, '/auth/logout');
		if (response.message === 'Success') {
			window.location.replace('/');
		}
	}
</script>

<div>
	<main>
		<nav
			class="fixed bg-base-200 shadow left-0 top-0 bottom-0 overflow-hidden w-20 ease-in-out transition-all duration-300 {navActive
				? 'md:w-56'
				: 'md:w-20'}"
		>
			<div class="flex flex-col pt-2 transition-all duration-300 ease-in-out">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label tabindex="0" class="btn btn-ghost btn-square ml-3.5" on:click={toggleNav}>
					<Icon icon={faBars} size={'1.25x'} />
				</label>
				<ul
					class="menu p-2 rounded-box transition-all duration-300 ease-in-out {navActive
						? 'w-56'
						: ''} "
				>
					<!-- svelte-ignore a11y-label-has-associated-control -->
					{#each navLinks as link (link.title)}
						<SidebarNavItem href={link.href} iconData={link.icon} title={link.title} {navActive} />
					{/each}
				</ul>
			</div>
		</nav>
		<div class="{navActive ? 'md:ml-56' : 'md:ml-20'} transition-all duration-300 ease-in-out">
			<div class="navbar bg-base-100 shadow">
				<div class="flex-1">
					<a href="/" class="btn btn-ghost normal-case text-xl">NETNOTICS</a>
				</div>
				<div class="flex-none gap-2">
					<div class="form-control">
						<input type="text" placeholder="Search" class="input input-bordered" />
					</div>
					<div class="dropdown dropdown-end">
						<!-- svelte-ignore a11y-label-has-associated-control -->
						<div
							tabindex="0"
							class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow"
						>
							<div class="card-body">
								<span class="font-bold text-lg">8 Items</span>
								<span class="text-info">Subtotal: $999</span>
								<div class="card-actions">
									<button class="btn btn-primary btn-block">View cart</button>
								</div>
							</div>
						</div>
					</div>
					<div class="dropdown dropdown-end">
						<!-- svelte-ignore a11y-label-has-associated-control -->
						<label tabindex="0" class="btn btn-ghost btn-circle avatar">
							<div class="w-10 rounded-full">
								<img src="https://placeimg.com/80/80/people" alt="profile" />
							</div>
						</label>
						<ul
							tabindex="0"
							class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
						>
							<li>
								<a href="/" class="justify-between">
									Profile
									<span class="badge">New</span>
								</a>
							</li>
							<li><a href="/profile">Settings</a></li>
							<li><button on:click|once={handleLogout}>Logout</button></li>
						</ul>
					</div>
				</div>
			</div>
			<div class="pl-8 pt-8">
				<slot />
			</div>
		</div>
	</main>
</div>
