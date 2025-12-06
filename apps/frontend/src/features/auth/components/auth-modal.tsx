"use client";

import { X } from "lucide-react";
import Login from "@/features/auth/components/login";
import SignUp from "@/features/auth/components/signup";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";

type AuthModalProps = {
  open: boolean;
  mode: "login" | "signup";
  onClose: () => void;
  onSwitchMode: (mode: "login" | "signup") => void;
};

const AuthModal = ({ open, mode, onClose, onSwitchMode }: AuthModalProps) => {
  const router = useRouter();

  const handleSuccess = () => {
    onClose();
    router.push("/dashboard");
  };

  // Parent controls mode via props; no routing here.

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur bg-white/60 dark:bg-white/20"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25, ease: "easeInOut" }}
        >
          <motion.div
            className="absolute inset-0"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
            onClick={onClose}
          />
          <motion.div
            className="relative w-full max-w-2xl mx-4 overflow-hidden rounded-2xl border border-border bg-card text-card-foreground shadow-2xl"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
          >
            <button
              onClick={onClose}
              className="absolute right-4 top-4 z-10 rounded-full bg-foreground/20 p-2 text-foreground hover:bg-foreground/30"
              aria-label="Close"
            >
              <X className="h-5 w-5" />
            </button>
            <div className="relative">
              {mode === "login" ? (
                <Login
                  variant="modal"
                  onSuccess={handleSuccess}
                  onSwitchMode={(next) => onSwitchMode(next)}
                />
              ) : (
                <SignUp
                  variant="modal"
                  onSuccess={handleSuccess}
                  onSwitchMode={(next) => onSwitchMode(next)}
                />
              )}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default AuthModal;
