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
	let email;
	let password;

	import { BASE_URL } from '$lib/constants';

	async function handleLogin() {
		const res = await fetch(`${BASE_URL}/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: new URLSearchParams({
				username: email,
				password: password
			}),
			credentials: 'include'
		});
		const data = await res.json();
		if (data.message === 'Success') {
			window.location.replace('/');
		}
	}
</script>

<div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-md">
		<h2 class="mt-6 text-center text-3xl font-bold text-neutral">Sign in to your account</h2>
		<p class="mt-2 text-center text-sm text-gray-600">
			Or
			<a href="/register" class="font-medium text-primary hover:text-primary-focus">
				register for an account
			</a>
		</p>
	</div>
	<form>
		<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
			<div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
				<div class="space-y-6">
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

					<div class="flex items-center justify-between">
						<div class="form-control">
							<label class="label cursor-pointer">
								<input type="checkbox" checked="checked" class="checkbox checkbox-primary" />
								<span class="label-text ml-3">Remember me</span>
							</label>
						</div>

						<div class="text-sm">
							<a href="/" class="font-medium text-primary hover:text-primary-focus">
								Forgot your password?
							</a>
						</div>
					</div>

					<div>
						<button class="w-full btn btn-primary" on:click={handleLogin}>Login</button>
					</div>
				</div>
			</div>
		</div>
	</form>
</div>
