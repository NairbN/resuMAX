"use client";

import { useEffect } from "react";
import { useAppDispatch } from "@/store/hooks";
import { me, refresh, logout } from "@/features/auth/store/thunks";

const REFRESH_INTERVAL_MS = 10 * 60 * 1000; // 10 minutes

const AuthInitializer = () => {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(me()).unwrap().catch(() => {
      // ignore initial failure; user may be unauthenticated
    });

    const id = setInterval(() => {
      dispatch(refresh())
        .unwrap()
        .catch(() => {
          dispatch(logout());
        });
    }, REFRESH_INTERVAL_MS);

    return () => {
      clearInterval(id);
    };
  }, [dispatch]);

  return null;
};

export default AuthInitializer;
