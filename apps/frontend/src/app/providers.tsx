"use client";

import { Provider } from "react-redux";
import { store } from "@/store";
import AuthInitializer from "@/features/auth/auth-initializer";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <Provider store={store}>
      <AuthInitializer />
      {children}
    </Provider>
  );
}
