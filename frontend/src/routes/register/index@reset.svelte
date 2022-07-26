<script context="module">
	export async function load({ session }) {
		if (session.authenticated === true) {
			return {
				status: 302,
				redirect: '/dashboard'
			};
		}
		return {
			props: {}
		};
	}
</script>

<script>
	let name;
	let email;
	let password;

	import { BASE_URL } from '$lib/constants';
	import { goto } from '$app/navigation';

	async function handleRegister() {
		const res = await fetch(`${BASE_URL}/users/register`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				email: email,
				password: password,
				name: name
			}),
			credentials: 'include'
		});
		if (res.ok) {
			goto('/login');
		}
	}
</script>

<div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-md">
		<h2 class="mt-6 text-center text-3xl font-bold text-neutral">Register for an Account</h2>
		<p class="mt-2 text-center text-sm text-gray-600">
			Already have an account?
			<a href="/login" class="font-medium text-primary hover:text-primary-focus"> Login</a>
		</p>
	</div>
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
						<label for="email" class="label">
							<span class="label-text font-semibold">Email address</span>
						</label>
						<input
							type="email"
							id="email"
							name="email"
							class="input input-bordered w-full"
							required
							bind:value={email}
						/>
					</div>

					<div class="form-control w-full">
						<label for="password" class="label">
							<span class="label-text font-semibold">Password</span>
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
						<button class="w-full btn btn-primary" on:click|preventDefault={handleRegister}
							>Register</button
						>
					</div>
				</div>
			</div>
		</div>
	</form>
</div>
