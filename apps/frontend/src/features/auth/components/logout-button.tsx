"use client";

import { Button } from "@/components/ui/button";
import { logout } from "@/features/auth/store/thunks";
import { useAppDispatch } from "@/store/hooks";
import { useRouter } from "next/navigation";
import { useState } from "react";

type LogoutButtonProps = {
  className?: string;
  variant?: "default" | "outline" | "ghost" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
  children?: React.ReactNode;
};

const LogoutButton = ({
  className,
  variant = "outline",
  size = "sm",
  children = "Log out",
}: LogoutButtonProps) => {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const [pending, setPending] = useState(false);

  const handleLogout = async () => {
    setPending(true);
    try {
      await dispatch(logout()).unwrap();
      router.push("/login");
    } finally {
      setPending(false);
    }
  };

  return (
    <Button
      className={className}
      variant={variant}
      size={size}
      onClick={handleLogout}
      disabled={pending}
    >
      {pending ? "Logging out..." : children}
    </Button>
  );
};

export default LogoutButton;
