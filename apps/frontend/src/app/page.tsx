import tailwindcss from 'tailwindcss';
export default function Home() {
  return (
    <div className="min-h-screen w-full grid grid-cols-2">
      {/* LEFT: Auth panel */}
      <div className="flex flex-col justify-center px-8 py-12 md:px-16 bg-white">
        <div className="max-w-md w-full mx-auto">
          {/* Logo / Title */}
          <h1 className="text-3xl font-bold mb-2">Welcome back</h1>
          <p className="text-gray-500 mb-8">
            Sign in to continue to your dashboard.
          </p>

          {/* Form */}
          <form className="space-y-6">
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition"
            >
              Sign In
            </button>
          </form>

          {/* Small text */}
          <p className="mt-6 text-sm text-gray-500 text-center">
            Don&apos;t have an account?{" "}
            <button className="text-blue-600 hover:underline">
              Sign up
            </button>
          </p>
        </div>
      </div>

      {/* RIGHT: Hero panel */}
      <div className="md:flex flex-col justify-center px-12 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 text-white">
        <div className="max-w-md">
          <h2 className="text-4xl font-bold mb-4">
            A clean place for your events.
          </h2>
          <p className="text-indigo-100 mb-6">
            Track countdowns, stay on top of deadlines, and never miss an
            important moment again.
          </p>

          <ul className="space-y-2 text-sm text-indigo-100">
            <li>• Minimal, distraction-free interface</li>
            <li>• Smart reminders for upcoming events</li>
            <li>• Works across desktop and mobile</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
