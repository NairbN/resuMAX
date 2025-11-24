export const routes = {
  home: "/",
  login: "/login",
  signup: "/signup",
  dashboard: "/dashboard",
  upload: "/dashboard/upload",
} as const;

export type RouteKey = keyof typeof routes;
