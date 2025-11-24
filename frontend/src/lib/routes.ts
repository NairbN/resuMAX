export const routes = {
  home: "/",
  login: "/login",
  signup: "/signup",
  dashboard: "/dashboard",
} as const;

export type RouteKey = keyof typeof routes;
