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
	let name;

	async function handleRegister() {
		console.log('handling register');
		const body = {
			email: email,
			name: name,
			password: password
		};
		const response = await fetch('http://localhost:8000/users/register', {
			method: 'POST',
			body: JSON.stringify(body),
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (response.ok) {
			window.location.replace('/');
		} else {
			console.log('error occurred');
		}
	}
</script>

<div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-md">
		<img
			class="mx-auto h-12 w-auto"
			src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
			alt="Workflow"
		/>
		<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Sign Up</h2>
		<p class="mt-2 text-center text-sm text-gray-600">
			Already a user?
			<a href="/login" class="font-medium text-indigo-600 hover:text-indigo-500"> Login </a>
		</p>
	</div>

	<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
		<div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
			<form class="space-y-6" action="/" method="POST">
				<div>
					<label for="name" class="block text-sm font-medium text-gray-700"> Full name </label>
					<div class="mt-1">
						<input
							bind:value={name}
							id="name"
							name="name"
							type="text"
							required
							class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
						/>
					</div>
				</div>
				<div>
					<label for="email" class="block text-sm font-medium text-gray-700"> Email address </label>
					<div class="mt-1">
						<input
							bind:value={email}
							id="email"
							name="email"
							type="email"
							required
							class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
						/>
					</div>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium text-gray-700"> Password </label>
					<div class="mt-1">
						<input
							bind:value={password}
							id="password"
							name="password"
							type="password"
							required
							class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
						/>
					</div>
				</div>

				<div>
					<button
						on:click|preventDefault={handleRegister}
						class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
						>Sign Up</button
					>
				</div>
			</form>
		</div>
	</div>
</div>
